import pandas as pd
import unicodedata



def cleaner(data):

    df = pd.read_csv(data) 
    source = df['Source'].unique()[0]
    df.drop('Source',axis=1,inplace=True)

    for col in df.columns :
        if df[col].dtype == 'object' :
            df[col] = df[col].astype('string')
    
    moroccan_cities = [
        "Casablanca","Rabat", "Tangier","Tanger", "Fez", "Fès", "Marrakesh", "Marrakech", "Salé", "Meknès", "Oujda",
        "Kenitra", "Agadir", "Tetouan", "Tétouan", "Temara", "Safi", "Mohammedia", "Khouribga",
        "El Jadida", "Beni Mellal", "Aït Melloul", "Nador", "Dar Bouazza", "Taza", "Settat",
        "Berrechid", "Khemisset", "Inezgane", "Ksar El Kebir", "Larache", "Guelmim", "Khenifra",
        "Berkane", "Taourirt", "Bouskoura", "Fquih Ben Salah", "Dcheira El Jihadia",
        "Oued Zem", "El Kelaa Des Sraghna", "Sidi Slimane", "Errachidia", "Guercif",
        "Oulad Teima", "Ben Guerir", "Benguerir", "Tifelt", "Lqliaa", "Taroudant", "Sefrou", "Essaouira",
        "Fnideq", "Sidi Kacem", "Tiznit", "Tan-Tan", "Ouarzazate", "Souk El Arbaa",
        "Youssoufia", "Lahraouyine", "Martil", "Ain Harrouda", "Suq as-Sabt Awlad an-Nama",
        "Skhirat", "Ouazzane", "Benslimane", "Al Hoceima", "Beni Ansar", "M'diq", "Sidi Bennour",
        "Midelt", "Azrou", "Drargua", "Laâyoune", "Dakhla", "Taliouine", "Ifrane", "Sala al Jadida"
    ]

    def normalize(text):
        """Lowercase and remove accents."""
        text = text.lower()
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )


    for i, loc in enumerate(df['Localisation']):
        loc_norm = normalize(loc)

        if ',' in loc:
            city_part = normalize(loc.split(',')[0].strip())
            matches = [c for c in moroccan_cities if normalize(c) in city_part]
            if not matches:
                matches = [c for c in moroccan_cities if normalize(c) in loc_norm]
        else:
            matches = [c for c in moroccan_cities if normalize(c) in loc_norm]

        if matches:
            df.loc[i, 'Localisation'] = matches[0]
    
    df.drop_duplicates() 


    role_keywords = {
        "data scientist": [
            "data scientist", "data scientists", "data science"
        ],
        "data analyst": [
            "data analyst", "business analyst","analyste","analyst","data analytics","power bi developer"
        ],
        "data engineer": [
            "data engineer", "big data engineer", "etl developer", "ingénieur data","database engineer"
        ],
        "web developer": [
            "full stack", "full-stack", "python developer", "développeur python", 
            "développeur web", "web developer", "frontend developer", "backend developer",
            "frontend", "backend", "back-end", "front-end"
        ],
        "software engineer": [
            "software engineer", "software developer", "ingénieur logiciel", "développeur logiciel",
            "application developer", "desktop developer", "system developer", "systems engineer","system engineer"
        ]
    }


    def map_title_to_role(title):
        title_lower = title.lower()
        for role, keywords in role_keywords.items():
            for kw in keywords:
                
                if kw.replace(" ", "").strip() in title_lower.replace(" ", ""):
                    return role
                
                kw_words = kw.lower().split()
                if all(word in title_lower for word in kw_words):
                    return role
        return 'autre'



    df['mapped_role'] = df['Titre'].apply(map_title_to_role)
    df.drop('Rôle',axis=1,inplace=True)

    df.to_csv(f"cleaned_data_{source}.csv")

    return df




