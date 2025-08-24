# TechSight - Plateforme d'Intelligence du Marché de l'Emploi Tech 

Une plateforme complète d'analyse du marché de l'emploi technologique au Maroc, utilisant le web scraping automatisé et la visualisation de données pour fournir des insights précieux sur les tendances d'embauche.

## Aperçu du Projet

TechSight collecte automatiquement les offres d'emploi tech depuis LinkedIn, les analyse et présente des visualisations interactives pour aider les professionnels et recruteurs à comprendre les tendances du marché.

### Fonctionnalités Principales

- **Scraping Automatisé** : Collection quotidienne d'offres d'emploi depuis LinkedIn
- **Analyse des Compétences** : Extraction et analyse des compétences techniques demandées
- **Visualisations Interactives** : Graphiques et KPIs en temps réel
- **Filtrage par Rôle** : Vue détaillée par type de poste (Data Scientist, Web Developer, etc.)
- **Géolocalisation** : Analyse par ville et région
- **Tendances Temporelles** : Évolution du marché dans le temps

## Technologies Utilisées

### Backend & Data Processing
- **Python 3.11+** - Langage principal
- **Selenium** - Web scraping automatisé
- **BeautifulSoup** - Parsing HTML
- **Pandas** - Manipulation de données
- **spaCy** - Traitement du langage naturel pour l'extraction de compétences

### Frontend & Visualisation
- **Streamlit** - Interface web interactive
- **Matplotlib** - Génération de graphiques

### Automation 
- **GitHub Actions** - pour le scraping automatique

## Structure du Projet

```
mouad-melloul-techsight/
├── README.md                    # Documentation du projet
├── app.py                      # Application Streamlit principale
├── requirements.txt            # Dépendances Python
├── TechSight.png              # Logo de l'application
├── code/
│   ├── cleaning.ipynb         # Notebook de nettoyage des données
│   └── functions.py           # Fonctions utilitaires
├── data/
│   └── dataset_final.csv      # Dataset des offres d'emploi
├── scraping/
│   └── auto_scraper_linkedin.py  # Script de scraping LinkedIn
└── .github/
    └── workflows/
        └── scraper.yml        # Workflow GitHub Actions
```

## Installation et Configuration

### Prérequis
- Python 3.11 ou supérieur

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/mouad-melloul-techsight.git
cd mouad-melloul-techsight
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. **Lancer l'application**
```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

## Utilisation

### Interface Utilisateur

1. **Sélection de Rôle** : Utilisez la sidebar pour filtrer par type de poste (Data Scientist, Data Analyst, etc.)
2. **KPIs** : Consultez les métriques clés (nombre d'offres, entreprises, villes, etc.)
3. **Visualisations** :
   - Répartition géographique des offres
   - Top des compétences demandées
   - Entreprises les plus actives
   - Évolution temporelle des offres

### Scraping Manuel

Pour lancer une collecte de données manuellement :

```bash
python scraping/auto_scraper_linkedin.py
```

### Automatisation

Le scraping s'exécute automatiquement chaque lundi à 8h UTC via GitHub Actions. Vous pouvez aussi le déclencher manuellement depuis l'onglet "Actions" de votre repository GitHub.


**TechSight** - Transforming job market data into actionable insights 
