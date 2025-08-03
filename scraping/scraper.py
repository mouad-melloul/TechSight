from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# ------- Configuration du navigateur Chrome pour Selenium -------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

roles = [
    "data analyst", "data scientist", "data engineer",
    "full stack developer", "AI engineer"
]

linkedin_base = "https://www.linkedin.com/jobs/search/?keywords={query}&location=Morocco"
indeed_base = "https://ma.indeed.com/jobs?q={query}&l=Morocco"

all_offers = []

def scrape_linkedin(role, scrolls=10):
    url = linkedin_base.format(query=role.replace(" ", "%20"))
    driver.get(url)
    time.sleep(4)

    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("div", class_="base-card")

    print(f"✅ Found {len(job_cards)} offers on LinkedIn for {role}")

    for card in job_cards:
        title_el = card.find("h3", class_="base-search-card__title")
        company_el = card.find("h4", class_="base-search-card__subtitle")
        location_el = card.find("span", class_="job-search-card__location")
        link_el = card.find("a", href=True)

        if title_el and link_el:
            title_text = title_el.text.strip().lower()
            role_lower = role.lower()

            if role_lower in title_text:
                job_link = link_el["href"]

                # Ouvrir le lien dans un nouvel onglet
                driver.execute_script("window.open(arguments[0]);", job_link)
                driver.switch_to.window(driver.window_handles[1])

                wait = WebDriverWait(driver, 10)
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup")))
                    detail_soup = BeautifulSoup(driver.page_source, "html.parser")
                    description_el = detail_soup.find("div", class_="show-more-less-html__markup")
                except:
                    description_el = None

                skills = []
                if description_el:
                    description_text = description_el.get_text(separator=' ').lower()

                    possible_skills = [
                        "python", "java", "javascript", "c++", "c#", "r", "php", "typescript","html","css","javascript",
                        "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "spark", "hadoop",
                        "sql", "nosql", "mongodb", "mysql", "postgresql", "oracle","aws", "azure", "google cloud", "gcp", "ibm cloud",
                        "docker", "git", "ci/cd", "linux", "airflow", "tableau", "power bi", "machine learning", "deep learning", "natural language processing", "nlp", "computer vision", "reinforcement learning",
                        "rest api", "graphql", "microservices", "agile", "scrum", "excel", "node.js", "react.js", "spring boot", "django"
                    ]

                    for skill in possible_skills:
                        if skill in description_text:
                            skills.append(skill)

                all_offers.append({
                    "Source": "LinkedIn",
                    "Rôle": role,
                    "Titre": title_el.text.strip(),
                    "Entreprise": company_el.text.strip() if company_el else "",
                    "Localisation": location_el.text.strip() if location_el else "",
                    "Lien": job_link,
                    "Compétences": ", ".join(skills)
                })

                # Fermer l’onglet détail et revenir à la page principale
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)


# def scrape_indeed(role, pages=6):
#     role_query = role.replace(" ", "+")
#     for page in range(pages):
#         start = page * 10  # 10 offres par page sur Indeed
#         url = indeed_base.format(query=role_query) + f"&start={start}"
#         driver.get(url)
#         time.sleep(4)  # Attendre que la page charge

#         soup = BeautifulSoup(driver.page_source, "html.parser")
#         job_cards = soup.find_all("div", class_="tapItem")

#         print(f"✅ Found {len(job_cards)} offers on Indeed for {role}, page {page+1}")

#         for card in job_cards:
#             title_el = card.find("h2", class_="jobTitle")
#             company_el = card.find("span", class_="company-name")
#             location_el = card.find("div", class_="text-location")

#             if not title_el:
#                 continue

#             title_text = title_el.text.strip().lower()
#             role_lower = role.lower()

#             # Vérifier que le rôle est bien mentionné dans le titre
#             if role_lower not in title_text:
#                 continue

#             job_link = "https://ma.indeed.com" + card["href"]

#             # Ouvrir le lien dans un nouvel onglet pour récupérer description
#             driver.execute_script("window.open(arguments[0]);", job_link)
#             driver.switch_to.window(driver.window_handles[1])

#             wait = WebDriverWait(driver, 10)
#             try:
#                 wait.until(EC.presence_of_element_located((By.ID, "jobDescriptionText")))
#                 detail_soup = BeautifulSoup(driver.page_source, "html.parser")
#                 description_el = detail_soup.find("div", id="jobDescriptionText")
#             except:
#                 description_el = None

#             skills = []
#             if description_el:
#                 description_text = description_el.get_text(separator=' ').lower()

#                 possible_skills = [
#                     "python", "java", "javascript", "c++", "c#", "r", "php", "typescript","html","css","javascript",
#                     "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "spark", "hadoop",
#                     "sql", "nosql", "mongodb", "mysql", "postgresql", "oracle","aws", "azure", "google cloud", "gcp", "ibm cloud",
#                     "docker", "git", "ci/cd", "linux", "airflow", "tableau", "power bi", "machine learning", "deep learning", "natural language processing", "nlp", "computer vision", "reinforcement learning",
#                     "rest api", "graphql", "microservices", "agile", "scrum", "excel", "node.js", "react.js", "spring boot", "django"
#                 ]

#                 for skill in possible_skills:
#                     if skill in description_text:
#                         skills.append(skill)

#             all_offers.append({
#                 "Source": "Indeed",
#                 "Rôle": role,
#                 "Titre": title_el.text.strip(),
#                 "Entreprise": company_el.text.strip() if company_el else "",
#                 "Localisation": location_el.text.strip() if location_el else "",
#                 "Lien": job_link,
#                 "Compétences": ", ".join(skills)
#             })

#             # Fermer l’onglet détail et revenir à la page principale
#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])
#             time.sleep(2)

#------- Run -------
for role in roles:
    print(f"🔍 Scraping LinkedIn: {role}")
    scrape_linkedin(role)

driver.quit()

# ------- Save -------
df = pd.DataFrame(all_offers)
df.drop_duplicates(subset="Lien", inplace=True)
df.to_csv("offres_it_maroc.csv", index=False)
print(f"✅ {len(df)} offres enregistrées dans offres_it_maroc.csv")
