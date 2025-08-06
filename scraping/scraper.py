from selenium import webdriver  # Contrôle automatisé d’un navigateur web (ici Chrome).
from selenium.webdriver.chrome.options import Options  # Permet de définir des options comme le mode headless.
from selenium.webdriver.common.by import By  # Pour localiser des éléments HTML (par ID, nom de classe, etc.).
from selenium.webdriver.support.ui import WebDriverWait  # Attente explicite jusqu'à une certaine condition.
from selenium.webdriver.support import expected_conditions as EC  # Conditions à vérifier (élément présent, visible, etc.).
from bs4 import BeautifulSoup  # Pour parser le HTML et extraire les données facilement.
import pandas as pd  # Pour stocker et manipuler les données sous forme de tableau.
import time  # Gérer les pauses entre les actions Selenium.
import spacy  # Traitement automatique du langage naturel (extraction de mots-clés).
from spacy.matcher import PhraseMatcher  # Pour détecter des expressions spécifiques (ex : compétences).



# ------- Configuration du navigateur Chrome pour Selenium -------
chrome_options = Options()
chrome_options.add_argument("--headless")  # Lance Chrome sans interface graphique (invisible).
chrome_options.add_argument("--no-sandbox")  # Nécessaire dans certains environnements (serveurs, Docker).
chrome_options.add_argument("--disable-dev-shm-usage")  # Pour éviter certains bugs de mémoire.
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)  # Initialise le navigateur avec les options.
driver.set_page_load_timeout(30)

roles = [
    "data analyst", "data scientist"
    ,"data engineer","full stack developer"
]

linkedin_base = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/?keywords={query}&location=Morocco"
# "https://www.linkedin.com/jobs/search/?keywords={query}&location=Morocco"

all_offers = []

# Chargement du modèle de langue anglais de spaCy
nlp = spacy.load("en_core_web_sm")

# Define possible skills
possible_skills = [
    "python", "java", "javascript", "c++", "c#", "R", "php", "typescript", "html", "css",
    "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "spark", "hadoop",
    "sql", "nosql", "mongodb", "mysql", "postgresql", "oracle",
    "aws", "azure", "google cloud", "gcp", "ibm cloud",
    "docker", "git", "ci/cd", "linux", "airflow", 
    "tableau", "power bi", "machine learning", "deep learning", "natural language processing", "nlp", 
    "computer vision", "reinforcement learning",
    "rest api", "graphql", "microservices", "agile", "scrum", "excel", 
    "node.js", "react", "spring boot", "django"
]

# Création du matcher spaCy pour détecter les compétences
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # Ignorer la casse
patterns = [nlp.make_doc(skill) for skill in possible_skills]  # Transformer chaque compétence en objet spaCy
matcher.add("SKILLS", patterns)  # Ajouter les motifs au matcher

def scrape_linkedin(role, max_pages=10):  # max_pages : nombre maximum de pages à parcourir
    page = 0
    while page < max_pages:
        # Génère l’URL de recherche
        url = linkedin_base.format(query=role.replace(" ", "%20")) + f"&start={page * 25}"
        try:
            driver.get(url)
        except Exception as e:
            print(f"[ERROR] Failed to load {url} : {e}")
            break
        time.sleep(4)  # Attend que la page charge

        # Scrolling jusqu’en bas de la page pour charger tous les résultats
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Parse le HTML avec BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_cards = soup.find_all("div", class_="base-card")  # Sélectionne chaque carte d’offre
        print(f"Page {page + 1} : {len(job_cards)} offres trouvées pour {role}")

        if not job_cards:
            print(f"No more jobs on page {page + 1} for {role}. Stopping.")
            break
        # Pour chaque offre d’emploi trouvée
        for card in job_cards:
            try:
                # Récupère les éléments principaux
                title_el = card.find("h3", class_="base-search-card__title")
                company_el = card.find("h4", class_="base-search-card__subtitle")
                location_el = card.find("span", class_="job-search-card__location")
                link_el = card.find("a", href=True, class_="base-card__full-link")

                # Vérifie si l’offre contient un titre et un lien
                if title_el and link_el:
                    title_text = title_el.text.strip().lower()
                    role_lower = role.lower()

                    #! (removed) if role_lower in title_text:
                    job_link = link_el["href"]

                    # Ouvre le lien de l’offre dans un nouvel onglet
                    driver.execute_script("window.open(arguments[0]);", job_link)
                    driver.switch_to.window(driver.window_handles[1])  # Se positionne sur le nouvel onglet

                    wait = WebDriverWait(driver, 10)
                    try:
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup")))
                        detail_soup = BeautifulSoup(driver.page_source, "html.parser")
                        description_el = detail_soup.find("div", class_="show-more-less-html__markup")
                    except :
                        print(f"Description not found")
                        description_el = None

                    skills = []
                    if description_el:
                        description_text = description_el.get_text(separator=' ').strip()
                        doc = nlp(description_text)
                        matches = matcher(doc)  # Cherche les compétences dans le texte
                        found_skills = set(span.text.lower() for _, start, end in matches for span in [doc[start:end]])
                        skills = sorted(found_skills)
                    else:
                        print("[DEBUG] No description element found.")

                    # Ajoute l’offre à la liste
                    all_offers.append({
                        "Source": "LinkedIn",
                        "Rôle": role,
                        "Titre": title_el.text.strip(),
                        "Entreprise": company_el.text.strip() if company_el else "",
                        "Localisation": location_el.text.strip() if location_el else "",
                        "Lien": job_link,
                        "Compétences": ", ".join(skills)
                    })

                    driver.close()  # Ferme l’onglet de l’offre
                    driver.switch_to.window(driver.window_handles[0])  # Revient à l’onglet principal
                    time.sleep(2)  # Petite pause entre les offres
            except Exception as e:
                print(f"[ERROR] Could not process job card: {e}")
                continue
        page += 1  # Passe à la page suivante

#------- Run -------
for role in roles:
    print(f"Scraping LinkedIn: {role}")
    scrape_linkedin(role)
    print(f"==> {role} : {len([x for x in all_offers if x['Rôle'] == role])} offres collectées.")
driver.quit()

# ------- Save -------
df = pd.DataFrame(all_offers)
df.to_csv("offres_it_maroc.csv", index=False)
print(f"{len(df)} offres enregistrées dans offres_it_maroc.csv")
