"""
Base de connaissances curée — Règlement (UE) 2024/1689 (AI Act) + RGPD (2016/679).

Sources officielles :
- AI Act : https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32024R1689
- RGPD  : https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679
- CNIL (autorité nationale IA en France) : https://www.cnil.fr

Les mots-clés sont stockés en minuscules et SANS accents (le serveur normalise
le texte d'entrée de la même façon avant comparaison).

⚠️ Outil d'information et d'orientation réglementaire — ne constitue pas un
conseil juridique. Vérifier auprès des textes officiels et d'un conseil qualifié.
"""

AI_ACT_URL = "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32024R1689"
GDPR_URL = "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679"
CNIL_URL = "https://www.cnil.fr"

DISCLAIMER = (
    "Information et orientation reglementaire, generee a partir de sources "
    "officielles (AI Act, RGPD, CNIL). Ne constitue pas un conseil juridique."
)

# --------------------------------------------------------------------------
# Niveaux de risque (AI Act)
# --------------------------------------------------------------------------
RISK_TIERS = {
    "prohibited": {
        "label": "Risque inacceptable (pratique interdite)",
        "article": "Article 5",
        "applicable_since": "2025-02-02",
        "summary": "Pratique interdite dans l'UE. Le systeme ne peut pas etre mis "
                   "sur le marche ni utilise.",
    },
    "high": {
        "label": "Haut risque",
        "article": "Article 6 + Annexe III (et Annexe I pour la securite produit)",
        "applicable_since": "2026-08-02",
        "summary": "Autorise mais soumis aux obligations les plus strictes "
                   "(gestion des risques, donnees, documentation, controle humain, "
                   "evaluation de conformite, marquage CE).",
    },
    "limited": {
        "label": "Risque limite (obligations de transparence)",
        "article": "Article 50",
        "applicable_since": "2026-08-02",
        "summary": "Obligations de transparence : informer l'utilisateur qu'il "
                   "interagit avec une IA et marquer les contenus synthetiques.",
    },
    "minimal": {
        "label": "Risque minimal",
        "article": "—",
        "applicable_since": "—",
        "summary": "Pas d'obligation specifique au titre de l'AI Act. Codes de "
                   "conduite volontaires encourages.",
    },
}

# --------------------------------------------------------------------------
# Pratiques interdites — Article 5
# --------------------------------------------------------------------------
PROHIBITED_PRACTICES = [
    {
        "id": "manipulation",
        "label": "Techniques subliminales ou manipulatrices causant un prejudice",
        "article": "Article 5(1)(a)",
        "keywords": ["subliminal", "manipulation", "manipulat", "technique trompeuse",
                     "deceptive technique", "manipuler le comportement"],
    },
    {
        "id": "vulnerabilites",
        "label": "Exploitation des vulnerabilites (age, handicap, situation sociale)",
        "article": "Article 5(1)(b)",
        "keywords": ["exploiter la vulnerabilite", "vulnerabilite", "exploit vulnerab",
                     "personnes vulnerables", "exploiter le handicap"],
    },
    {
        "id": "notation_sociale",
        "label": "Notation sociale (social scoring) menant a un traitement defavorable",
        "article": "Article 5(1)(c)",
        "keywords": ["notation sociale", "social scoring", "social score",
                     "score citoyen", "scoring social", "note de citoyennete"],
    },
    {
        "id": "police_predictive",
        "label": "Police predictive fondee uniquement sur le profilage",
        "article": "Article 5(1)(d)",
        "keywords": ["police predictive", "predictive policing", "predire un crime",
                     "predict crime", "risque de commettre une infraction",
                     "profilage penal"],
    },
    {
        "id": "moisson_faciale",
        "label": "Moissonnage non cible d'images faciales pour bases de reconnaissance",
        "article": "Article 5(1)(e)",
        "keywords": ["moissonnage d'images", "scraping facial", "untargeted scraping",
                     "base de reconnaissance faciale", "facial recognition database",
                     "aspirer des visages"],
    },
    {
        "id": "emotions_travail_ecole",
        "label": "Reconnaissance des emotions au travail ou dans l'education",
        "article": "Article 5(1)(f)",
        "keywords": ["reconnaissance des emotions au travail", "emotions des employes",
                     "emotion recognition workplace", "emotions en classe",
                     "emotions des eleves", "classroom emotion"],
    },
    {
        "id": "categorisation_sensible",
        "label": "Categorisation biometrique inferant des attributs sensibles",
        "article": "Article 5(1)(g)",
        "keywords": ["categorisation biometrique", "biometric categorization",
                     "inferer l'origine", "inferer l'orientation sexuelle",
                     "inferer les opinions politiques", "inferer la religion"],
    },
    {
        "id": "biometrie_temps_reel",
        "label": "Identification biometrique a distance en temps reel dans l'espace "
                 "public a des fins repressives (sous reserve d'exceptions)",
        "article": "Article 5(1)(h)",
        "keywords": ["identification biometrique a distance en temps reel",
                     "real-time remote biometric", "reconnaissance faciale en direct",
                     "live facial recognition", "temps reel espace public"],
    },
]

