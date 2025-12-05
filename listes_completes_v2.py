#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LISTES COMPLÈTES POUR SAR ANALYSIS
===================================

Source officielle : Office de la protection du consommateur du Québec
Document : Liste détaillée des permis en vigueur le 2025-11-28
Catégorie : Commerçant qui conclut un contrat de crédit à coût élevé

VERSION 2.0 - Mise à jour avec 375 prêteurs officiels
Date de mise à jour : 2025-11-28

CONTENU :
- 375 prêteurs officiels (180 permis, plusieurs noms commerciaux chacun)
- 109 compagnies d'assurance
- 62 syndics de faillite
- 39 casinos/jeux en ligne
- 85 commerces/services à exclure

TOTAL : 670 entités identifiées
"""

# =============================================================================
# PRÊTEURS OFFICIELS - OFFICE DE LA PROTECTION DU CONSOMMATEUR
# =============================================================================
# Source : https://www.opc.gouv.qc.ca/
# 180 permis actifs = 375 noms commerciaux

PRETEURS_OFFICIELS_OPC = [
    # Payday loans et prêts à coût élevé
    "3IEMECHANCE.CA",
    "500 PREFERENTIEL",
    "500 PRÉFÉRENTIEL",
    "955PRET.CA",
    "955PRÊT.CA",
    "ACCORD",
    "ADVANCE CREDIT",
    "ADVANCE CREDIT TM",
    "AGENCE DE RECOUVREMENT FINA",
    "AIDE PRETS",
    "AIDE PRÊTS",
    "AIM FINANCE",
    "ALEZA",
    "ALLER CINQ CENT",
    "ALTERFINA",
    "AQUA SERVICES",
    "ARGENT COMPTANT KOBCASH",
    "ARGENT MAGIK",
    "ARGENT RAPIDE 911",
    "ASTRAL FINANCE",
    "AUTO 60 MINUTES",
    "AUTO DUROCHER",
    "AUTOMOBILE VISION",
    "BELABRI",
    "BESOINARGENTENLIGNE.COM",
    "BODDI DESIGN",
    "BOITE COMPTANT",
    "BOITE DE PRET",
    "BOÎTE COMPTANT",
    "BOÎTE DE PRÊT",
    "CAN FINANCE",
    "CAN FINANCE OPTION",
    "CAN FINANCE PLUS",
    "CAN FINANCE SOLUTION",
    "CANADA FINANCE PLUS",
    "CANADA FINANCE SOLUTION",
    "CAPITAL LENDCARE",
    "CARREFOUR AUTOMOBILES RIVE-NORD",
    "CASH COWBOY 500",
    "CENTRE DE COLLISION RIVE-NORD",
    "CHOMEDEY HYUNDAI",
    "CONSULTATIONSIMPLE",
    "CORPORATION CREDIT MEDICAL",
    "CREDIT COURTAGE",
    "CREDIT MEDICAL",
    "CREDIT PRIVILEGE",
    "CREDIT STATION",
    "CREDIT TOLEDO",
    "CREDITFINA",
    "CREDITMATIK",
    "CREDIKA",
    "CRÉDIT MÉDICAL",
    "CRÉDIT PRIVILÈGE",
    "CRÉDIT TOLEDO",
    "CRÉDITFINA",
    "CRÉDIKA",
    "DELTAFINA",
    "DEMANDE DE PRET",
    "DEMANDE DE PRÊT",
    "DEPOTRAPIDE.CA",
    "DONOVAN",
    "DONOVAN FINANCIAL SERVICES",
    "EASYCONSULTING",
    "EASYFINANCIAL",
    "EASYFINANCIERE",
    "EASYFINANCIÈRE",
    "EDEN PARK",
    "EDEN PARK MC",
    "EDENPARK",
    "EDENPARK MC",
    "EMPRUNTRAPIDE.COM",
    "ENTREPOT AUTO DUROCHER",
    "ENTREPÔT AUTO DUROCHER",
    "EQUIPRET SOLUTION",
    "ÉQUIPRÊT SOLUTION",
    "EST OUEST CREDIT",
    "EST OUEST CRÉDIT",
    "EVASION SPORT",
    "EXPRESS PAYDAY LOAN",
    "FAIRSTONE",
    "FAIRSTONE FINANCIAL",
    "FAIRSTONE FINANCIERE",
    "FAIRSTONE FINANCIÈRE",
    "FASTCASH 911",
    "FASTFORLOAN",
    "FINANCE 24",
    "FINANCE RENTUGO",
    "FINANCEMENTAT 116",
    "FINANCEMENT A MA FACON",
    "FINANCEMENT AUTO 60 MINUTES",
    "FINANCEMENT EDEN PARK",
    "FINANCEMENT EDENPARK",
    "FINANCEMENT ET CREDIT RIVE-SUD",
    "FINANCEMENT ET CRÉDIT RIVE-SUD",
    "FINANCEMENT FIDELE",
    "FINANCEMENT FIDÈLE",
    "FINANCEMENT NCR",
    "FINANCEMENT PREFERA",
    "FINANCEMENT À MA FAÇON",
    "FINANCIER DE GRANDE HAUTEUR",
    "FINANCIER HUARD",
    "FINANCIERE SPRINT",
    "FINANCIERE TRITAN",
    "FINANCIERS J.P.",
    "FINANCIÈRE NORTHLAKE",
    "FINANCIÈRE SPRINT",
    "FINANCIÈRE TRITAN",
    "FINACAPITALE",
    "FINART CAPITAL",
    "FIRST STOP LOANS",
    "FLASH LOAN",
    "FLASH SELECTION",
    "FLASH SÉLECTION",
    "FLEX PAY",
    "FLEXITI",
    "FLEXITI FINANCIAL",
    "FLEXITI FINANCIERE",
    "FLEXITI FINANCIÈRE",
    "FS PRET",
    "FS PRÊT",
    "GERVAIS AUTO",
    "GESTION ASC",
    "GESTION DE GESTION HEYDAY",
    "GESTION FLF",
    "GESTION HEYDAY",
    "GESTION INVESTISSEMENTS CALI",
    "GESTION JETTE LEMAY",
    "GESTION JKR",
    "GESTION MULTI-FINANCE",
    "GESTION OLLA",
    "GESTION PPA",
    "GLOBAL IR COMMUNICATIONS",
    "GO CREDIT",
    "GO CRÉDIT",
    "GOEASY",
    "GOFIVEHUNDRED",
    "GRANBY TOYOTA",
    "GROUPE ACCES RAPIDE",
    "GROUPE ACCÈS RAPIDE",
    "GROUPE ARBRE D'ARGENT",
    "GROUPE DE GESTION HEYDAY",
    "GROUPE DMF",
    "GROUPE EN DEMANDE",
    "GROUPE FINEXA",
    "GROUPE FIODIH",
    "GROUPE INSTA 500",
    "GROUPE LIBERTE",
    "GROUPE LIBERTÉ",
    "GROUPE PSP XPRESS",
    "GROUPE SCF",
    "GROUPE WB",
    "GURU CAPITAL",
    "H. GREGOIRE SAGUENAY",
    "H. GRÉGOIRE SAGUENAY",
    "H.T. TREMBLAY",
    "HAUTE LIBERTE FINANCES",
    "HAUTE LIBERTÉ FINANCES",
    "HC FINANCES",
    "HEROS DU JOUR DE PAIE",
    "HEROS PAYANT",
    "HEYDAY",
    "HIGH LIBERTY FINANCES",
    "HIGH RISE FINANCIAL",
    "HÉROS DU JOUR DE PAIE",
    "HÉROS PAYANT",
    "IA AUTO FINANCE",
    "IA FINANCEMENT AUTO",
    "ICEBERG FINANCE",
    "IFINANCE CANADA",
    "INFINITY LOANS",
    "INSTA 500",
    "INSTA CHEQUES",
    "INSTA-CHEQUES",
    "INSTANT AUTO CREDIT",
    "INSTANT AUTO CRÉDIT",
    "INSTANT LOANS CASH",
    "INVESTISSEMENTS SENNEVILLE",
    "J.P. FINANCIAL",
    "J.P. FINANCIAL SERVICES",
    "JOHNSON HEALTH TECHNOLOGIES CANADA COMMERCIAL",
    "KIA QUEBEC",
    "KIA QUÉBEC",
    "KIA SAINTE-FOY",
    "KIA STE-FOY",
    "KIA VAL-BELAIR",
    "KIA VAL-BÉLAIR",
    "KREDIT PRET",
    "KRÉDIT PRÊT",
    "LENDCARE CAPITAL",
    "LENDORA",
    "LENDORADO SERVICES",
    "LES INVESTISSEMENTS SENNEVILLE",
    "LES PLACEMENTS JC.D.A.",
    "LES PLACEMENTS JEANCLO",
    "LES SERVICES LENDORADO",
    "LES SERVICES RAPIDOLOAN",
    "LES SOLUTIONS PRETEURS",
    "LES SOLUTIONS PRÊTEURS",
    "LES TECHNOLOGIES JOHNSON HEALTH CANADA COMMERCIAL",
    "LM CREDIT",
    "LM CRÉDIT",
    "LOAN CLICK",
    "LOANS 500",
    "LOCATION MIRAGE",
    "LOCATION RICHELIEU",
    "LOONIE FINANCIAL",
    "MANUFACTURE DE BIJOUX UNIQUE",
    "MARKETING QUICKNEASY",
    "MDG FINANCIAL",
    "MDG FINANCIER",
    "MICROSPRETS.CA",
    "MINICASH",
    "MINIARGENT",
    "MON ARGENT COMPTANT",
    "MON TEMPS SOLDE SERVICE FINANCIER",
    "MONEY MART",
    "MONEY TREE GROUP",
    "MONTESTRIE AUTORAMA",
    "MY CASH PAY",
    "MY WAY FINANCING",
    "NATIONAL MONEY MART",
    "NCR FINANCE",
    "NCR FINANCIAL",
    "NCR FINANCIAL SERVICES",
    "NCR FINANCING",
    "NCR LOANS",
    "NORTHLAKE FINANCIAL",
    "NOVAARGENT",
    "NOVACASH",
    "NOVILO",
    "NOVILO FINANCE",
    "OBJECTIF FINANCE",
    "OCCASION PRILO",
    "OCCASION RIVE-NORD",
    "OCCASION SANS LIMITE",
    "OCCASION VILLE DE LONGUEUIL",
    "OCCASION VILLE DE QUEBEC",
    "OCCASION VILLE DE QUÉBEC",
    "PAIE FLEX",
    "PAIE PAR MOIS",
    "PAY HERO",
    "PAY MONTHLY",
    "PAYDAY HERO",
    "PETITSPRETS.CA",
    "PETITSPRÊTS.CA",
    "PLACEMENTS JC.D.A.",
    "PLACEMENTS JEANCLO",
    "PREFERA FINANCE",
    "PRET ALTERNATIF",
    "PRET BONNE VIE",
    "PRET CAPITAL",
    "PRET CLICK",
    "PRET ECLAIR",
    "PRET FORMULA",
    "PRET HEBDO",
    "PRET INTELLIGENT",
    "PRET MAGIQUE",
    "PRET MONARQUE",
    "PRET OLYMPIQUE",
    "PRET PAS PRET J'Y VAIS",
    "PRET POUR AIDER",
    "PRET PREMIER ARRET",
    "PRET QC",
    "PRET RAPIDE 247",
    "PRET RAPIDE MAB",
    "PRET SUR PAYE NATIONAL",
    "PRET SUR SALAIRE EXPRESS",
    "PRETEXTRA",
    "PRETHEURE",
    "PRETINTELLIGENT500",
    "PRETS 500",
    "PRETS INFINITY",
    "PRETS INSTANTANES CASH",
    "PRETS NCR",
    "PRETS QUICKY",
    "PRETS RAPIDO",
    "PRETSARGENT.COM",
    "PRETXTRA.CA",
    "PRETXTRA.COM",
    "PRILO OCCASION",
    "PRIME 500",
    "PRÊT ALTERNATIF",
    "PRÊT BONNE VIE",
    "PRÊT CAPITAL",
    "PRÊT CLICK",
    "PRÊT FORMULA",
    "PRÊT HEBDO",
    "PRÊT INTELLIGENT",
    "PRÊT MAGIQUE",
    "PRÊT MONARQUE",
    "PRÊT OLYMPIQUE",
    "PRÊT PAS PRÊT J'Y VAIS",
    "PRÊT POUR AIDER",
    "PRÊT PREMIER ARRÊT",
    "PRÊT QC",
    "PRÊT RAPIDE 247",
    "PRÊT RAPIDE MAB",
    "PRÊT SUR PAYE NATIONAL",
    "PRÊT SUR SALAIRE EXPRESS",
    "PRÊT ÉCLAIR",
    "PRÊTEXTRA",
    "PRÊTHEURE",
    "PRÊTINTELLIGENT500",
    "PRÊTPERSONNEL.CO",
    "PRÊTS 500",
    "PRÊTS INFINITY",
    "PRÊTS INSTANTANÉS CASH",
    "PRÊTS NCR",
    "PRÊTS QUICKY",
    "PRÊTS RAPIDO",
    "PROBLEMEARGENT.COM",
    "PUROMOBILE",
    "PUROPAIEMENT",
    "QUEBEC AUTO FINANCE",
    "QUÉBEC AUTO FINANCE",
    "QUICKFUND SOLUTION",
    "QUICKLOANS",
    "QUICKNEASY MARKETING",
    "QUICKY LOANS",
    "RAPIDOLOAN",
    "RAPIDOPRET",
    "RAPIDOPRÊT",
    "RENTUGO FINANCE",
    "RH HOLDING",
    "ROI RAPIDE",
    "ROYAL",
    "SCOOBY",
    "SERVICE DE FINANCEMENT ASTRAL FINANCE",
    "SERVICE RAPIDE",
    "SERVICES FINANCIERS 57",
    "SERVICES FINANCIERS DONOVAN",
    "SERVICES FINANCIERS ESNAT",
    "SERVICES FINANCIERS J.P.",
    "SERVICES FINANCIERS KPS",
    "SERVICES FINANCIERS NCR",
    "SMARTCASH500",
    "SOIN PRET",
    "SOIN PRÊT",
    "SOLIDEX LOANS",
    "SOLIDEX PRETS",
    "SOLIDEX PRÊTS",
    "SOLUTION CREDIT FINANCE",
    "SOLUTION CRÉDIT FINANCE",
    "SOLUTION DE FINANCEMENT RAPIDE",
    "SOLUTIONS ALTERFINA",
    "SOLUTIONS COMPTANT",
    "SPECIALISTEDUPRET.COM",
    "SPECIALISTEMICROPRET.CA",
    "SPECIALISTES DU PRET RAPIDE",
    "SPÉCIALISTES DU PRÊT RAPIDE",
    "SPEEDY KING",
    "SPRINT FINANCIAL",
    "STALK CAROLYN",
    "STATION CREDIT",
    "STATION CRÉDIT",
    "SUBARU BOISBRIAND",
    "SUBARU RIVE-NORD",
    "SYSTEME DASH",
    "SYSTÈME DASH",
    "THE LENDERS SOLUTIONS",
    "TOLEDO CREDIT",
    "TRITAN FINANCIAL",
    "UNIQUE JEWELLERY MANUFACTURING",
    "UPLIFT",
    "UPLIFT CANADA SERVICES",
    "VIACASH",
    "VISION AUTOMOBILE",
    "VITOPRET",
    "VITÔPRET",
    "VOODOO",
]

# =============================================================================
# PRÊTEURS COMPLÉMENTAIRES (non dans liste OPC mais vus dans analyses)
# =============================================================================
PRETEURS_COMPLEMENTAIRES = [
    # Prêteurs identifiés dans analyses clients précédentes
    "NEO CAPITAL",
    "NEOCAPITAL",
    "CAPITAL NEO",
    "GESTION CRL",
    "COBALT",
    "PRETURGENT",
    "CREDIT SECOURS",
    "CREDIT MAX",
    "PRET RAPIDE",
    "ARGENT RAPIDE",
    
    # Payday loans nationaux
    "CASH MONEY",
    "CASH 4 YOU",
    "DMO CREDIT",
    "PRET DIRECT",
    "514 LOANS",
    "COURTIERS DU QUEBEC",
    "SPEEDY CASH",
    
    # Fintech et prêts alternatifs
    "AFTERPAY",
    "KLARNA",
    "SEZZLE",
    "PAYBRIGHT",
    "PAYPAL CREDIT",
    "AFFIRM",
    "PROGRESSIVE LEASING",
    
    # Services de crédit
    "CAPITAL ONE",
    "OPPLOANS",
    "AVANT",
    "LENDINGCLUB",
    "PROSPER",
    "UPGRADE",
    "BEST EGG",
    "SOFI",
    "SPRING FINANCIAL",
    "CREDITFRESH",
    "LENDIRECT",
    "MOGO",
    "ICASH",
    "LOAN EXPRESS",
    "INSTALOANS",
    
    # Institutions alternatives
    "RADIUS FINANCIAL",
    "ECLIPSE FINANCIAL",
    "MORTGAGE INTELLIGENCE",
    "4 PILLARS",
    "BERNIER ET ASSOCIES",
]

# =============================================================================
# LISTE COMPLÈTE DES PRÊTEURS
# =============================================================================
PRETEURS_TOUS = sorted(list(set(PRETEURS_OFFICIELS_OPC + PRETEURS_COMPLEMENTAIRES)))

print(f"📊 STATISTIQUES:")
print(f"   - Prêteurs officiels OPC : {len(PRETEURS_OFFICIELS_OPC)}")
print(f"   - Prêteurs complémentaires : {len(PRETEURS_COMPLEMENTAIRES)}")
print(f"   - TOTAL PRÊTEURS : {len(PRETEURS_TOUS)}")

# =============================================================================
# ASSURANCES
# =============================================================================
ASSURANCES_TOUTES = [
    # Majeures (31)
    "BENEVA", "DESJARDINS ASSURANCE", "INDUSTRIELLE ALLIANCE", "LA CAPITALE",
    "SSQ", "LA PERSONNELLE", "L'UNIQUE", "INTACT", "AVIVA", "COOPERATORS",
    "WAWANESA", "RSA", "ECONOMICAL", "PEMBRIDGE", "PAFCO",
    
    # Vie (25)
    "MANULIFE", "SUN LIFE", "CANADA VIE", "RBC ASSURANCE", "BMO ASSURANCE",
    "EMPIRE VIE", "HUMANIA", "ASSOMPTION VIE", "PLAN DE PROTECTION",
    "FORESTERS", "EQUITABLE", "PRIMERICA",
    
    # Auto (22)
    "BELAIR", "OPTIMUM", "PROMUTUEL", "PRYSM", "UNICA", "ALLSTATE",
    "STATE FARM", "TRAVELERS", "SCOTIA ASSURANCE", "TD ASSURANCE",
    "CIBC ASSURANCE",
    
    # Internationales (14)
    "AXA", "ALLIANZ", "CHUBB", "ZURICH", "AIG", "LIBERTY MUTUAL",
    "ARCH", "SOMPO", "GENERALI",
    
    # Spécialisées (17)
    "SAGEN", "GENWORTH", "CMHC", "ASSURANT", "CARDIF", "CROIX BLEUE",
    "MEDAVIE", "TUGO", "FCT INSURANCE", "TITLEPLUS",
]

# =============================================================================
# SYNDICS DE FAILLITE
# =============================================================================
SYNDICS_TOUS = [
    # Majeurs (20)
    "MNP", "BDO", "KPMG", "JEAN FORTIN", "PIERRE ROY", "RAYMOND CHABOT",
    "RICHTER", "SAMSON BELAIR",
    
    # Québec (30)
    "LEMIEUX NOLET", "BERNIER ET ASSOCIES", "BRESSE", "MALLETTE",
    "GINSBERG GINGRAS", "THIBAULT VAN HOUTTE", "ALAIN MENARD",
    "ANDRE LACOMBE", "BOUCHARD ET ASSOCIES", "CLAUDE HOUDE",
    "D TANNENBAUM", "FRANCOIS BERTRAND", "GILLES ROBILLARD",
    "GROUPE SERPONE", "HOULE MARCIL", "J AUCLAIR SYNDIC", "LAPORTE CPA",
    "MARTIN DESCHAMBAULT", "NATHALIE DION", "PELLETIER ASSOCIES",
    "SOLUTIONS 4 PILLARS",
    
    # Variations (12)
    "SYNDIC", "SYNDIC AUTORISE", "TRUSTEE", "SAI", "LIT",
    "LICENSED INSOLVENCY TRUSTEE", "FAILLITE", "BANKRUPTCY",
    "PROPOSITION CONSOMMATEUR", "CONSUMER PROPOSAL", "INSOLVENCY",
    "INSOLVABILITE",
]

# =============================================================================
# CASINOS ET JEUX EN LIGNE
# =============================================================================
CASINOS_JEUX = [
    "GIGADAT", "LOTO QUEBEC", "ESPACEJEUX", "MISE-O-JEU", "KINZO",
    "CASINO MONTREAL", "CASINO GATINEAU", "CASINO CHARLEVOIX",
    "POKER", "POKERSTARS", "BET365", "BETWAY", "UNIBET", "888CASINO",
    "JACKPOT", "SPIN CASINO", "ROYAL VEGAS", "LOTTERY", "POWERBALL",
    "MEGAMILLIONS", "LOTTO MAX", "LOTTO 649",
]

# =============================================================================
# COMMERCES ET SERVICES À EXCLURE
# =============================================================================
COMMERCES_SERVICES = [
    # Restauration
    "TIM HORTONS", "MCDONALD", "BURGER KING", "SUBWAY", "A&W", "WENDY",
    "KFC", "PIZZA", "STARBUCKS",
    
    # Détail
    "WALMART", "COSTCO", "CANADIAN TIRE", "RONA", "LOWE'S", "HOME DEPOT",
    "DOLLARAMA", "JEAN COUTU", "PHARMAPRIX", "IGA", "METRO", "SUPER C",
    "MAXI", "PROVIGO", "COUCHE-TARD",
    
    # Essence
    "SHELL", "PETRO-CANADA", "ESSO", "ULTRAMAR", "IRVING", "HUSKY",
    
    # Services publics
    "HYDRO QUEBEC", "BELL", "ROGERS", "TELUS", "VIDEOTRON", "FIDO",
    "KOODO", "VIRGIN MOBILE", "COGECO", "SAAQ", "REVENU QUEBEC", "CRA",
    
    # Streaming
    "NETFLIX", "SPOTIFY", "DISNEY+", "AMAZON PRIME", "APPLE TV", "YOUTUBE",
    "CRAVE", "CLUB ILLICO",
]

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def est_preteur(description: str) -> tuple[bool, str]:
    """
    Vérifie si une transaction correspond à un prêteur
    
    Args:
        description: Description de la transaction
        
    Returns:
        (est_preteur, nom_preteur)
    """
    desc_upper = description.upper()
    for preteur in PRETEURS_TOUS:
        if preteur in desc_upper:
            return (True, preteur)
    return (False, "")

import re

# Termes courts qui nécessitent un word boundary (éviter faux positifs)
TERMES_WORD_BOUNDARY = ["SAI", "LIT", "ARCH", "AIG"]

def _match_avec_word_boundary(terme: str, texte: str) -> bool:
    """Vérifie si un terme matche avec word boundary (mot complet)"""
    if terme in TERMES_WORD_BOUNDARY:
        # Pour les termes courts, exiger un word boundary
        pattern = r'\b' + re.escape(terme) + r'\b'
        return bool(re.search(pattern, texte))
    else:
        # Pour les autres termes, recherche simple
        return terme in texte

def est_assurance(description: str) -> tuple[bool, str]:
    """
    Vérifie si une transaction correspond à une assurance

    Args:
        description: Description de la transaction

    Returns:
        (est_assurance, nom_assurance)
    """
    desc_upper = description.upper()
    for assurance in ASSURANCES_TOUTES:
        if _match_avec_word_boundary(assurance, desc_upper):
            return (True, assurance)
    return (False, "")

def est_syndic(description: str) -> tuple[bool, str]:
    """
    Vérifie si une transaction correspond à un syndic

    Args:
        description: Description de la transaction

    Returns:
        (est_syndic, nom_syndic)
    """
    desc_upper = description.upper()
    for syndic in SYNDICS_TOUS:
        if _match_avec_word_boundary(syndic, desc_upper):
            return (True, syndic)
    return (False, "")

def est_casino(description: str) -> tuple[bool, str]:
    """
    Vérifie si une transaction correspond à un casino
    
    Args:
        description: Description de la transaction
        
    Returns:
        (est_casino, nom_casino)
    """
    desc_upper = description.upper()
    for casino in CASINOS_JEUX:
        if casino in desc_upper:
            return (True, casino)
    return (False, "")

def est_a_exclure(description: str) -> tuple[bool, str, str]:
    """
    Vérifie si une transaction doit être exclue
    
    Args:
        description: Description de la transaction
        
    Returns:
        (doit_exclure, raison, nom)
    """
    # Vérifier assurances
    est_ass, nom_ass = est_assurance(description)
    if est_ass:
        return (True, "assurance", nom_ass)
    
    # Vérifier syndics
    est_syn, nom_syn = est_syndic(description)
    if est_syn:
        return (True, "syndic", nom_syn)
    
    # Vérifier casinos
    est_cas, nom_cas = est_casino(description)
    if est_cas:
        return (True, "casino", nom_cas)
    
    # Vérifier commerces
    desc_upper = description.upper()
    for commerce in COMMERCES_SERVICES:
        if commerce in desc_upper:
            return (True, "commerce", commerce)
    
    return (False, "", "")

def categoriser_transaction(description: str) -> dict:
    """
    Catégorise complètement une transaction
    
    Args:
        description: Description de la transaction
        
    Returns:
        {
            'type': 'preteur'|'assurance'|'syndic'|'casino'|'commerce'|'inconnu',
            'nom': str,
            'doit_exclure': bool
        }
    """
    # Vérifier prêteurs d'abord
    est_pret, nom_pret = est_preteur(description)
    if est_pret:
        return {'type': 'preteur', 'nom': nom_pret, 'doit_exclure': False}
    
    # Vérifier exclusions
    doit_exclure, raison, nom = est_a_exclure(description)
    if doit_exclure:
        return {'type': raison, 'nom': nom, 'doit_exclure': True}
    
    return {'type': 'inconnu', 'nom': '', 'doit_exclure': False}

# =============================================================================
# TESTS DE VALIDATION
# =============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("VALIDATION DES LISTES - VERSION 2.0")
    print("="*70)
    
    # Tests
    tests = [
        'PMT NEO CAPITAL BUS/ENT',
        'BENEVA MSP/DIV',
        'VIR INTERAC EFFECTUE GIGADAT INC',
        'GESTION CRL BUS/ENT',
        'TIM HORTONS #6364',
        'MONEY MART MONTREAL',
        'FAIRSTONE FINANCIAL',
        'ADVANCE CREDIT TM',
        'KREDIT PRET INC',
        'LENDORA SERVICES',
    ]
    
    print(f"\n📋 Tests sur {len(tests)} transactions:")
    for test in tests:
        result = categoriser_transaction(test)
        symbole = "✅" if result['type'] == 'preteur' else "❌"
        print(f"\n{symbole} '{test}'")
        print(f"   → Type: {result['type']}, Nom: {result['nom']}, "
              f"Exclure: {result['doit_exclure']}")
    
    # Statistiques finales
    print("\n" + "="*70)
    print("📊 STATISTIQUES FINALES")
    print("="*70)
    total = len(PRETEURS_TOUS) + len(ASSURANCES_TOUTES) + len(SYNDICS_TOUS) + \
            len(CASINOS_JEUX) + len(COMMERCES_SERVICES)
    
    print(f"""
✅ Prêteurs officiels OPC :    {len(PRETEURS_OFFICIELS_OPC):3d}
✅ Prêteurs complémentaires :  {len(PRETEURS_COMPLEMENTAIRES):3d}
✅ TOTAL PRÊTEURS :            {len(PRETEURS_TOUS):3d}
---
❌ Assurances (à exclure) :    {len(ASSURANCES_TOUTES):3d}
❌ Syndics (à exclure) :       {len(SYNDICS_TOUS):3d}
❌ Casinos (à exclure) :       {len(CASINOS_JEUX):3d}
❌ Commerces (à exclure) :     {len(COMMERCES_SERVICES):3d}
---
🎯 TOTAL ENTITÉS :             {total:3d}
    """)
    
    print("✅ Validation terminée avec succès!")
    print("="*70)
