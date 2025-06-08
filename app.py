# app.py

import streamlit as st
from st_cytoscape import cytoscape
from data import nodes

# ─────────────────────────────────────────────────────────────────────────────
# 1) Configuration de la page Streamlit et CSS global
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arbre Interactif – Mindmap Tech",
    layout="wide",
)

# CSS global pour la police, le fond, la sidebar, et le conteneur Cytoscape
st.markdown(
    """
    <style>
      /* ===== Police et fond général ===== */
      body {
        font-family: "Helvetica", "Arial", sans-serif;
        background-color: #f8f9fa;  /* gris très clair */
      }
      /* ===== Sidebar ===== */
      .sidebar .sidebar-content {
        background-color: #ffffff;   /* fond blanc */
        padding: 16px;
      }
      .sidebar .sidebar-content p, .sidebar .sidebar-content li {
        font-size: 14px;
        line-height: 1.5;
      }
      /* ===== Titres ===== */
      h1, h2, h3, h4 {
        color: #2c3e50;  /* bleu foncé */
      }
      /* ===== Conteneur du composant Cytoscape ===== */
      div[data-testid="cytoscape-widget"],
      div[data-testid="stCytoscape"] {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-left: auto;
        margin-right: auto;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre et description introductive
st.title("🗺️ Arbre Interactif – Mindmap Tech")
st.markdown(
    """
    **Bienvenue !**  
    Cliquez sur le **rectangle “Arbre Tech”** pour déployer les 7 branches principales.  
    Ensuite :
    - Cliquez sur chaque branche “principal” pour dévoiler ses sous‐sections.  
    - Puis sur chaque “secondaire” pour découvrir les feuilles (si existantes).  
    Toutes les infos supplémentaires s’affichent dans la sidebar de droite.
    """,
    unsafe_allow_html=True
)

# Texte fixe initial dans la sidebar tant qu’aucun clic n’a eu lieu
if "intro_done" not in st.session_state:
    st.sidebar.markdown(
        """
        ### Détails du nœud  
        Cliquez sur un nœud dans l’arbre pour voir ses informations ici.
        """
    )
    st.session_state["intro_done"] = True


# ─────────────────────────────────────────────────────────────────────────────
# 2) Stylesheet pour Cytoscape (arborescent vertical, nœuds + arêtes)
# ─────────────────────────────────────────────────────────────────────────────
stylesheet_base = [
    {
        "selector": "[group = 'root']",
        "style": {
            "content": "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            "background-color": "#2c3e50",  # bleu nuit foncé
            "color": "#ffffff",
            "font-size": "16px",
            "shape": "rectangle",
            "width": "160px",             # root un peu plus large
            "height": "40px",
            "border-width": 2,
            "border-color": "#1a252f",
            "border-opacity": 1,
            "z-index": 100,
        },
    },
    {
        "selector": "[group = 'principal']",
        "style": {
            "content": "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            "background-color": "#3498db",  # bleu vif
            "color": "#ffffff",
            "font-size": "14px",
            "shape": "rectangle",
            "width": "130px",              # légèrement réduit
            "height": "32px",
            "border-width": 1,
            "border-color": "#2573a6",
            "border-opacity": 0.9,
            "shadow-color": "#000000",
            "shadow-blur": 4,
            "shadow-opacity": 0.1,
            "shadow-offset-x": 0,
            "shadow-offset-y": 2,
            "z-index": 90,
        },
    },
    {
        "selector": "[group = 'secondaire']",
        "style": {
            "content": "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            "background-color": "#e67e22",  # orange vif
            "color": "#ffffff",
            "font-size": "12px",
            "shape": "rectangle",
            "width": "115px",
            "height": "30px",
            "border-width": 1,
            "border-color": "#b35918",
            "border-opacity": 0.9,
            "shadow-color": "#000000",
            "shadow-blur": 3,
            "shadow-opacity": 0.1,
            "shadow-offset-x": 0,
            "shadow-offset-y": 1,
            "z-index": 80,
        },
    },
    {
        "selector": "[group = 'feuille']",
        "style": {
            "content": "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            "background-color": "#27ae60",  # vert vif
            "color": "#ffffff",
            "font-size": "10px",
            "shape": "rectangle",
            "width": "100px",
            "height": "28px",
            "border-width": 1,
            "border-color": "#1e8449",
            "border-opacity": 0.9,
            "shadow-color": "#000000",
            "shadow-blur": 2,
            "shadow-opacity": 0.1,
            "shadow-offset-x": 0,
            "shadow-offset-y": 1,
            "z-index": 70,
        },
    },
    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",
            "line-color": "#adb5bd",         # gris bleuté clair
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#adb5bd",
            "width": 1.5,
            "opacity": 0.6,
            "z-index": 50,
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# 3) Layout « breadthfirst » (vertical, top-to-bottom) pour l’arbre hiérarchique
# ─────────────────────────────────────────────────────────────────────────────
layout = {
    "name": "breadthfirst",
    "roots": ["root"],      # on force « root » à être tout en haut
    "directed": True,
    "circle": False,        # pas de cercles concentriques
    "padding": 30,          # marge autour du graphe
    "spacingFactor": 1.7,   # espacement vertical
}


# ─────────────────────────────────────────────────────────────────────────────
# 4) Initialisation de st.session_state (nœuds et arêtes affichés)
# ─────────────────────────────────────────────────────────────────────────────
if "displayed_nodes" not in st.session_state:
    st.session_state["displayed_nodes"] = [
        n for n in nodes if n["data"]["id"] == "root"
    ]
    st.session_state["displayed_edges"] = []


# ─────────────────────────────────────────────────────────────────────────────
# 5) Fonctions de révélation progressive
# ─────────────────────────────────────────────────────────────────────────────
def reveal_principals():
    """
    Quand on clique sur « root », ajoute les nœuds principal (parent='root')
    et crée les arêtes root→principal.
    """
    disp_nodes = st.session_state["displayed_nodes"]
    disp_edges = st.session_state["displayed_edges"]

    for n in nodes:
        d = n["data"]
        if d.get("group") == "principal" and d.get("parent") == "root":
            if not any(x["data"]["id"] == d["id"] for x in disp_nodes):
                disp_nodes.append(n)
                disp_edges.append({
                    "data": {
                        "id": f"edge_root_{d['id']}",
                        "source": "root",
                        "target": d["id"],
                    }
                })

    st.session_state["displayed_nodes"] = disp_nodes
    st.session_state["displayed_edges"] = disp_edges


def reveal_secondaries(parent_id):
    """
    Quand on clique sur un nœud principal, ajoute les secondaires (parent=parent_id)
    et crée les arêtes parent→secondary.
    """
    disp_nodes = st.session_state["displayed_nodes"]
    disp_edges = st.session_state["displayed_edges"]

    for n in nodes:
        d = n["data"]
        if d.get("group") == "secondaire" and d.get("parent") == parent_id:
            if not any(x["data"]["id"] == d["id"] for x in disp_nodes):
                disp_nodes.append(n)
                disp_edges.append({
                    "data": {
                        "id": f"edge_{parent_id}_{d['id']}",
                        "source": parent_id,
                        "target": d["id"],
                    }
                })

    st.session_state["displayed_nodes"] = disp_nodes
    st.session_state["displayed_edges"] = disp_edges


def reveal_leaves(parent_id):
    """
    Quand on clique sur un nœud secondaire, ajoute les feuilles (parent=parent_id)
    et crée les arêtes parent→leaf.
    """
    disp_nodes = st.session_state["displayed_nodes"]
    disp_edges = st.session_state["displayed_edges"]

    for n in nodes:
        d = n["data"]
        if d.get("group") == "feuille" and d.get("parent") == parent_id:
            if not any(x["data"]["id"] == d["id"] for x in disp_nodes):
                disp_nodes.append(n)
                disp_edges.append({
                    "data": {
                        "id": f"edge_{parent_id}_{d['id']}",
                        "source": parent_id,
                        "target": d["id"],
                    }
                })

    st.session_state["displayed_nodes"] = disp_nodes
    st.session_state["displayed_edges"] = disp_edges


# ─────────────────────────────────────────────────────────────────────────────
# 6) Affichage unique du composant Cytoscape
# ─────────────────────────────────────────────────────────────────────────────
elements_to_show = (
    st.session_state["displayed_nodes"] + st.session_state["displayed_edges"]
)

selected = cytoscape(
    elements=elements_to_show,
    stylesheet=stylesheet_base,
    layout=layout,
    width="100%",
    height="650px",
    user_zooming_enabled=True,
    user_panning_enabled=True,
    key="cyto_graph",
)


# ─────────────────────────────────────────────────────────────────────────────
# 7) Traitement du clic pour « déplier » l’arbre et mise à jour de la sidebar
# ─────────────────────────────────────────────────────────────────────────────
if selected:
    clicked_nodes = selected.get("nodes", [])
    if clicked_nodes:
        clicked_id = clicked_nodes[0]

        # 7.1) Si on clique sur « root » → révèle les principals
        if clicked_id == "root":
            reveal_principals()

        # 7.2) Si on clique sur un principal → révèle ses secondaires
        elif clicked_id in [
            n["data"]["id"] for n in nodes if n["data"]["group"] == "principal"
        ]:
            reveal_secondaries(clicked_id)

        # 7.3) Si on clique sur un secondaire → révèle ses feuilles
        elif clicked_id in [
            n["data"]["id"] for n in nodes if n["data"]["group"] == "secondaire"
        ]:
            reveal_leaves(clicked_id)

        # 7.4) Mise à jour de la sidebar
        st.sidebar.header(f"Détails : {clicked_id}")
        content_map = {
            # ─── Root ───────────────────────────────────────────────────────────
            "root": """
   ### Bienvenue sur l’Arbre Tech  
   Cliquez sur **Arbre Tech** (rectangle tout en haut) pour déployer les branches principales.
   """,

            # ─── Principals ──────────────────────────────────────────────────────
            "developpement": """
   ### Développement / Programmation  
   Domaine : Création de logiciels, applications, sites ou systèmes numériques à l’aide de langages de programmation.
   """,
            "data_ia": """
   ### Data & Intelligence Artificielle  
   Domaine : Exploiter les données et développer des systèmes d’IA pour analyser, prévoir et automatiser.
   """,
            "cybersecurite": """
   ### Cybersécurité  
   Domaine : Protéger les systèmes informatiques contre les cyberattaques, fuites de données ou intrusions.
   """,
            "cloud_systemes": """
   ### Cloud / Systèmes / Réseaux  
   Domaine : Concevoir, faire fonctionner et sécuriser les infrastructures numériques (cloud, serveurs, réseaux).
   """,
            "design_produit": """
   ### Design / Produit  
   Domaine : Imaginer, concevoir et améliorer des interfaces numériques ou des produits interactifs.
   """,
            "gestion_strategie": """
   ### Gestion / Stratégie / Innovation  
   Domaine : Organiser, piloter et faire évoluer les projets et les structures numériques.
   """,
            "hardware_robotique": """
   ### Hardware / Robotique / Électronique  
   Domaine : Concevoir et programmer des systèmes physiques intelligents (robots, objets connectés, cartes électroniques).
   """,

            # ─── Secondaires “Développement” ──────────────────────────────────
            "dev_web": """
   ### Développeur·se Web  
   • Frontend : interface visible d’un site (HTML, CSS, JS).  
   • Backend : moteur invisible (bases de données, logique).  
   • Fullstack : maîtrise des deux.  
   🧠 Compétences : React, Angular, SQL, API, Git  
   🎯 Objectif : créer des sites efficaces, rapides et sécurisés.
   """,
            "dev_mobile": """
   ### Développeur·se Mobile  
   • Crée des applis pour smartphones (iOS/Android).  
   • Utilise Swift, Kotlin, Flutter, etc.  
   🧠 Compétences : responsive design, UX mobile  
   📱 Objectif : proposer une appli fluide et moderne.
   """,
            "dev_logiciel": """
   ### Développeur·se Logiciel  
   • Conçoit des logiciels pour PC ou serveurs.  
   • Participe à toutes les étapes du développement.  
   🧠 Compétences : Java, C#, Python, POO  
   🎯 Objectif : fournir des logiciels stables et performants.
   """,
            "dev_jeux": """
   ### Développeur·se Jeux Vidéo  
   • Crée gameplay, IA, graphismes interactifs.  
   • Utilise Unity, Unreal Engine.  
   🧠 Compétences : animation, temps réel, moteur 3D  
   🎮 Objectif : offrir une expérience immersive et ludique.
   """,
            "dev_ia_ml": """
   ### Développeur·se IA / Machine Learning  
   • Crée des algorithmes capables d’apprendre.  
   • Utilise Python, TensorFlow, scikit-learn.  
   🧠 Compétences : statistiques, big data, IA  
   🎯 Objectif : automatiser l’analyse de données.
   """,
            "devops": """
   ### DevOps Engineer  
   • Automatise les déploiements, surveille les serveurs.  
   • Utilise Docker, Jenkins, Kubernetes.  
   🧠 Compétences : scripting, cloud, CI/CD  
   ⚙ Objectif : fiabiliser et accélérer les mises en production.
   """,
            "dev_embarque": """
   ### Développeur·se embarqué  
   • Programme des systèmes dans des objets connectés.  
   • Travaille en temps réel avec peu de ressources.  
   🧠 Compétences : C, électronique, IoT  
   🔌 Objectif : rendre les objets intelligents.
   """,
            "dev_blockchain": """
   ### Développeur·se Blockchain  
   • Crée des applis décentralisées (smart contracts).  
   • Utilise Solidity, Rust, Web3.js.  
   🧠 Compétences : crypto, réseaux, Web3  
   🔐 Objectif : créer des systèmes sûrs et sans intermédiaire.
   """,

            # ─── Secondaires “Data & IA” ───────────────────────────────────────
            "data_scientist": """
   ### Data Scientist  
   • Analyse de volumes de données pour en extraire des modèles.  
   • Utilise techniques statistiques, visualisation, machine learning.  
   🧠 Compétences : Python, R, SQL, statistiques, scikit-learn  
   🎯 Objectif : transformer les données en décisions.
   """,
            "data_analyst": """
   ### Data Analyst  
   • Crée tableaux de bord et rapports à partir de données.  
   • Répond aux questions métiers via analyses claires.  
   🧠 Compétences : Excel, Power BI, SQL, data visualisation  
   🎯 Objectif : rendre les données compréhensibles et exploitables.
   """,
            "data_engineer": """
   ### Data Engineer  
   • Construit des pipelines de données fiables et automatisés.  
   • Prépare les données pour analystes et data scientists.  
   🧠 Compétences : Spark, ETL, cloud (AWS/GCP), NoSQL  
   🎯 Objectif : structurer les flux de données pour l’entreprise.
   """,
            "ml_engineer": """
   ### ML Engineer  
   • Déploie des modèles d’IA dans produits ou services.  
   • Optimise performances algorithmiques pour usage réel.  
   🧠 Compétences : Python, TensorFlow, MLOps, CI/CD  
   🎯 Objectif : intégrer l’IA dans les outils numériques.
   """,
            "mlops_engineer": """
   ### MLOps Engineer  
   • Automatise entraînement, test et déploiement de modèles ML.  
   • Assure reproductibilité, suivi et robustesse des IA.  
   🧠 Compétences : Docker, Kubernetes, MLflow, CI/CD  
   🎯 Objectif : fiabiliser l’usage de l’IA en production.
   """,
            "ai_researcher": """
   ### AI Researcher  
   • Travaille sur fondements de l’intelligence artificielle.  
   • Explore nouvelles approches algorithmiques.  
   🧠 Compétences : mathématiques avancées, deep learning, publications  
   🎯 Objectif : faire progresser les capacités de l’IA.
   """,
            "prompt_engineer": """
   ### AI Prompt Engineer  
   • Conçoit instructions optimales pour interagir avec modèles de langage (GPT, Claude…).  
   • Optimise requêtes pour résultats pertinents.  
   🧠 Compétences : NLP, ingénierie linguistique, test A/B  
   🎯 Objectif : améliorer l'efficacité des systèmes conversationnels.
   """,
            "data_steward": """
   ### Data Steward  
   • Gère qualité, gouvernance et conformité des données.  
   • Collabore avec équipes IT, légales et métier.  
   🧠 Compétences : RGPD, data lineage, outils de gouvernance  
   🎯 Objectif : garantir que la donnée est fiable et traçable.
   """,

            # ─── Secondaires “Cybersécurité” ──────────────────────────────────
            "analyste_soc": """
   ### Analyste SOC  
   • Surveille en temps réel les alertes de sécurité.  
   • Utilise outils pour détecter intrusions et anomalies.  
   🧠 Compétences : SIEM (Splunk), logs, protocoles réseau  
   🎯 Objectif : détecter et bloquer les cyberattaques.
   """,
            "pentester": """
   ### Pentester  
   • Simule des cyberattaques pour tester les systèmes.  
   • Identifie failles avant les vrais hackers.  
   🧠 Compétences : Kali Linux, Metasploit, OWASP  
   🎯 Objectif : trouver vulnérabilités avant exploitation.
   """,
            "sec_reseau": """
   ### Ingénieur·e Sécurité Réseau  
   • Conçoit architecture réseau sécurisée.  
   • Met en place pare-feux, VPN, antivirus…  
   🧠 Compétences : chiffrement, firewall, systèmes  
   🎯 Objectif : empêcher les accès non autorisés.
   """,
            "cryptoanalyste": """
   ### Cryptoanalyste  
   • Analyse et conçoit systèmes de chiffrement.  
   • Peut chercher à casser ou renforcer des codes.  
   🧠 Compétences : mathématiques, cryptographie  
   🎯 Objectif : sécuriser ou décoder l'information.
   """,
            "rssi": """
   ### Responsable Cybersécurité / RSSI  
   • Supervise stratégie de sécurité d'une entreprise.  
   • Gère risques, équipe sécurité, conformité.  
   🧠 Compétences : gouvernance, droit numérique, audit  
   🎯 Objectif : protéger l’organisation à haut niveau.
   """,
            "expert_forensic": """
   ### Expert Forensic  
   • Analyse des systèmes après une attaque.  
   • Récupère preuves, reconstitue actions.  
   🧠 Compétences : investigation, outils forensics, droit  
   🎯 Objectif : comprendre l’attaque et retrouver auteurs.
   """,

            # ─── Secondaires “Cloud / Systèmes / Réseaux” ──────────────────────
            "ing_cloud": """
   ### Ingénieur·e Cloud  
   • Conçoit systèmes hébergés sur AWS, Azure, GCP…  
   • Automatise déploiement, assure scalabilité.  
   🧠 Compétences : Terraform, Docker, scripting  
   🎯 Objectif : héberger des services fiables dans le cloud.
   """,
            "admin_sys_reseau": """
   ### Administrateur·trice Systèmes & Réseaux  
   • Gère serveurs et réseaux d’une organisation.  
   • Assure disponibilité des services informatiques.  
   🧠 Compétences : TCP/IP, DNS, Active Directory  
   🎯 Objectif : garantir la stabilité du système.
   """,
            "archi_cloud": """
   ### Architecte Cloud / Infrastructure  
   • Conçoit structure technique d’un système numérique.  
   • Choisit outils adaptés, pense long terme.  
   🧠 Compétences : architecture logicielle, sécurité, multi-cloud  
   🎯 Objectif : bâtir des infrastructures robustes.
   """,
            "tech_reseau": """
   ### Technicien·ne Réseaux / IT  
   • Installe et entretient équipements informatiques.  
   • Intervient en cas de panne ou de problème utilisateur.  
   🧠 Compétences : diagnostic, support, maintenance  
   🎯 Objectif : garantir l’accès et le bon usage des outils.
   """,
            "sre": """
   ### Site Reliability Engineer  
   • Fiabilise services numériques à grande échelle.  
   • Automatise tests, surveillance, incidents.  
   🧠 Compétences : CI/CD, monitoring, cloud  
   🎯 Objectif : assurer la disponibilité continue des services.
   """,

            # ─── Secondaires “Design / Produit” ─────────────────────────────────
            "ux_designer": """
   ### UX Designer  
   • Étudie besoins utilisateurs, crée parcours intuitifs.  
   • Réalise maquettes, tests et prototypes interactifs.  
   🧠 Compétences : Figma, design thinking, ergonomie  
   🎯 Objectif : rendre l’utilisation d’un outil simple et agréable.
   """,
            "ui_designer": """
   ### UI Designer  
   • Travaille aspect visuel (boutons, couleurs, typo…).  
   • Assure cohérence graphique des interfaces.  
   🧠 Compétences : design graphique, Illustrator, Adobe XD  
   🎯 Objectif : créer des interfaces belles et lisibles.
   """,
            "product_manager": """
   ### Product Owner / Product Manager  
   • Détermine besoins prioritaires du produit.  
   • Sert de lien entre équipe technique et utilisateurs.  
   🧠 Compétences : agilité, gestion de projet, rédaction de specs  
   🎯 Objectif : livrer un produit utile et pertinent.
   """,
            "game_designer": """
   ### Game Designer  
   • Imagine règles, mécaniques et niveaux de jeu.  
   • Collabore avec devs, artistes, scénaristes.  
   🧠 Compétences : logique, narration, prototypage  
   🎯 Objectif : offrir une expérience de jeu captivante.
   """,
            "ergonome": """
   ### Ergonome numérique  
   • Étudie interaction homme-machine.  
   • Rend outils numériques accessibles et confortables.  
   🧠 Compétences : sciences cognitives, tests utilisateurs  
   🎯 Objectif : adapter la technologie à l’humain.
   """,
            "designer_3d": """
   ### Designer 3D / Graphiste technique  
   • Crée objets ou environnements numériques en 3D.  
   • Utilisé dans jeux vidéo, réalité virtuelle, industrie…  
   🧠 Compétences : Blender, Maya, modélisation  
   🎯 Objectif : donner forme aux mondes numériques.
   """,

            # ─── Secondaires “Gestion / Stratégie / Innovation” ────────────────
            "chef_projet": """
   ### Chef·fe de projet IT / digital  
   • Supervise réalisation d’un produit numérique.  
   • Gère délais, budgets, équipes pluridisciplinaires.  
   🧠 Compétences : planification, communication, outils projet  
   🎯 Objectif : livrer un projet conforme et dans les temps.
   """,
            "consultant_num": """
   ### Consultant·e en transformation numérique  
   • Accompagne entreprises dans leur digitalisation.  
   • Identifie besoins, propose solutions innovantes.  
   🧠 Compétences : audit, analyse stratégique, veille techno  
   🎯 Objectif : moderniser organisations grâce au numérique.
   """,
            "scrum_master": """
   ### Scrum Master / Coach Agile  
   • Facilite travail agile dans une équipe tech.  
   • Anime rituels et améliore collaboration.  
   🧠 Compétences : agilité, coaching, gestion de groupe  
   🎯 Objectif : fluidifier et optimiser fonctionnement de l’équipe.
   """,
            "tech_evangelist": """
   ### Tech Evangelist / Developer Advocate  
   • Présente technologies à publics techniques.  
   • Crée contenus, anime communautés.  
   🧠 Compétences : développement, communication, pédagogie  
   🎯 Objectif : promouvoir une technologie et fédérer autour.
   """,
            "entrepreneur_tech": """
   ### Entrepreneur·e tech / Startup Founder  
   • Crée entreprise dans la tech (app, IA, plateforme…).  
   • Gère produit, équipe, finances, stratégie.  
   🧠 Compétences : innovation, leadership, vision produit  
   🎯 Objectif : apporter solution innovante au marché.
   """,

            # ─── Secondaires “Hardware / Robotique / Électronique” ────────────
            "ing_robotique": """
   ### Ingénieur·e Robotique  
   • Conçoit et pilote systèmes automatisés (robots).  
   • Combine mécanique, électronique et informatique.  
   🧠 Compétences : ROS, capteurs, automatisme  
   🎯 Objectif : créer des machines intelligentes.
   """,
            "ing_embarque": """
   ### Ingénieur·e Systèmes Embarqués  
   • Développe systèmes miniaturisés intégrés aux objets.  
   • Travaille en temps réel avec contraintes fortes.  
   🧠 Compétences : C/C++, microcontrôleurs, électronique  
   🎯 Objectif : rendre les objets connectés autonomes.
   """,
            "pcb_designer": """
   ### PCB Designer  
   • Dessine cartes électroniques (schémas, placement).  
   • Utilise CAO pour fabrication.  
   🧠 Compétences : Altium, Eagle, normes CE  
   🎯 Objectif : concevoir supports des composants électroniques.
   """,
            "tech_electronique": """
   ### Technicien·ne en Électronique  
   • Monte, teste et dépanne circuits ou appareils.  
   • Intervient en labo ou sur le terrain.  
   🧠 Compétences : soudure, oscilloscope, diagnostic  
   🎯 Objectif : garantir bon fonctionnement des systèmes.
   """,
            "ing_mecatronique": """
   ### Ingénieur·e Mécatronique  
   • Fusionne mécanique, électronique et informatique embarquée.  
   • Conçoit systèmes automatisés complexes (robots, drones).  
   🧠 Compétences : SolidWorks, robotique, contrôle-commande  
   🎯 Objectif : produire systèmes intelligents et interactifs.
   """,
        }

        if clicked_id in content_map:
            st.sidebar.markdown(content_map[clicked_id], unsafe_allow_html=True)
        else:
            st.sidebar.write("Aucun contenu disponible pour ce nœud.")
