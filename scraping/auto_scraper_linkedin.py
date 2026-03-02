import pandas as pd
import time
import random
import spacy
from spacy.matcher import PhraseMatcher
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import chromedriver_autoinstaller
import os
import re

#! Configuration de ChromeDriver :
chromedriver_autoinstaller.install()  

chrome_options = Options()
chrome_options.add_argument("--headless") # pas d'interface graphique
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)" # Simule un vrai navigateur
) 

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(30)

#! Paramètres de scraping :
roles = [
    "data engineer",
    "data analyst",
    "data scientist",
    "web developer",
    "software engineer"
]
# endpoint (API publique/cachée) qui permet de récupérer des offres d'emploi sans authentification (guest)
linkedin_base = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/?keywords={query}&location=Morocco"

all_offers = []

#! Extraction automatique de compétences (NLP) :
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner", "tagger"])

def normalize_text(text):
    text = text.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

skills_dict = {

    # LANGUAGES

    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "c++": ["c++"],
    "c#": ["c#"],
    "c": ["c"],
    "php": ["php"],
    "scala": ["scala"],
    "swift": ["swift"],
    "r": ["r", "r language"],
    "matlab": ["matlab"],
    "bash": ["bash", "shell scripting"],
    "powershell": ["powershell"],

    # WEB / FRONTEND

    "html": ["html"],
    "css": ["css"],
    "react": ["react"],
    "next.js": ["next.js", "nextjs"],
    "angular": ["angular"],
    "vue": ["vue", "vue.js"],
    "tailwind": ["tailwind", "tailwindcss"],
    "bootstrap": ["bootstrap"],

    # BACKEND

    "node.js": ["node.js", "nodejs"],
    "express": ["express", "express.js"],
    "spring boot": ["spring boot"],
    "spring": ["spring framework"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "laravel": ["laravel"],
    "graphql": ["graphql"],
    "rest api": ["rest api", "restful"],
    "microservices": ["microservices"],

    # DATABASES

    "sql": ["sql"],
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql"],
    "sql server": ["sql server", "mssql"],
    "oracle": ["oracle"],
    "sqlite": ["sqlite"],
    "mongodb": ["mongodb"],

    # DATA ENGINEERING

    "spark": ["spark", "pyspark"],
    "hadoop": ["hadoop"],
    "kafka": ["kafka"],
    "airflow": ["airflow"],
    "etl": ["etl"],
    "elt": ["elt"],
    "snowflake": ["snowflake"],
    "bigquery": ["bigquery"],
    "redshift": ["redshift"],
    "databricks": ["databricks"],
    "data warehouse": ["data warehouse"],
    "data lake": ["data lake"],

    # DATA SCIENCE / ML

    "machine learning": ["machine learning"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision"],
    "reinforcement learning": ["reinforcement learning"],
    "time series": ["time series", "forecasting"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scipy": ["scipy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "plotly": ["plotly"],
    "spacy": ["spacy"],
    "huggingface": ["huggingface"],
    "llm": ["llm", "large language model"],

    # MLOPS

    "mlops": ["mlops"],
    "model deployment": ["model deployment"],
    "model monitoring": ["model monitoring"],
    "mlflow": ["mlflow"],

    # CLOUD

    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker"],
    "github actions": ["github actions"],
    "ci/cd": ["ci/cd", "continuous integration"],
    "apache": ["apache"],

    # BI / ANALYTICS

    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel"],
    "statistics": ["statistics"],

    # SOFTWARE ENGINEERING
    
    "design patterns": ["design patterns"],
    "unit testing": ["unit testing"],
    "agile": ["agile"],
    "scrum": ["scrum"],
    "jira": ["jira"],
    "git": ["git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
}

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

patterns = []
skill_lookup = {}

for canonical, variations in skills_dict.items():
    for variation in variations:
        norm_variation = normalize_text(variation)
        patterns.append(nlp.make_doc(norm_variation))
        skill_lookup[norm_variation] = canonical

matcher.add("SKILLS", patterns)


def extract_skills(text):
    text_norm = normalize_text(text)
    doc = nlp(text_norm)

    matches = matcher(doc)
    found = set()

    for _, start, end in matches:
        span = doc[start:end].text
        if span in skill_lookup:
            found.add(skill_lookup[span])

    return sorted(found)

#! main function :
def scrape_linkedin(role, max_pages=10):
    page = 0
    while page < max_pages:
        url = linkedin_base.format(query=role.replace(" ", "%20")) + f"&start={page * 25}" # LinkedIn pagine par 25 résultats
        try:
            driver.get(url)
        except Exception as e:
            print(f"[ERROR] Failed to load {url} : {e}")
            break
        time.sleep(3)
        '''
        time.sleep(3) :
        - wait for pages to load
        - reduce risk of being blocked
        - behave more like a human '''

        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="base-card")

        if not job_cards:
            break

        for card in job_cards:
            try:
                title_el = card.find("h3", class_="base-search-card__title")
                company_el = card.find("h4", class_="base-search-card__subtitle")
                location_el = card.find("span", class_="job-search-card__location")
                link_el = card.find("a", href=True, class_="base-card__full-link")
                time_el = card.find("time")

                if not title_el or not link_el or not time_el:
                    continue

                # Filtre temporel (offres récentes uniquement)
                posted_text = time_el.text.strip().lower()
                if not any(x in posted_text for x in ["minute", "minutes", "hour", "hours", "h", "today", "1 day"]):
                    continue

                date_el = (
                    card.find("time", class_="job-search-card__listdate")
                    or card.find("time", class_="job-search-card__listdate--new")
                )
                date_attr = date_el["datetime"] if date_el and date_el.has_attr("datetime") else ""


                job_link = link_el["href"]

                # Extraction des détails (ouverture d'onglets)
                driver.execute_script("window.open(arguments[0]);", job_link)
                driver.switch_to.window(driver.window_handles[1])
                
                try:
                    wait = WebDriverWait(driver, 10)
                    try:
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup")))
                        detail_soup = BeautifulSoup(driver.page_source, "html.parser")
                        description_el = detail_soup.find("div", class_="show-more-less-html__markup")
                    except:
                        description_el = None

                    skills = []
                    # Extraction des compétences via NLP
                    if description_el:
                        description_text = description_el.get_text(separator=" ").strip()
                        skills = extract_skills(description_text)

                    # Stockage des données
                    all_offers.append({
                        "Source": "LinkedIn",
                        "Rôle": role,
                        "Titre": title_el.text.strip(),
                        "Entreprise": company_el.text.strip() if company_el else "",
                        "Localisation": location_el.text.strip() if location_el else "",
                        "Lien": job_link,
                        "Compétences": ", ".join(skills),
                        "Date": date_attr 
                    })
                
                finally:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
                
            except Exception as e:
                print(f"[ERROR] {e}")
                continue
        page += 1


import os

# Get folder of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_final_path = os.path.join(script_dir, "..", "data", "dataset_final.csv")

#! CLEANER FUNCTION 
def cleaner(df):
    df = df.copy()
    source = df['Source'].unique()[0]
    df.drop('Source', axis=1, inplace=True)

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype('string')

    # Normalisation des villes marocaines
    moroccan_cities = [
        "Casablanca","Rabat","Tangier","Tanger","Fez","Fès","Marrakesh","Marrakech","Salé","Meknès","Oujda",
        "Kenitra","Agadir","Tetouan","Tétouan","Temara","Safi","Mohammedia","Khouribga",
        "El Jadida","Beni Mellal","Aït Melloul","Nador","Dar Bouazza","Taza","Settat",
        "Berrechid","Khemisset","Inezgane","Ksar El Kebir","Larache","Guelmim","Khenifra",
        "Berkane","Taourirt","Bouskoura","Fquih Ben Salah","Dcheira El Jihadia",
        "Oued Zem","El Kelaa Des Sraghna","Sidi Slimane","Errachidia","Guercif",
        "Oulad Teima","Ben Guerir","Benguerir","Tifelt","Lqliaa","Taroudant","Sefrou","Essaouira",
        "Fnideq","Sidi Kacem","Tiznit","Tan-Tan","Ouarzazate","Souk El Arbaa",
        "Youssoufia","Lahraouyine","Martil","Ain Harrouda","Suq as-Sabt Awlad an-Nama",
        "Skhirat","Ouazzane","Benslimane","Al Hoceima","Beni Ansar","M'diq","Sidi Bennour",
        "Midelt","Azrou","Drargua","Laâyoune","Dakhla","Taliouine","Ifrane","Sala al Jadida"
    ]

    # Synonyms mapping → canonical name
    city_synonyms = {
        "Tangier": ["Tangier", "Tanger"],
        "Fez": ["Fez", "Fès", "Fes"]
    }

    def normalize(text):
        text = str(text).lower().strip()
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    # Build synonym lookup dict
    synonym_to_city = {}
    for canonical, syns in city_synonyms.items():
        for s in syns:
            synonym_to_city[normalize(s)] = canonical

    def map_location_to_city(location):
       
        loc_norm = normalize(location)
        first_part = normalize(location.split(',')[0] if ',' in location else location)
        
        for syn, canonical in synonym_to_city.items():
            if syn in first_part:
                return canonical

        for c in moroccan_cities:
            if normalize(c) in first_part:
                return c

        # Step 2: fallback — check whole string if first part fails
        for syn, canonical in synonym_to_city.items():
            if syn in loc_norm:
                return canonical

        for c in moroccan_cities:
            if normalize(c) in loc_norm:
                return c

        return None

    df['Localisation'] = df['Localisation'].apply(
        lambda loc: map_location_to_city(loc) if pd.notna(loc) else loc
    ).fillna(df['Localisation'])

    # Mapping des titres vers les rôles standardisés
    role_keywords = {
        "data scientist": ["data scientist", "data scientists", "data science"],
        "data analyst": ["data analyst", "business analyst","analyste","analyst","data analytics","power bi developer"],
        "data engineer": ["data engineer", "big data engineer", "etl developer", "ingénieur data","database engineer"],
        "web developer": ["full stack", "full-stack", "python developer", "développeur python", 
                          "développeur web", "web developer", "frontend developer", "backend developer",
                          "frontend", "backend", "back-end", "front-end"],
        "software engineer": ["software engineer", "software developer", "ingénieur logiciel", "développeur logiciel",
                              "application developer", "desktop developer", "system developer", "systems engineer","system engineer"]
    }

    def map_title_to_role(title):
        title_lower = str(title).lower()
        for role, keywords in role_keywords.items():
            for kw in keywords:
                if kw.replace(" ", "") in title_lower.replace(" ", ""):
                    return role
                kw_words = kw.lower().split()
                if all(word in title_lower for word in kw_words):
                    return role
        return 'autre'

    df['mapped_role'] = df['Titre'].apply(map_title_to_role)
    df.drop(df[df["mapped_role"] == "autre"].index, axis=0, inplace=True)

    # Suppression des doublons
    df.drop('Rôle', axis=1, inplace=True, errors="ignore")  
    df.drop_duplicates(inplace=True)  # Rôle isn't compared
    df.drop_duplicates(subset=["Titre", "Entreprise", "Localisation"], inplace=True)

    df.to_csv(dataset_final_path, index=False)
    return df

#!  Exécution et fusion
for role in roles:
    scrape_linkedin(role)

driver.quit()

new_df = pd.DataFrame(all_offers)
# Merge with existing dataset
try:
    old_df = pd.read_csv(dataset_final_path)
    combined = pd.concat([old_df, new_df], ignore_index=True)
except FileNotFoundError:
    print("Dataset final not found, creating a new one")
    combined = new_df

# Clean and save
cleaned_df = cleaner(combined)
print(f"{len(new_df)} nouvelles offres récupérées. Total après nettoyage: {len(cleaned_df)}")
