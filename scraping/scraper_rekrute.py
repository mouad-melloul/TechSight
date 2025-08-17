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
from selenium.common.exceptions import TimeoutException


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
    ,"data engineer","web developer","software engineer"
]

rekrute_base = "https://www.rekrute.com/offres.html?p=1&s=2&o=1&query={query}&keyword={query}&st=d&jobLocation=RK"


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

def scrape_rekrute(role):  # max_pages : nombre maximum de pages à parcourir
    
    url = rekrute_base.format(query=role.replace(" ", "+"))
    try:
        driver.get(url)
    except Exception as e:
        print(f"[ERROR] Failed to load {url} : {e}")

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
    job_cards = soup.find_all("li", class_="post-id")  # Sélectionne chaque carte d’offre
    print(f"{len(job_cards)} offres trouvées pour {role}")

    
    # Pour chaque offre d’emploi trouvée
    for card in job_cards:
        try:
            # Récupère les éléments principaux
            title_tag = card.find("a", class_="titreJob")
            full_title = title_tag.get_text(strip=True) if title_tag else ""
            title_text = full_title.split("|")[0].strip()
            
            img_tag = card.find("img", class_="photo")
            company_name = img_tag["alt"] if img_tag and "alt" in img_tag.attrs else ""

            location = full_title.split("|")[1].strip()
            link_el = card.find("a", href=True, class_="titreJob")

            # Vérifie si l’offre contient un titre et un lien
            if title_tag and link_el:
                role_lower = role.lower()

                #! (removed) if role_lower in title_text:
                job_link = link_el["href"]
                # Convert relative URL to absolute
                if job_link.startswith("/"):
                    job_link = "https://www.rekrute.com" + job_link

                # Ouvre le lien de l’offre dans un nouvel onglet
                driver.execute_script("window.open(arguments[0]);", job_link)
                driver.switch_to.window(driver.window_handles[1])  # Se positionne sur le nouvel onglet
                
                try:
                    wait = WebDriverWait(driver, 10)
                    close_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "close-popup")))
                    close_btn.click()
                    print("Popup fermée avec succès.")
                except TimeoutException:
                    print("Aucun popup détecté, on continue.")

                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "contentbloc")))
                    detail_soup = BeautifulSoup(driver.page_source, "html.parser")
                    description_el = detail_soup.find("div", class_="contentbloc")

                    description_text = ""
                    skills = []

                    if description_el:
                        paragraphs = description_el.find_all(['p', 'li'])
                        description_text = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

                        if not description_text:
                            description_text = description_el.get_text(separator=" ", strip=True)

                        doc = nlp(description_text)
                        matches = matcher(doc)
                        found_skills = set(span.text.lower() for _, start, end in matches for span in [doc[start:end]])
                        skills = sorted(found_skills)
                except :
                    print(f"Description not found")
                    description_el = None


                # Ajoute l’offre à la liste
                all_offers.append({
                    "Source": "rekrute",
                    "Rôle": role,
                    "Titre": title_text,
                    "Entreprise": company_name.strip() if company_name else "",
                    "Localisation": location if location else "",
                    "Lien": job_link,
                    "Compétences": ", ".join(skills)
                })

                driver.close()  # Ferme l’onglet de l’offre
                driver.switch_to.window(driver.window_handles[0])  # Revient à l’onglet principal
                time.sleep(2)  # Petite pause entre les offres
        except Exception as e:
            print(f"[ERROR] Could not process job card: {e}")
            continue

#------- Run -------
for role in roles:
    print(f"Scraping rekrute : {role}")
    scrape_rekrute(role)
    print(f"==> {role} : {len([x for x in all_offers if x['Rôle'] == role])} offres collectées.")
driver.quit()

# ------- Save -------
df = pd.DataFrame(all_offers)
df.to_csv("offres_rekrute.csv", index=False)
print(f"{len(df)} offres enregistrées dans offres_rekrute.csv")
