# data.py

# Chaque nœud doit avoir :
# - "id" unique
# - "label" (texte affiché)
# - "group" ∈ {"root", "principal", "secondaire", "feuille"}
# - "parent" si ce nœud n’est pas le root

nodes = [
    # ─── Root ────────────────────────────────────────────────────────────────
    {
        "data": {
            "id": "root",
            "label": "Arbre Tech",
            "group": "root",
            # pas de "parent" pour le root
        }
    },

    # ─── Branches principales (group="principal", parent="root") ──────────────
    {
        "data": {
            "id": "developpement",
            "label": "Développement / Programmation",
            "group": "principal",
            "parent": "root",
        }
    },
    {
        "data": {
            "id": "data_ia",
            "label": "Data & Intelligence Artificielle",
            "group": "principal",
            "parent": "root",
        }
    },
    {
        "data": {
            "id": "cybersecurite",
            "label": "Cybersécurité",
            "group": "principal",
            "parent": "root",
        }
    },
    {
        "data": {
            "id": "cloud_systemes",
            "label": "Cloud / Systèmes / Réseaux",
            "group": "principal",
            "parent": "root",
        }
    },
    {
        "data": {
            "id": "design_produit",
            "label": "Design / Produit",
            "group": "principal",
            "parent": "root",
        }
    },
    {
        "data": {
            "id": "gestion_strategie",
            "label": "Gestion / Stratégie / Innovation",
            "group": "principal",
            "parent": "root",
        }
    },
    {
        "data": {
            "id": "hardware_robotique",
            "label": "Hardware / Robotique / Électronique",
            "group": "principal",
            "parent": "root",
        }
    },

    # ─── Sous‐branches “Développement / Programmation” ─────────────────────────
    {
        "data": {
            "id": "dev_web",
            "label": "Développeur·se Web",
            "group": "secondaire",
            "parent": "developpement",
        }
    },
    {
        "data": {
            "id": "dev_mobile",
            "label": "Développeur·se Mobile",
            "group": "secondaire",
            "parent": "developpement",
        }
    },
    {
        "data": {
            "id": "dev_logiciel",
            "label": "Développeur·se Logiciel",
            "group": "secondaire",
            "parent": "developpement",
        }
    },
    {
        "data": {
            "id": "dev_jeux",
            "label": "Développeur·se Jeux Vidéo",
            "group": "secondaire",
            "parent": "developpement",
        }
    },
    {
        "data": {
            "id": "dev_ia_ml",
            "label": "Développeur·se IA / Machine Learning",
            "group": "secondaire",
            "parent": "developpement",
        }
    },
    {
        "data": {
            "id": "devops",
            "label": "DevOps Engineer",
            "group": "secondaire",
            "parent": "developpement",
        }
    },
    {
        "data": {
            "id": "dev_embarque",
            "label": "Développeur·se embarqué",
            "group": "secondaire",
            "parent": "developpement",
        }
    },
    {
        "data": {
            "id": "dev_blockchain",
            "label": "Développeur·se Blockchain",
            "group": "secondaire",
            "parent": "developpement",
        }
    },

    # ─── Sous‐branches “Data & Intelligence Artificielle” ──────────────────────
    {
        "data": {
            "id": "data_scientist",
            "label": "Data Scientist",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },
    {
        "data": {
            "id": "data_analyst",
            "label": "Data Analyst",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },
    {
        "data": {
            "id": "data_engineer",
            "label": "Data Engineer",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },
    {
        "data": {
            "id": "ml_engineer",
            "label": "ML Engineer",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },
    {
        "data": {
            "id": "mlops_engineer",
            "label": "MLOps Engineer",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },
    {
        "data": {
            "id": "ai_researcher",
            "label": "AI Researcher",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },
    {
        "data": {
            "id": "prompt_engineer",
            "label": "AI Prompt Engineer",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },
    {
        "data": {
            "id": "data_steward",
            "label": "Data Steward",
            "group": "secondaire",
            "parent": "data_ia",
        }
    },

    # ─── Sous‐branches “Cybersécurité” ─────────────────────────────────────────
    {
        "data": {
            "id": "analyste_soc",
            "label": "Analyste SOC",
            "group": "secondaire",
            "parent": "cybersecurite",
        }
    },
    {
        "data": {
            "id": "pentester",
            "label": "Pentester",
            "group": "secondaire",
            "parent": "cybersecurite",
        }
    },
    {
        "data": {
            "id": "sec_reseau",
            "label": "Ingénieur·e Sécurité Réseau",
            "group": "secondaire",
            "parent": "cybersecurite",
        }
    },
    {
        "data": {
            "id": "cryptoanalyste",
            "label": "Cryptoanalyste",
            "group": "secondaire",
            "parent": "cybersecurite",
        }
    },
    {
        "data": {
            "id": "rssi",
            "label": "Responsable Cybersécurité / RSSI",
            "group": "secondaire",
            "parent": "cybersecurite",
        }
    },
    {
        "data": {
            "id": "expert_forensic",
            "label": "Expert Forensic",
            "group": "secondaire",
            "parent": "cybersecurite",
        }
    },

    # ─── Sous‐branches “Cloud / Systèmes / Réseaux” ───────────────────────────
    {
        "data": {
            "id": "ing_cloud",
            "label": "Ingénieur·e Cloud",
            "group": "secondaire",
            "parent": "cloud_systemes",
        }
    },
    {
        "data": {
            "id": "admin_sys_reseau",
            "label": "Administrateur·trice Systèmes & Réseaux",
            "group": "secondaire",
            "parent": "cloud_systemes",
        }
    },
    {
        "data": {
            "id": "archi_cloud",
            "label": "Architecte Cloud / Infrastructure",
            "group": "secondaire",
            "parent": "cloud_systemes",
        }
    },
    {
        "data": {
            "id": "tech_reseau",
            "label": "Technicien·ne Réseaux / IT",
            "group": "secondaire",
            "parent": "cloud_systemes",
        }
    },
    {
        "data": {
            "id": "sre",
            "label": "Site Reliability Engineer",
            "group": "secondaire",
            "parent": "cloud_systemes",
        }
    },

    # ─── Sous‐branches “Design / Produit” ──────────────────────────────────────
    {
        "data": {
            "id": "ux_designer",
            "label": "UX Designer",
            "group": "secondaire",
            "parent": "design_produit",
        }
    },
    {
        "data": {
            "id": "ui_designer",
            "label": "UI Designer",
            "group": "secondaire",
            "parent": "design_produit",
        }
    },
    {
        "data": {
            "id": "product_manager",
            "label": "Product Owner / Product Manager",
            "group": "secondaire",
            "parent": "design_produit",
        }
    },
    {
        "data": {
            "id": "game_designer",
            "label": "Game Designer",
            "group": "secondaire",
            "parent": "design_produit",
        }
    },
    {
        "data": {
            "id": "ergonome",
            "label": "Ergonome numérique",
            "group": "secondaire",
            "parent": "design_produit",
        }
    },
    {
        "data": {
            "id": "designer_3d",
            "label": "Designer 3D / Graphiste technique",
            "group": "secondaire",
            "parent": "design_produit",
        }
    },

    # ─── Sous‐branches “Gestion / Stratégie / Innovation” ──────────────────────
    {
        "data": {
            "id": "chef_projet",
            "label": "Chef·fe de projet IT / digital",
            "group": "secondaire",
            "parent": "gestion_strategie",
        }
    },
    {
        "data": {
            "id": "consultant_num",
            "label": "Consultant·e en transformation numérique",
            "group": "secondaire",
            "parent": "gestion_strategie",
        }
    },
    {
        "data": {
            "id": "scrum_master",
            "label": "Scrum Master / Coach Agile",
            "group": "secondaire",
            "parent": "gestion_strategie",
        }
    },
    {
        "data": {
            "id": "tech_evangelist",
            "label": "Tech Evangelist / Developer Advocate",
            "group": "secondaire",
            "parent": "gestion_strategie",
        }
    },
    {
        "data": {
            "id": "entrepreneur_tech",
            "label": "Entrepreneur·e tech / Startup Founder",
            "group": "secondaire",
            "parent": "gestion_strategie",
        }
    },

    # ─── Sous‐branches “Hardware / Robotique / Électronique” ──────────────────
    {
        "data": {
            "id": "ing_robotique",
            "label": "Ingénieur·e Robotique",
            "group": "secondaire",
            "parent": "hardware_robotique",
        }
    },
    {
        "data": {
            "id": "ing_embarque",
            "label": "Ingénieur·e Systèmes Embarqués",
            "group": "secondaire",
            "parent": "hardware_robotique",
        }
    },
    {
        "data": {
            "id": "pcb_designer",
            "label": "PCB Designer",
            "group": "secondaire",
            "parent": "hardware_robotique",
        }
    },
    {
        "data": {
            "id": "tech_electronique",
            "label": "Technicien·ne en Électronique",
            "group": "secondaire",
            "parent": "hardware_robotique",
        }
    },
    {
        "data": {
            "id": "ing_mecatronique",
            "label": "Ingénieur·e Mécatronique",
            "group": "secondaire",
            "parent": "hardware_robotique",
        }
    },
]

# Les edges ne sont pas définies ici (elles seront générées dynamiquement dans app.py)
edges = []