# --------------------------------------------------------------------------
# Domaines a haut risque — Annexe III
# --------------------------------------------------------------------------
HIGH_RISK_DOMAINS = [
    {
        "id": "biometrie",
        "label": "Biometrie (identification/categorisation, hors cas interdits)",
        "annex": "Annexe III §1",
        "keywords": ["biometrie", "biometric", "empreinte", "reconnaissance faciale",
                     "identification biometrique"],
    },
    {
        "id": "infrastructures",
        "label": "Infrastructures critiques (composants de securite)",
        "annex": "Annexe III §2",
        "keywords": ["infrastructure critique", "critical infrastructure",
                     "reseau electrique", "gestion du trafic", "traffic safety",
                     "approvisionnement en eau", "gaz", "chauffage"],
    },
    {
        "id": "education",
        "label": "Education et formation professionnelle",
        "annex": "Annexe III §3",
        "keywords": ["education", "formation professionnelle", "admission",
                     "examen", "proctoring", "surveillance d'examen",
                     "notation des eleves", "student assessment",
                     "vocational training"],
    },
    {
        "id": "emploi",
        "label": "Emploi, gestion des travailleurs, acces a l'emploi independant",
        "annex": "Annexe III §4",
        "keywords": ["recrutement", "recruitment", "embauche", "tri de cv",
                     "tri des cv", "candidat", "tri de candidatures", "cv screening",
                     "promotion", "licenciement", "evaluation des employes",
                     "gestion des travailleurs", "worker management",
                     "surveillance des employes"],
    },
    {
        "id": "services_essentiels",
        "label": "Acces aux services essentiels (credit, assurance, aide sociale)",
        "annex": "Annexe III §5",
        "keywords": ["credit", "creditworthiness", "score de credit", "solvabilite",
                     "assurance", "tarification assurance", "insurance pricing",
                     "prestations sociales", "aide sociale", "welfare",
                     "eligibilite aux prestations", "services d'urgence",
                     "regulation des secours"],
    },
    {
        "id": "forces_ordre",
        "label": "Forces de l'ordre",
        "annex": "Annexe III §6",
        "keywords": ["force de l'ordre", "law enforcement", "police",
                     "evaluation du risque de recidive", "polygraphe",
                     "evaluation de preuves", "enquete penale"],
    },
    {
        "id": "migration",
        "label": "Migration, asile et controle des frontieres",
        "annex": "Annexe III §7",
        "keywords": ["migration", "asile", "asylum", "visa", "frontiere",
                     "border control", "immigration", "demande d'asile"],
    },
    {
        "id": "justice",
        "label": "Administration de la justice et processus democratiques",
        "annex": "Annexe III §8",
        "keywords": ["administration de la justice", "judiciaire", "tribunal",
                     "judicial", "elections", "processus democratique",
                     "influencer le vote"],
    },
]

