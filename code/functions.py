import pandas as pd
import unicodedata

def cleaner(df):
    df = df.copy()
    source = df['Source'].unique()[0]
    df.drop('Source', axis=1, inplace=True)

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype('string')

        
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
        loc_norm = normalize(location.split(',')[0] if ',' in location else location)
        # 1. Check synonyms
        for syn, canonical in synonym_to_city.items():
            if syn in loc_norm:
                return canonical

        # 2. Check city list
        for c in moroccan_cities:
            if normalize(c) in loc_norm:
                return c
        return None

    for i, loc in enumerate(df['Localisation']):
        matched_city = map_location_to_city(loc)
        if matched_city:
            df.loc[i, 'Localisation'] = matched_city


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
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset=["Titre", "Entreprise", "Localisation"], inplace=True)
    df.drop('Rôle', axis=1, inplace=True, errors="ignore")

    df.to_csv('../data/dataset.csv', index=False)
    return df