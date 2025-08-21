import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import numpy as np
import textwrap

# ===========================
# CSS STYLING
# ===========================
st.markdown(
    """
    <style>
    /* Main page background */
    header[data-testid="stHeader"] {
        background-color: #F2F3F2;   
        color: #3B3B3B;
    }
    .stApp {
        background-color: #F2F3F2;
        color: #3B3B3B;
    }
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #0e123e; 
        color: #FFFFFF; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===========================
# PAGE CONFIGURATION
# ===========================
st.set_page_config(
    page_title="Plateforme Emploi Tech",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
# DATA LOAD
# ===========================
df = pd.read_csv("data/dataset_final.csv")

# ===========================
# SIDEBAR
# ===========================
st.sidebar.image("Jobscape.png", width=200)
roles = df['mapped_role'].unique()
selected_role = st.sidebar.selectbox("Choisir un rôle :", roles)

# Filter data based on selection
filtered_df = df[df['mapped_role'] == selected_role]


# ===========================
# CUSTOM TITLE FUNCTION
# ===========================
def section_title(text):
    st.markdown(f"""
        <h3 style='
            margin-top:25px;
            margin-bottom:15px;
            padding:12px 20px;
            background-color:white; /* soft matching with F2F3F2 */
            color:#1F2933; /* dark text for contrast */
            border-left: 3px solid #4D5180;   /*accent color */
            border-radius: 8px;
            font-size:20px;
            font-weight:600;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.08); /* subtle shadow */
        '>{text}</h3>
    """, unsafe_allow_html=True)




from collections import Counter
import re

def get_top_skills(df, n=10):
    skills = []
    for comp in df['Compétences'].dropna().astype(str):
        for skill in comp.split(","):
            skill = skill.strip().lower()
            if skill:
                skills.append(skill)
    skill_counts = dict(Counter(skills))
    top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:n])
    return top_skills

top_skills = get_top_skills(filtered_df, n=10)

st.markdown(
    """
    <style>
    /* Hide the Streamlit header action elements (anchor link) */
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def kpi_card(title, value, color="#E0E2DF"):
    st.markdown(f"""
        <div style="
            background-color:{color};
            padding:10px;
            border-radius:15px;
            text-align:center;
            color:black;
            border-bottom: 6px solid #4D5180;
            box-shadow:2px 2px 10px rgba(0,0,0,0.1);
        ">
            <h3 style="font-size:20px;font-weight:600;color:#1F2933;">{title}</h3>
            <p style="font-size:33px;font-weight:600;">{value}</p>
        </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1: 
    kpi_card("Total Offres", len(filtered_df))

with col2: 
    kpi_card("Entreprises Actives", filtered_df['Entreprise'].nunique())

with col3: 
    kpi_card("Villes", filtered_df['Localisation'].nunique())

with col4: 
    top_skill = next(iter(top_skills.keys()), "N/A")
    kpi_card("Top Compétence", f'"{top_skill.capitalize()}"')



# ===========================
# MAIN LAYOUT: 3 COLUMNS
# ===========================
col1, col2, col3 = st.columns([1.2, 1, 1.2])

# ---------------------------
# COLUMN 1: Top Skills (Bar Chart)
# ---------------------------
with col1:
    # st.write("##### Compétences les plus demandées")
    section_title("Compétences les plus demandées")
    skills = []
    for comp in filtered_df['Compétences'].dropna().astype(str):
        for skill in comp.split(","):
            skill = skill.strip().lower()
            if skill:
                skills.append(skill)

    skill_counts = dict(Counter(skills))
    top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    fig3, ax3 = plt.subplots(figsize=(6, 3.7))
    colors = ["#a6a5e7"]
    ax3.bar(top_skills.keys(), top_skills.values(), color=colors)
    ax3.set_ylabel("Nombre d'occurrences")
    ax3.set_xlabel("Compétence")
    ax3.set_title("Top 10 compétences")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig3)

# ---------------------------
# COLUMN 2: Top Locations (Pie Chart)
# ---------------------------
with col2:
    section_title("Villes les plus fréquentes")
    colors = ["#71a0a5","#acc6aa","#cda715",'#87222d',"#9681f0","#fd9a24","#787376","#623F4C"]
   

    loc_counts = filtered_df[~filtered_df['Localisation'].isin(["Maroc", "Morocco"])]['Localisation'].value_counts().head(10)


    fig1, ax1 = plt.subplots(figsize=(6, 6.5), dpi=100)
    wedges, texts, autotexts = ax1.pie(
        loc_counts,
        labels=None,
        autopct='%1.0f%%',
        startangle=140,
        colors=colors,
        textprops={'fontsize': 15} 
    )

    wrapped_labels = ["\n".join(textwrap.wrap(label, width=12)) for label in loc_counts.index]
    ax1.legend(
        wedges, wrapped_labels, title="Villes",
        bbox_to_anchor=(1.05, 1), loc='upper left',
        fontsize=12,
        handlelength=1,
        handletextpad=0.5,
        borderaxespad=0.5,
        labelspacing=1
    )
    ax1.set(aspect="equal")
    st.pyplot(fig1, clear_figure=True)

# ---------------------------
# COLUMN 3: Top Companies (WordCloud)
# ---------------------------
with col3:
    section_title("Top entreprises par rôle")

    top_companies = filtered_df['Entreprise'].value_counts().head(30)
    
    if top_companies.empty:
        st.info("Pas d'entreprise à afficher pour ce rôle.")
    else:
        companies_dict = {company.replace(" ", "_"): count for company, count in top_companies.items()}

        # Ensure a minimum frequency so words are readable
        min_count = max(1, max(companies_dict.values()) // 2)
        companies_dict = {k: max(v, min_count) for k, v in companies_dict.items()}

        wordcloud = WordCloud(
            width=600,
            height=360,
            background_color="white",
            colormap='cividis',
            random_state=42
        ).generate_from_frequencies(companies_dict)

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.imshow(wordcloud.recolor(random_state=42), interpolation="bilinear")
        ax2.axis("off")
        fig2.canvas.draw()
        st.pyplot(fig2)


# ===========================
# LINE CHART: Nombre d'offres par mois
# ===========================
section_title("Nombre d'offres par mois")

filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], errors='coerce')
filtered_df['YearMonth'] = filtered_df['Date'].dt.to_period('M')
offers_by_month = filtered_df.groupby('YearMonth').size()


fig4, ax4 = plt.subplots(figsize=(8, 4.5))
ax4.plot(
    offers_by_month.index.astype(str),
    offers_by_month.values,
    marker='o',
    linestyle='-',
    linewidth=2.5,
    markersize=8,
    color="#4D5180",          # line color
    markerfacecolor="#a6a5e7",# marker fill
    markeredgecolor="#2D3748" # marker border
)

ax4.set_title(f"Évolution des offres pour {selected_role}", fontsize=15, fontweight="bold", color="#1F2933")
ax4.set_xlabel("Mois", fontsize=12, labelpad=10, color="#374151")
ax4.set_ylabel("Nombre d'offres", fontsize=12, labelpad=10, color="#374151")

ax4.grid(True, which='major', linestyle='--', alpha=0.4)

plt.xticks(rotation=45, fontsize=10, ha="right")
plt.yticks(fontsize=10)

ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig4)


# ===========================
# SECOND ROW: Job Listings Table
# ===========================
section_title("Liste des Offres")
display_df = filtered_df[['Titre', 'Entreprise', 'Localisation','Date','Compétences','Lien']].copy()
st.dataframe(
    display_df,
    column_config={"Lien": st.column_config.LinkColumn("Lien")},
    height=300
)