# --------------------------------------------------------------------------
# Obligations de transparence — Article 50 (risque limite)
# --------------------------------------------------------------------------
TRANSPARENCY_OBLIGATIONS = [
    {
        "id": "interaction_ia",
        "label": "Systeme interagissant avec des personnes (chatbot, assistant)",
        "requirement": "Informer clairement l'utilisateur qu'il interagit avec une IA.",
        "article": "Article 50(1)",
        "keywords": ["chatbot", "agent conversationnel", "assistant virtuel",
                     "conversationnel", "interagit avec", "interacts with humans",
                     "dialogue", "callbot", "voicebot", "service client",
                     "relation client", "repond aux clients"],
    },
    {
        "id": "contenu_synthetique",
        "label": "Generation de contenu de synthese (texte, image, audio, video)",
        "requirement": "Marquer le contenu comme genere/manipule par IA "
                       "(format lisible par machine).",
        "article": "Article 50(2)",
        "keywords": ["genere du contenu", "generative", "generatif", "generer des images",
                     "generer du texte", "synthese vocale", "synthetic content",
                     "generate images", "generate text", "contenu de synthese",
                     "generateur", "generation de contenu", "generation d'images",
                     "de synthese", "genere"],
    },
    {
        "id": "deepfake",
        "label": "Hypertrucage (deepfake)",
        "requirement": "Indiquer que le contenu a ete genere ou manipule artificiellement.",
        "article": "Article 50(4)",
        "keywords": ["deepfake", "hypertrucage", "visage synthetique",
                     "clonage vocal", "voice clone", "video truquee"],
    },
    {
        "id": "emotions_categorisation",
        "label": "Reconnaissance des emotions / categorisation biometrique (hors interdit)",
        "requirement": "Informer les personnes exposees au fonctionnement du systeme.",
        "article": "Article 50(3)",
        "keywords": ["reconnaissance des emotions", "emotion recognition",
                     "categorisation biometrique"],
    },
]

# --------------------------------------------------------------------------
# Modeles a usage general (GPAI) — Chapitre V
# --------------------------------------------------------------------------
GPAI_KEYWORDS = ["modele de fondation", "foundation model", "modele a usage general",
                 "general-purpose ai", "general purpose ai", "gpai", "llm",
                 "grand modele de langage", "large language model",
                 "modele generatif entraine", "modele pre-entraine"]

GPAI_OBLIGATIONS = {
    "applicable_since": "2025-08-02",
    "base": [
        "Documentation technique du modele (Article 53).",
        "Informations et documentation pour les fournisseurs en aval.",
        "Politique de respect du droit d'auteur de l'Union.",
        "Resume suffisamment detaille des contenus d'entrainement.",
    ],
    "systemic_risk": [
        "Evaluation du modele (y compris tests contradictoires).",
        "Evaluation et attenuation des risques systemiques (Article 55).",
        "Signalement des incidents graves ; cybersecurite du modele.",
    ],
    "legacy_note": "Les modeles GPAI mis sur le marche avant le 2 aout 2025 doivent "
                   "se mettre en conformite au plus tard le 2 aout 2027.",
}

# --------------------------------------------------------------------------
# Calendrier d'application (verifie)
# --------------------------------------------------------------------------
TIMELINE = [
    {"date": "2024-08-01", "milestone": "Entree en vigueur du reglement",
     "scope": "Debut du compte a rebours des echeances."},
    {"date": "2025-02-02", "milestone": "Pratiques interdites + litteratie IA",
     "scope": "Application de l'Article 5 (interdictions) et de l'Article 4 "
              "(obligation de litteratie en IA)."},
    {"date": "2025-08-02", "milestone": "Modeles GPAI + gouvernance",
     "scope": "Obligations des fournisseurs de modeles a usage general, mise en "
              "place des autorites et du regime de sanctions."},
    {"date": "2026-08-02", "milestone": "Application generale",
     "scope": "Systemes a HAUT RISQUE (Annexe III), transparence (Article 50), "
              "obligations des deployeurs et pouvoirs de sanction. Echeance majeure."},
    {"date": "2027-08-02", "milestone": "Haut risque Annexe I + GPAI historiques",
     "scope": "Systemes a haut risque lies a la securite des produits (Annexe I) "
              "et mise en conformite des modeles GPAI anterieurs au 2 aout 2025."},
]

