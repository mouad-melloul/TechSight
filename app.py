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
st.sidebar.image("TechSight.png", width=220)
roles = df['mapped_role'].unique()
selected_role = st.sidebar.selectbox("Choisir un rôle :", roles)

# Filter data based on selection
filtered_df = df[df['mapped_role'] == selected_role]


# ===========================
# CUSTOM TITLE FUNCTION
# ===========================
# def section_title(text):
#     st.markdown(f"""
#         <h3 style='
#             margin-bottom:15px;
#             padding:12px 20px;
#             background-color:white; /* soft matching with F2F3F2 */
#             color:#1F2933; /* dark text for contrast */
#             border-left: 3px solid #4D5180;   /*accent color */
#             border-radius: 8px;
#             font-size:20px;
#             font-weight:600;
#             box-shadow: 2px 2px 5px rgba(0,0,0,0.08); /* subtle shadow */
#         '>{text}</h3>
#     """, unsafe_allow_html=True)




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

def kpi_card(title, value, color="#FFFFFF"):
    st.markdown(f"""
        <div style="
            background-color:{color};
            margin-bottom:20px;
            border-radius:10px;
            padding-bottom:10px;
            text-align:center;
            color:black;
            box-shadow:2px 2px 10px rgba(0,0,0,0.1);
        ">
            <h3 style="font-size:20px;font-weight:600;color:#1F2933;">{title}</h3>
            <p style="font-size:25px;font-weight:600;color:#326f72;">{value}</p>
        </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([0.4, 0.4, 0.8, 1])

with col1: 
    kpi_card("Total Offres", len(filtered_df))
    kpi_card("Entreprises", filtered_df['Entreprise'].nunique())

with col2: 
    kpi_card("Villes", filtered_df[~filtered_df['Localisation'].isin(["Maroc", "Morocco"])]['Localisation'].nunique())
    skill_abbr = {
    "machine learning": "ML",
    "deep learning": "DL",
    "natural language processing": "NLP",
    "artificial intelligence": "AI"
    }

    top_skill = next(iter(top_skills.keys()), "N/A").lower()

    # Map to abbreviation if exists
    top_skill_display = skill_abbr.get(top_skill, top_skill.capitalize())

    kpi_card("Top Skill", top_skill_display)

with col3: 
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

    fig1.text(0.02, 0.95, "Villes les plus fréquentes", fontsize=14, fontweight="bold", ha="left", va="top")

    st.pyplot(fig1, clear_figure=True)
    

with col4:
    skills = []
    for comp in filtered_df['Compétences'].dropna().astype(str):
        for skill in comp.split(","):
            skill = skill.strip().lower()
            if skill:
                skills.append(skill)

    skill_counts = dict(Counter(skills))
    top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    fig3, ax3 = plt.subplots(figsize=(6, 3.7))
    colors = ["#71a0a5"]

    # Bar chart
    ax3.bar(top_skills.keys(), top_skills.values(), color=colors)

    # Axis labels
    ax3.set_ylabel("Nombre d'occurrences", fontsize=12, labelpad=10, color="#374151")
    ax3.set_xlabel("Compétence",fontsize=12, labelpad=10, color="#374151")

    # Rotate x-ticks
    plt.xticks(rotation=45, ha='right')

    # Add figure-level title (top-left)
    fig3.text(0.02, 0.98, "Top 10 compétences les plus demandées",
              fontsize=10, fontweight="bold", ha="left", va="top")

    plt.tight_layout(rect=[0, 0, 1, 0.90])  # leave space for title
    st.pyplot(fig3)
    


col1, col2, col3 = st.columns([1, 1, 0.5])


with col1:
    top_companies = filtered_df['Entreprise'].value_counts().head(5)

    if top_companies.empty:
        st.info("Pas d'entreprise à afficher pour ce rôle.")
    else:
        fig2, ax2 = plt.subplots(figsize=(6, 3.4))  # taille augmentée pour lisibilité

        # --- Bar chart horizontal ---
        ax2.barh(top_companies.index, top_companies.values, color="#71a0a5")

        # Inverser l'ordre pour que la plus grande soit en haut
        ax2.invert_yaxis()

        # Labels
        ax2.set_xlabel("Nombre d'offres", fontsize=12, labelpad=10, color="#374151")
        ax2.set_ylabel("Entreprise", fontsize=12, labelpad=10, color="#374151")

        # Titre personnalisé
        fig2.text(0.02, 0.98, "Top 5 entreprises par rôle",
                  fontsize=10, fontweight="bold", ha="left", va="top")

        # Supprimer les bordures inutiles
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        plt.tight_layout(rect=[0, 0, 1, 0.90])  # laisser espace pour le titre
        st.pyplot(fig2)


    

with col2:

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

    ax4.set_xlabel("Mois", fontsize=12, labelpad=10, color="#374151")
    ax4.set_ylabel("Nombre d'offres", fontsize=12, labelpad=10, color="#374151")

    ax4.grid(True, which='major', linestyle='--', alpha=0.4)

    plt.xticks(rotation=45, fontsize=10, ha="right")
    plt.yticks(fontsize=10)

    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)

    plt.tight_layout()

        # Add figure-level title (top-left)
    fig4.text(0.02, 0.98, "Évolution du nombre d'offres par mois",
              fontsize=12, fontweight="bold", ha="left", va="top")

    plt.tight_layout(rect=[0, 0, 1, 0.90])  # leave space for title
    st.pyplot(fig4)
    

# ---------------------------
# COLUMN 3: Top Companies (WordCloud)
# ---------------------------
with col3:
    recent_offers = filtered_df[filtered_df['Date'] >= (pd.Timestamp.today() - pd.Timedelta(days=7))]
    kpi_card("Offres récentes", len(recent_offers))

    if not filtered_df.empty and not filtered_df['Date'].isna().all():
        most_active_month = (
            filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).size().idxmax()
        )
        # Convert Period to Timestamp and get month name
        month_name = most_active_month.to_timestamp().strftime("%B")
    else:
        month_name = "N/A"

    kpi_card("Mois le plus actif", month_name)
    

# ===========================
# LINE CHART: Nombre d'offres par mois
# ===========================



# ===========================
# SECOND ROW: Job Listings Table
# ===========================
st.markdown(
    "<h3 style='font-size:20px; color:black;'>Liste des offres</h1>", 
    unsafe_allow_html=True
)
display_df = filtered_df[['Titre', 'Entreprise', 'Localisation','Date','Compétences','Lien']].copy()
st.dataframe(
    display_df,
    column_config={"Lien": st.column_config.LinkColumn("Lien")},
    height=300
)



