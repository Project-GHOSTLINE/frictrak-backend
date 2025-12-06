#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRICTRAK API Backend - Railway
==============================
API Flask pour analyser les données Inverite
"""

import os
import json
import tempfile
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Import des modules locaux
from analyser_hybride import process_json_file_hybrid, load_paiements_excel
from listes_completes_v2 import (
    PRETEURS_TOUS, PRETEURS_OFFICIELS_OPC, categoriser_transaction,
    est_preteur, est_a_exclure, est_assurance, est_syndic, est_casino
)

# Charger les paiements au démarrage
PAIEMENTS = load_paiements_excel()

app = Flask(__name__)
CORS(app, origins=["*"])  # Permettre les requêtes cross-origin

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "FRICTRAK API",
        "version": "2.0.0-reports",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy"})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyser des données JSON Inverite

    Body: JSON avec les données Inverite complètes
    Returns: Rapport d'analyse
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Aucune donnée JSON fournie"
            }), 400

        # Créer un fichier temporaire avec les données
        temp_file = os.path.join(UPLOAD_FOLDER, f"inverite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        try:
            # Analyser le fichier avec la fonction hybride
            resultat = process_json_file_hybrid(temp_file, PAIEMENTS)

            if resultat is None:
                return jsonify({
                    "success": False,
                    "error": "Erreur lors de l'analyse du fichier"
                }), 500

            # Retourner les résultats
            return jsonify({
                "success": True,
                "analysis": resultat,
                "timestamp": datetime.now().isoformat()
            })

        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/analyze-direct', methods=['POST'])
def analyze_direct():
    """
    Analyse directe sans fichier - traite les données en mémoire
    Format Inverite: details (pas description), debit/credit (pas amount)
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Aucune donnée JSON fournie"
            }), 400

        # Extraire les informations de base
        client_name = data.get('name', 'Inconnu')
        reference_id = data.get('referenceid', '')
        accounts = data.get('accounts', [])

        # Analyser les transactions
        all_transactions = []
        preteurs_detectes = {}
        nsf_count = 0
        nsf_details = []
        total_revenus = 0
        total_depenses = 0
        debt_total = 0

        for account in accounts:
            transactions = account.get('transactions', [])

            for tx in transactions:
                # INVERITE utilise 'details' pas 'description'
                description = (tx.get('details') or tx.get('description') or '').upper()

                # INVERITE utilise 'debit'/'credit' pas 'amount'
                debit = float(tx.get('debit') or 0)
                credit = float(tx.get('credit') or 0)
                amount = credit - debit  # Positif = entrée, Négatif = sortie

                tx_date = tx.get('date', '')

                # Compter les NSF (chercher dans description ET flags)
                flags = tx.get('flags', [])
                is_nsf = ('NSF' in description or
                          'INSUFFICIENT' in description or
                          'FONDS INSUFF' in description or
                          'OVERDRAFT' in description or
                          any('nsf' in str(f).lower() for f in flags))

                if is_nsf:
                    nsf_count += 1
                    nsf_details.append({
                        'date': tx_date,
                        'montant': debit or credit,
                        'description': description
                    })

                # Catégoriser revenus/dépenses
                if credit > 0:
                    total_revenus += credit
                if debit > 0:
                    total_depenses += debit

                # Détecter les prêteurs
                if est_preteur(description):
                    preteur_info = categoriser_transaction(description)
                    if preteur_info and preteur_info.get('preteur'):
                        preteur_nom = preteur_info['preteur']
                        if preteur_nom not in preteurs_detectes:
                            preteurs_detectes[preteur_nom] = {
                                'nom': preteur_nom,
                                'source': preteur_info.get('source', 'detection'),
                                'transactions': [],
                                'total': 0
                            }
                        preteurs_detectes[preteur_nom]['transactions'].append({
                            'date': tx_date,
                            'amount': debit or credit,
                            'description': description
                        })
                        preteurs_detectes[preteur_nom]['total'] += (debit or credit)
                        debt_total += (debit or credit)

        # Extraire revenus depuis payschedules si disponibles
        revenu_from_payschedules = 0
        payschedules = data.get('payschedules', [])

        # Chercher aussi dans accounts[0].payschedules
        if not payschedules and accounts:
            payschedules = accounts[0].get('payschedules', [])

        # Chercher dans stats
        stats = data.get('stats', {})
        employer_income = float(stats.get('employer', {}).get('last_amount', 0) or 0)
        govt_income = float(stats.get('government', {}).get('last_amount', 0) or 0)

        if employer_income > 0 or govt_income > 0:
            revenu_from_payschedules = employer_income + govt_income
            print(f"📊 Revenus stats: employer={employer_income}, govt={govt_income}")
        elif payschedules:
            for ps in payschedules:
                amount = float(ps.get('amount', 0) or ps.get('last_amount', 0) or 0)
                revenu_from_payschedules += amount
            print(f"📊 Revenus payschedules: {revenu_from_payschedules}")

        # Calculer revenu mensuel
        # Priorité: payschedules > calcul depuis transactions (sur 3 mois)
        if revenu_from_payschedules > 0:
            revenu_mensuel = revenu_from_payschedules
        else:
            revenu_mensuel = round(total_revenus / 3, 2)

        # Calculer le score de risque
        score = 100
        alertes = []

        # Pénalités prêteurs
        nb_preteurs = len(preteurs_detectes)
        if nb_preteurs > 0:
            score -= min(nb_preteurs * 10, 40)
            alertes.append({
                "type": "preteurs",
                "niveau": "critical" if nb_preteurs >= 3 else "warning",
                "message": f"{nb_preteurs} prêteur(s) alternatif(s) détecté(s)",
                "details": list(preteurs_detectes.keys())
            })

        # Pénalités NSF
        if nsf_count > 0:
            score -= min(nsf_count * 5, 25)
            alertes.append({
                "type": "nsf",
                "niveau": "critical" if nsf_count >= 3 else "warning",
                "message": f"{nsf_count} transaction(s) NSF détectée(s)",
                "details": nsf_details
            })

        # Score minimum
        score = max(score, 0)

        # Décision
        if score >= 70:
            decision = "BON DOSSIER"
        elif score >= 50:
            decision = "ATTENTION REQUISE"
        else:
            decision = "DOSSIER À RISQUE"

        # Construire le résultat
        result = {
            "success": True,
            "client": {
                "nom": client_name,
                "reference": reference_id
            },
            "resume": {
                "score_risque": str(score),
                "decision": decision,
                "revenu_mensuel": round(revenu_mensuel, 2),
                "depenses_mensuelles": round(total_depenses / 3, 2),
                "nsf_count": nsf_count,
                "preteurs_count": nb_preteurs,
                "debt_detected": round(debt_total, 2)
            },
            "preteurs": list(preteurs_detectes.values()),
            "alertes": alertes,
            "nsf_details": nsf_details,
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/check-preteur', methods=['POST'])
def check_preteur():
    """
    Vérifier si une description correspond à un prêteur
    """
    try:
        data = request.get_json()
        description = data.get('description', '')

        is_preteur = est_preteur(description)
        info = categoriser_transaction(description) if is_preteur else None

        return jsonify({
            "success": True,
            "description": description,
            "is_preteur": is_preteur,
            "info": info
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/preteurs-list', methods=['GET'])
def preteurs_list():
    """
    Retourner la liste des prêteurs connus
    """
    return jsonify({
        "success": True,
        "total": len(PRETEURS_TOUS),
        "opc_officiels": len(PRETEURS_OFFICIELS_OPC),
        "preteurs": PRETEURS_TOUS[:100]  # Limiter pour la réponse
    })


# ============================================
# NOUVEAUX ENDPOINTS POUR EXTENSION OVERWATCH
# ============================================

DOSSIERS_DIR = os.path.join(os.path.dirname(__file__), 'dossiers-clients')

def sanitize_filename(name):
    """Nettoyer les noms de fichiers"""
    import unicodedata
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    name = ''.join(c if c.isalnum() or c in '_-' else '_' for c in name)
    name = '_'.join(filter(None, name.split('_')))
    return name.upper()


@app.route('/api/save-dossier', methods=['POST'])
def save_dossier():
    """
    Sauvegarder un dossier client (Margill + Inverite)
    """
    try:
        data = request.get_json()
        reference = data.get('reference')
        prenom = data.get('prenom', 'INCONNU')
        nom = data.get('nom', 'INCONNU')
        margill_data = data.get('margillData')
        inverite_data = data.get('inveriteData')
        inverite_guid = data.get('inveriteGuid')

        if not reference:
            return jsonify({"success": False, "error": "Référence manquante"}), 400

        # Créer le répertoire si nécessaire
        if not os.path.exists(DOSSIERS_DIR):
            os.makedirs(DOSSIERS_DIR, exist_ok=True)

        # Nom du dossier
        folder_name = f"{sanitize_filename(reference)}_{sanitize_filename(prenom)}_{sanitize_filename(nom)}"
        folder_path = os.path.join(DOSSIERS_DIR, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        saved_files = []

        # Sauvegarder margill.json
        if margill_data:
            margill_path = os.path.join(folder_path, 'margill.json')
            margill_data['_metadata'] = {
                'saved_at': datetime.now().isoformat(),
                'source': 'overwatch-extension-v6',
                'reference': reference
            }
            with open(margill_path, 'w', encoding='utf-8') as f:
                json.dump(margill_data, f, ensure_ascii=False, indent=2)
            saved_files.append('margill.json')

        # Sauvegarder inverite.json
        if inverite_data:
            inverite_path = os.path.join(folder_path, 'inverite.json')
            inverite_data['_metadata'] = {
                'saved_at': datetime.now().isoformat(),
                'source': 'overwatch-extension-v6',
                'reference': reference,
                'guid': inverite_guid
            }
            with open(inverite_path, 'w', encoding='utf-8') as f:
                json.dump(inverite_data, f, ensure_ascii=False, indent=2)
            saved_files.append('inverite.json')

        # Index
        index_path = os.path.join(folder_path, 'index.json')
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump({
                'reference': reference,
                'client': {'prenom': prenom, 'nom': nom},
                'files': saved_files,
                'created_at': datetime.now().isoformat(),
                'inverite_guid': inverite_guid
            }, f, ensure_ascii=False, indent=2)

        print(f"✅ Dossier sauvegardé: {folder_name}")

        return jsonify({
            "success": True,
            "folderName": folder_name,
            "files": saved_files
        })

    except Exception as e:
        print(f"❌ Erreur save-dossier: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/pedro-analyze', methods=['POST'])
def pedro_analyze():
    """
    Recevoir et analyser les logs de Pedro (extension debug)
    """
    try:
        data = request.get_json()
        logs = data.get('logs', [])
        url = data.get('url', '')
        timestamp = data.get('timestamp', datetime.now().isoformat())

        print(f"🐻 Pedro reçoit {len(logs)} lignes de log")
        print(f"   URL: {url}")

        # Analyser les logs pour détecter les erreurs
        errors = [log for log in logs if '[X]' in log or 'ERREUR' in log]
        successes = [log for log in logs if '[+]' in log]

        # Sauvegarder le log
        logs_dir = os.path.join(os.path.dirname(__file__), 'pedro-logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir, exist_ok=True)

        log_file = os.path.join(logs_dir, f"pedro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return jsonify({
            "success": True,
            "message": f"Pedro a bien reçu! {len(errors)} erreurs, {len(successes)} succès",
            "errors_count": len(errors),
            "successes_count": len(successes)
        })

    except Exception as e:
        print(f"❌ Erreur pedro-analyze: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Cache en mémoire pour les rapports (simple dict)
REPORTS_CACHE = {}

@app.route('/api/analyze-inverite', methods=['POST'])
def analyze_inverite():
    """
    Analyser des données Inverite et retourner un rapport
    Format Inverite: details (pas description), debit/credit (pas amount)
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "Aucune donnée"}), 400

        # Extraire infos client
        client_name = data.get('name', 'Inconnu')
        accounts = data.get('accounts', [])

        # Compter transactions et détecter prêteurs
        total_transactions = 0
        preteurs_detectes = {}
        nsf_count = 0
        nsf_details = []
        total_revenus = 0
        total_depenses = 0
        debt_total = 0

        for account in accounts:
            transactions = account.get('transactions', [])
            total_transactions += len(transactions)

            for tx in transactions:
                # INVERITE utilise 'details' pas 'description'
                description = (tx.get('details') or tx.get('description') or '').upper()

                # INVERITE utilise 'debit'/'credit' pas 'amount'
                debit = float(tx.get('debit') or 0)
                credit = float(tx.get('credit') or 0)
                tx_date = tx.get('date', '')

                # NSF (chercher dans description ET flags)
                flags = tx.get('flags', [])
                is_nsf = ('NSF' in description or
                          'INSUFFICIENT' in description or
                          'FONDS INSUFF' in description or
                          'OVERDRAFT' in description or
                          any('nsf' in str(f).lower() for f in flags))

                if is_nsf:
                    nsf_count += 1
                    nsf_details.append({
                        'date': tx_date,
                        'montant': debit or credit,
                        'description': description
                    })

                # Revenus/Dépenses
                if credit > 0:
                    total_revenus += credit
                if debit > 0:
                    total_depenses += debit

                # Prêteurs
                if est_preteur(description):
                    info = categoriser_transaction(description)
                    if info and info.get('preteur'):
                        nom = info['preteur']
                        if nom not in preteurs_detectes:
                            preteurs_detectes[nom] = {'nom': nom, 'count': 0, 'total': 0}
                        preteurs_detectes[nom]['count'] += 1
                        preteurs_detectes[nom]['total'] += (debit or credit)
                        debt_total += (debit or credit)

        # Extraire revenus depuis payschedules/stats
        revenu_from_payschedules = 0
        payschedules = data.get('payschedules', [])

        if not payschedules and accounts:
            payschedules = accounts[0].get('payschedules', [])

        stats = data.get('stats', {})
        employer_income = float(stats.get('employer', {}).get('last_amount', 0) or 0)
        govt_income = float(stats.get('government', {}).get('last_amount', 0) or 0)

        if employer_income > 0 or govt_income > 0:
            revenu_from_payschedules = employer_income + govt_income
        elif payschedules:
            for ps in payschedules:
                amount = float(ps.get('amount', 0) or ps.get('last_amount', 0) or 0)
                revenu_from_payschedules += amount

        # Revenu mensuel
        if revenu_from_payschedules > 0:
            revenu_mensuel = revenu_from_payschedules
        else:
            revenu_mensuel = round(total_revenus / 3, 2)

        # Score
        score = 100
        score -= min(len(preteurs_detectes) * 10, 40)
        score -= min(nsf_count * 5, 25)
        score = max(score, 0)

        # Générer ID unique
        report_id = f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Construire le rapport complet
        report_data = {
            "success": True,
            "id": report_id,
            "client": {
                "nom": client_name
            },
            "score_global": score,
            "resume": {
                "transactions_analysees": total_transactions,
                "preteurs_count": len(preteurs_detectes),
                "nsf_count": nsf_count,
                "revenu_mensuel": round(revenu_mensuel, 2),
                "revenus": round(total_revenus, 2),
                "depenses": round(total_depenses, 2),
                "debt_detected": round(debt_total, 2)
            },
            "preteurs_detectes": list(preteurs_detectes.values()),
            "nsf_details": nsf_details,
            "alertes": [],
            "timestamp": datetime.now().isoformat()
        }

        # Ajouter alertes
        if len(preteurs_detectes) > 0:
            report_data["alertes"].append({
                "type": "preteurs",
                "niveau": "critical" if len(preteurs_detectes) >= 3 else "warning",
                "message": f"{len(preteurs_detectes)} prêteur(s) alternatif(s) détecté(s)",
                "details": list(preteurs_detectes.keys())
            })
        if nsf_count > 0:
            report_data["alertes"].append({
                "type": "nsf",
                "niveau": "critical" if nsf_count >= 3 else "warning",
                "message": f"{nsf_count} transaction(s) NSF détectée(s)",
                "details": nsf_details
            })

        # Sauvegarder dans le cache
        REPORTS_CACHE[report_id] = report_data
        print(f"✅ Rapport {report_id} sauvegardé en cache")

        # Aussi sauvegarder en fichier JSON
        reports_dir = os.path.join(os.path.dirname(__file__), 'rapports-cache')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir, exist_ok=True)
        report_file = os.path.join(reports_dir, f"{report_id}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        return jsonify({
            "success": True,
            "id": report_id,
            "client": client_name,
            "score": score,
            "knockOuts": len(preteurs_detectes)
        })

    except Exception as e:
        print(f"❌ Erreur analyze-inverite: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/get-report/<report_id>', methods=['GET'])
def get_report(report_id):
    """
    Récupérer un rapport par son ID
    """
    try:
        # 1. Chercher dans le cache mémoire
        if report_id in REPORTS_CACHE:
            print(f"✅ Rapport {report_id} trouvé en cache mémoire")
            return jsonify(REPORTS_CACHE[report_id])

        # 2. Chercher dans les fichiers
        reports_dir = os.path.join(os.path.dirname(__file__), 'rapports-cache')
        report_file = os.path.join(reports_dir, f"{report_id}.json")

        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Rapport {report_id} trouvé en fichier")
            # Remettre en cache
            REPORTS_CACHE[report_id] = data
            return jsonify(data)

        print(f"❌ Rapport {report_id} non trouvé")
        return jsonify({"success": False, "error": "Rapport non trouvé"}), 404

    except Exception as e:
        print(f"❌ Erreur get-report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/save-report', methods=['POST'])
def save_report():
    """
    Sauvegarder un rapport complet (depuis Vercel/extension)
    POST /api/save-report
    Body: { id: string, data: object }
    """
    try:
        body = request.get_json()
        report_id = body.get('id')
        report_data = body.get('data', body)  # Si pas de 'data', utiliser tout le body

        if not report_id:
            return jsonify({"success": False, "error": "ID manquant"}), 400

        # Sauvegarder en cache mémoire
        REPORTS_CACHE[report_id] = report_data

        # Sauvegarder en fichier (persistant)
        reports_dir = os.path.join(os.path.dirname(__file__), 'rapports-cache')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir, exist_ok=True)

        report_file = os.path.join(reports_dir, f"{report_id}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"💾 Rapport sauvegardé: {report_id}")

        return jsonify({
            "success": True,
            "id": report_id,
            "message": "Rapport sauvegardé"
        })

    except Exception as e:
        print(f"❌ Erreur save-report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/reports', methods=['GET'])
def list_reports():
    """
    Lister tous les rapports sauvegardés
    GET /api/reports
    Returns: { success: true, reports: [...] }
    """
    try:
        reports = []

        # Lire tous les fichiers du dossier rapports-cache
        reports_dir = os.path.join(os.path.dirname(__file__), 'rapports-cache')
        if os.path.exists(reports_dir):
            for filename in os.listdir(reports_dir):
                if filename.endswith('.json'):
                    report_id = filename.replace('.json', '')
                    report_file = os.path.join(reports_dir, filename)

                    try:
                        with open(report_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # Extraire les infos essentielles
                        client_nom = data.get('client', {}).get('nom', 'Inconnu')
                        if not client_nom or client_nom == 'Inconnu':
                            client_nom = data.get('nom', 'Inconnu')

                        created_at = data.get('created_at', '')
                        if not created_at:
                            # Utiliser la date de modification du fichier
                            mtime = os.path.getmtime(report_file)
                            created_at = datetime.fromtimestamp(mtime).isoformat()

                        reports.append({
                            "id": report_id,
                            "client_nom": client_nom,
                            "created_at": created_at,
                            "data": data
                        })

                        # Aussi mettre en cache
                        REPORTS_CACHE[report_id] = data

                    except Exception as e:
                        print(f"⚠️ Erreur lecture {filename}: {e}")

        # Trier par date (plus récent en premier)
        reports.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        print(f"📋 {len(reports)} rapports listés")

        return jsonify({
            "success": True,
            "reports": reports,
            "count": len(reports)
        })

    except Exception as e:
        print(f"❌ Erreur list-reports: {e}")
        return jsonify({"success": False, "error": str(e), "reports": []}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