# --------------------------------------------------------------------------
# Sanctions
# --------------------------------------------------------------------------
PENALTIES = [
    {"infraction": "Pratique interdite (Article 5)",
     "max": "35 000 000 EUR ou 7 % du chiffre d'affaires annuel mondial (le plus eleve)"},
    {"infraction": "Autres obligations (dont haut risque, deployeurs, transparence)",
     "max": "15 000 000 EUR ou 3 % du chiffre d'affaires annuel mondial"},
    {"infraction": "Manquements des fournisseurs de modeles GPAI",
     "max": "15 000 000 EUR ou 3 % du chiffre d'affaires annuel mondial"},
    {"infraction": "Informations inexactes fournies aux autorites",
     "max": "7 500 000 EUR ou 1 % du chiffre d'affaires annuel mondial"},
    {"note": "Pour les PME et jeunes pousses, les plafonds correspondent au montant "
             "le plus BAS des deux."},
]

# --------------------------------------------------------------------------
# Obligations par role et par niveau
# --------------------------------------------------------------------------
OBLIGATIONS = {
    ("provider", "high"): [
        "Systeme de gestion des risques (Article 9).",
        "Gouvernance des donnees et jeux de donnees de qualite (Article 10).",
        "Documentation technique (Article 11) et journalisation (Article 12).",
        "Transparence et notice d'utilisation (Article 13).",
        "Controle humain effectif (Article 14).",
        "Exactitude, robustesse et cybersecurite (Article 15).",
        "Systeme de gestion de la qualite (Article 17).",
        "Evaluation de la conformite et marquage CE (Article 43).",
        "Enregistrement dans la base de donnees de l'UE (Article 49).",
    ],
    ("deployer", "high"): [
        "Utiliser le systeme conformement a la notice (Article 26).",
        "Assurer un controle humain par des personnes competentes.",
        "Surveiller le fonctionnement et conserver les journaux.",
        "Analyse d'impact sur les droits fondamentaux si requise (Article 27).",
        "Informer les personnes concernees le cas echeant.",
    ],
    ("provider", "limited"): [
        "Obligations d'information / transparence (Article 50).",
        "Marquage des contenus de synthese dans un format lisible par machine.",
    ],
    ("deployer", "limited"): [
        "Informer les personnes exposees (chatbot, emotions, deepfake).",
        "Signaler le caractere artificiel des contenus diffuses.",
    ],
    ("provider", "prohibited"): [
        "Interdit : le systeme ne peut etre ni mis sur le marche ni utilise (Article 5).",
    ],
    ("deployer", "prohibited"): [
        "Interdit : l'utilisation du systeme est prohibee (Article 5).",
    ],
    ("provider", "minimal"): [
        "Aucune obligation specifique. Codes de conduite volontaires encourages.",
    ],
    ("deployer", "minimal"): [
        "Aucune obligation specifique au titre de l'AI Act.",
    ],
}

