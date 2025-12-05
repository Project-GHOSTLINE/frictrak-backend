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
        "version": "1.0.0",
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
        total_revenus = 0
        total_depenses = 0

        for account in accounts:
            transactions = account.get('transactions', [])

            for tx in transactions:
                description = tx.get('description', '').upper()
                amount = float(tx.get('amount', 0))
                tx_type = tx.get('type', '')

                # Compter les NSF
                if 'NSF' in description or 'INSUFFICIENT' in description or 'FONDS INSUFF' in description:
                    nsf_count += 1

                # Catégoriser
                if tx_type == 'credit' or amount > 0:
                    total_revenus += abs(amount)
                else:
                    total_depenses += abs(amount)

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
                            'date': tx.get('date', ''),
                            'amount': amount,
                            'description': description
                        })
                        preteurs_detectes[preteur_nom]['total'] += abs(amount)

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
                "message": f"{nb_preteurs} prêteur(s) alternatif(s) détecté(s)"
            })

        # Pénalités NSF
        if nsf_count > 0:
            score -= min(nsf_count * 5, 25)
            alertes.append({
                "type": "nsf",
                "niveau": "critical" if nsf_count >= 3 else "warning",
                "message": f"{nsf_count} transaction(s) NSF détectée(s)"
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
                "revenu_mensuel": round(total_revenus / 3, 2),  # Approximation 3 mois
                "depenses_mensuelles": round(total_depenses / 3, 2),
                "nsf_count": nsf_count,
                "preteurs_count": nb_preteurs
            },
            "preteurs": list(preteurs_detectes.values()),
            "alertes": alertes,
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
        total_revenus = 0
        total_depenses = 0

        for account in accounts:
            transactions = account.get('transactions', [])
            total_transactions += len(transactions)

            for tx in transactions:
                description = tx.get('description', '').upper()
                amount = float(tx.get('amount', 0))

                # NSF
                if 'NSF' in description or 'INSUFFICIENT' in description:
                    nsf_count += 1

                # Revenus/Dépenses
                if amount > 0:
                    total_revenus += amount
                else:
                    total_depenses += abs(amount)

                # Prêteurs
                if est_preteur(description):
                    info = categoriser_transaction(description)
                    if info and info.get('preteur'):
                        nom = info['preteur']
                        if nom not in preteurs_detectes:
                            preteurs_detectes[nom] = {'nom': nom, 'count': 0, 'total': 0}
                        preteurs_detectes[nom]['count'] += 1
                        preteurs_detectes[nom]['total'] += abs(amount)

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
                "revenus": round(total_revenus, 2),
                "depenses": round(total_depenses, 2)
            },
            "preteurs_detectes": list(preteurs_detectes.values()),
            "alertes": [],
            "timestamp": datetime.now().isoformat()
        }

        # Ajouter alertes
        if len(preteurs_detectes) > 0:
            report_data["alertes"].append({
                "type": "preteurs",
                "niveau": "critical" if len(preteurs_detectes) >= 3 else "warning",
                "message": f"{len(preteurs_detectes)} prêteur(s) alternatif(s) détecté(s)"
            })
        if nsf_count > 0:
            report_data["alertes"].append({
                "type": "nsf",
                "niveau": "critical" if nsf_count >= 3 else "warning",
                "message": f"{nsf_count} transaction(s) NSF détectée(s)"
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