# --------------------------------------------------------------------------
# Index de references juridiques (AI Act + RGPD)
# --------------------------------------------------------------------------
LEGAL_REFS = {
    "ai_act": {"title": "Reglement (UE) 2024/1689 (AI Act)", "url": AI_ACT_URL},
    "ai_act_art_4": {"title": "Article 4 — Litteratie en matiere d'IA",
                     "summary": "Les fournisseurs et deployeurs assurent un niveau "
                                "suffisant de litteratie IA de leur personnel.",
                     "url": AI_ACT_URL},
    "ai_act_art_5": {"title": "Article 5 — Pratiques interdites",
                     "summary": "Liste des pratiques d'IA interdites dans l'Union.",
                     "url": AI_ACT_URL},
    "ai_act_art_6": {"title": "Article 6 — Regles de classification haut risque",
                     "summary": "Definit quand un systeme est a haut risque (Annexe I/III).",
                     "url": AI_ACT_URL},
    "ai_act_art_9": {"title": "Article 9 — Systeme de gestion des risques",
                     "summary": "Processus continu de gestion des risques pour le haut risque.",
                     "url": AI_ACT_URL},
    "ai_act_art_10": {"title": "Article 10 — Gouvernance des donnees",
                      "summary": "Qualite et gouvernance des jeux de donnees d'entrainement.",
                      "url": AI_ACT_URL},
    "ai_act_art_13": {"title": "Article 13 — Transparence et information",
                      "summary": "Notice d'utilisation et transparence envers les deployeurs.",
                      "url": AI_ACT_URL},
    "ai_act_art_14": {"title": "Article 14 — Controle humain",
                      "summary": "Conception permettant une supervision humaine effective.",
                      "url": AI_ACT_URL},
    "ai_act_art_50": {"title": "Article 50 — Obligations de transparence",
                      "summary": "Chatbots, contenus de synthese et deepfakes.",
                      "url": AI_ACT_URL},
    "ai_act_art_53": {"title": "Article 53 — Obligations des fournisseurs GPAI",
                      "summary": "Documentation, droit d'auteur, resume des donnees.",
                      "url": AI_ACT_URL},
    "ai_act_art_55": {"title": "Article 55 — GPAI a risque systemique",
                      "summary": "Evaluation, attenuation, cybersecurite, incidents.",
                      "url": AI_ACT_URL},
    "gdpr": {"title": "Reglement (UE) 2016/679 (RGPD)", "url": GDPR_URL},
    "gdpr_art_6": {"title": "Article 6 — Liceite du traitement",
                   "summary": "Bases legales du traitement de donnees personnelles.",
                   "url": GDPR_URL},
    "gdpr_art_9": {"title": "Article 9 — Categories particulieres",
                   "summary": "Donnees sensibles (sante, biometrie, opinions, etc.).",
                   "url": GDPR_URL},
    "gdpr_art_22": {"title": "Article 22 — Decision automatisee et profilage",
                    "summary": "Droit de ne pas faire l'objet d'une decision "
                               "exclusivement automatisee.",
                    "url": GDPR_URL},
    "gdpr_art_30": {"title": "Article 30 — Registre des traitements", "summary": "",
                    "url": GDPR_URL},
    "gdpr_art_35": {"title": "Article 35 — Analyse d'impact (AIPD/DPIA)",
                    "summary": "Requise pour les traitements a risque eleve.",
                    "url": GDPR_URL},
    "gdpr_art_37": {"title": "Article 37 — Delegue a la protection des donnees (DPO)",
                    "summary": "Cas ou la designation d'un DPO est obligatoire.",
                    "url": GDPR_URL},
}

# --------------------------------------------------------------------------
# RGPD — bases legales et croisement
# --------------------------------------------------------------------------
GDPR_LAWFUL_BASES = [
    "Consentement (Art. 6(1)(a))",
    "Execution d'un contrat (Art. 6(1)(b))",
    "Obligation legale (Art. 6(1)(c))",
    "Interets vitaux (Art. 6(1)(d))",
    "Mission d'interet public (Art. 6(1)(e))",
    "Interet legitime (Art. 6(1)(f))",
]

GDPR_TRIGGERS = [
    {"id": "decision_auto",
     "label": "Decision automatisee / profilage",
     "keywords": ["decision automatisee", "profilage", "scoring", "automated decision",
                  "profiling", "notation automatique"],
     "obligations": ["Article 22 (decision automatisee)", "AIPD recommandee (Article 35)",
                     "Information renforcee (Articles 13-14)"]},
    {"id": "sensibles",
     "label": "Donnees sensibles (categories particulieres)",
     "keywords": ["donnees de sante", "sante", "biometrie", "opinions politiques",
                  "religion", "orientation sexuelle", "origine ethnique",
                  "health data", "biometric"],
     "obligations": ["Base de l'Article 9(2) requise", "AIPD probable (Article 35)"]},
    {"id": "surveillance",
     "label": "Surveillance systematique a grande echelle",
     "keywords": ["surveillance", "monitoring a grande echelle", "videosurveillance",
                  "tracking", "geolocalisation", "large scale monitoring"],
     "obligations": ["Designation d'un DPO probable (Article 37)", "AIPD (Article 35)"]},
    {"id": "transfert",
     "label": "Transfert hors Union europeenne",
     "keywords": ["transfert hors ue", "hors union europeenne", "etats-unis",
                  "international transfer", "cloud americain", "sous-traitant etranger"],
     "obligations": ["Encadrement des transferts (Chapitre V, Articles 44-49)",
                     "Clauses contractuelles types ou decision d'adequation"]},
]

GDPR_ALWAYS = [
    "Tenir un registre des traitements (Article 30).",
    "Informer les personnes concernees (Articles 13-14).",
    "Garantir les droits (acces, rectification, effacement...) (Articles 15-22).",
    "Notifier toute violation sous 72 h a la CNIL (Articles 33-34).",
]
