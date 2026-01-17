import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import numpy as np
import textwrap

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        background-color: #323233;   
        color: #F6F6F6;
    }
    .stApp {
        background-color: #323233;
        color: #F6F6F6;
    }
    section[data-testid="stSidebar"] {
        background-color: #141515; 
        color: #F6F6F6; 
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(
    page_title="Plateforme Emploi Tech",
    layout="wide",
    initial_sidebar_state="expanded"
)


df = pd.read_csv("data/dataset_final.csv")

st.markdown(
    """
    <style>
    /* Style the sidebar selectbox container */
    section[data-testid="stSidebar"] .stSelectbox {
        padding: 5px 10px;
        margin-bottom: 0px;
        padding-bottom:10px;
    }

    /* Style the select text */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        color: #f4f8fa;   /* Text color */
        font-weight: 600;
        font-size: 14px;
        background-color: #323233;  /* Slightly lighter than container */
        border-radius: 8px;
    }

    /* Style the label/title of the selectbox */
    section[data-testid="stSidebar"] label {
        color: #f4f8fa;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar 
st.sidebar.image("TechSight.png", width=220)
roles = df['mapped_role'].unique()
selected_role = st.sidebar.selectbox("Sélectionnez un rôle :", roles)
filtered_df = df[df['mapped_role'] == selected_role]


# Top skills 
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
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .rounded-chart {
        background-color: #1d1c1c;
        border-radius: 16px;
        padding: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# KPI cards
def kpi_card(title, value, gradient="linear-gradient(135deg, #8b8b8c, #323233)"):
    st.markdown(f"""
        <div style="
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 15px 20px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-top: 10px;
            min-width: 120px;
            background-image: {gradient};
        ">
            <div style="
                font-size: 15px;
                margin-bottom: 5px;
                font-weight: 600;
                opacity: 0.9;
            ">
                {title}
            </div>
            <div style="
                font-size: 26px;
                font-weight: 600;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            ">
                <span>{value}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# KPI section 
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
    top_skill_display = skill_abbr.get(top_skill, top_skill.capitalize())
    kpi_card("Top Skill", top_skill_display)

with col3: 
    colors = ["#dafc64", "#d26f6e", "#a175e1", "#fa7b83",
              "#63744a", "#b0e4db", "#6a9c93", "#8cbfb6",
              "#b0e4db", "#787376", "#623F4C"]

    loc_counts = (
        filtered_df[~filtered_df['Localisation'].isin(["Maroc", "Morocco"])]
        ['Localisation']
        .value_counts()
        .head(10)
    )

    fig1, ax1 = plt.subplots(figsize=(7, 7), dpi=120)

    # Dark background cohérent
    fig1.patch.set_facecolor("#1d1c1c")
    ax1.set_facecolor("#1d1c1c")

    wedges, texts, autotexts = ax1.pie(
        loc_counts,
        labels=None,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops={
            'width': 0.45,
            'edgecolor': '#1d1c1c',
            'linewidth': 2
        },
        pctdistance=0.75
    )

    # Amélioration des labels de pourcentage
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(15)

    # Légende améliorée avec comptage
    wrapped_labels = [
        f"{label} ({val})"
        for label, val in zip(loc_counts.index, loc_counts.values)
    ]

    legend = ax1.legend(
        wedges,
        wrapped_labels,
        title="Villes",
        bbox_to_anchor=(1.15, 1),
        loc='upper left',
        fontsize=11,
        labelcolor="white",
        frameon=False,
        title_fontsize=13
    )

    # Style de la légende
    plt.setp(legend.get_title(), color="white", fontsize=14, weight='bold')

    ax1.set(aspect="equal")

    # Titre principal amélioré
    fig1.text(
        0.5, 0.98,
        "Répartition géographique des offres",
        fontsize=15,
        fontweight="bold",
        color="white",
        ha="center",
        va="top"
    )

    
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
    
    fig3, ax3 = plt.subplots(figsize=(7, 4), dpi=120)
    
    # Gradient de couleurs plus moderne (du foncé au clair)
    colors = [
        "#3b82f6",  # Bleu vif
        "#60a5fa",
        "#7dd3fc",
        "#a5f3fc",
        "#6366f1",  # Indigo
        "#818cf8",
        "#c084fc",  # Purple
        "#e879f9",
        "#f0abfc",
        "#fae8ff"
    ]
    
    # Background sombre cohérent
    fig3.patch.set_facecolor("#1d1c1c")
    ax3.set_facecolor("#1d1c1c")
    
    # Création des barres avec effet visuel
    bars = ax3.bar(
        top_skills.keys(), 
        top_skills.values(), 
        color=colors,
        edgecolor='white',
        linewidth=1.5,
        alpha=0.9
    )
    
    # Ajout des valeurs au-dessus des barres
    for bar in bars:
        height = bar.get_height()
        ax3.text(
            bar.get_x() + bar.get_width()/2., 
            height,
            f'{int(height)}',
            ha='center', 
            va='bottom',
            color='white',
            fontsize=9,
            fontweight='bold'
        )
    
    # Grille plus subtile
    ax3.grid(axis="y", linestyle="--", alpha=0.3, color='gray')
    ax3.set_axisbelow(True)
    
    # Labels avec couleurs claires
    ax3.set_ylabel(
        "Nombre d'occurrences", 
        fontsize=12, 
        labelpad=10, 
        color="white",
        fontweight='bold'
    )
    ax3.set_xlabel(
        "Compétence",
        fontsize=12, 
        labelpad=10, 
        color="white",
        fontweight='bold'
    )
    
    # Rotation des labels x pour meilleure lisibilité
    ax3.tick_params(axis='x', colors='white', labelsize=10)
    ax3.tick_params(axis='y', colors='white', labelsize=10)
    plt.xticks(rotation=45, ha='right')
    
    # Suppression des bordures supérieure et droite
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('white')
    ax3.spines['bottom'].set_color('white')
    
    # Titre centré et moderne
    fig3.text(
        0.5, 0.98, 
        "Top 10 compétences les plus demandées",
        fontsize=14, 
        fontweight="bold", 
        ha="center", 
        va="top",
        color="white"
    )
    
    
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    st.pyplot(fig3, clear_figure=True)
    

# Companies / Trends / Recents 
col1, col2, col3 = st.columns([1, 1, 0.5])

with col1:
    top_companies = filtered_df['Entreprise'].value_counts().head(5)
    if top_companies.empty:
        st.info("Pas d'entreprise à afficher pour ce rôle.")
    else:
        fig2, ax2 = plt.subplots(figsize=(7, 4.5), dpi=120)
        
        # Dark background
        fig2.patch.set_facecolor("#1d1c1c")
        ax2.set_facecolor("#1d1c1c")
        
        # Palette de couleurs vibrantes
        colors = [
            "#ff6b6b",  # Rouge coral
            "#4ecdc4",  # Turquoise
            "#45b7d1",  # Bleu ciel
            "#96ceb4",  # Vert menthe
            "#ffeaa7"   # Jaune doux
        ]
        
        def truncate_label(label, max_len=20):
            return label if len(label) <= max_len else label[:max_len-3] + "..."
        
        truncated_labels = [truncate_label(name, max_len=20) for name in top_companies.index]
        
        # Barres horizontales avec bordure
        bars = ax2.barh(
            truncated_labels, 
            top_companies.values, 
            color=colors,
            edgecolor='white',
            linewidth=1.5,
            alpha=0.9
        )
        
        # Ajout des valeurs à la fin des barres
        for i, (bar, value) in enumerate(zip(bars, top_companies.values)):
            ax2.text(
                value + 0.5,
                bar.get_y() + bar.get_height()/2,
                f'{int(value)}',
                va='center',
                ha='left',
                color='white',
                fontsize=10,
                fontweight='bold'
            )
        
        # Grille subtile
        ax2.grid(axis="x", linestyle="--", alpha=0.3, color='gray')
        ax2.set_axisbelow(True)
        
        ax2.invert_yaxis()
        
        # Labels en blanc
        ax2.set_xlabel(
            "Nombre d'offres", 
            fontsize=12, 
            labelpad=10, 
            color="white",
            fontweight='bold'
        )
        ax2.set_ylabel(
            "Entreprise", 
            fontsize=12, 
            labelpad=10, 
            color="white",
            fontweight='bold'
        )
        
        # Ticks en blanc
        ax2.tick_params(axis='x', colors='white', labelsize=10)
        ax2.tick_params(axis='y', colors='white', labelsize=10)
        
        # Suppression des bordures
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color('white')
        ax2.spines['bottom'].set_color('white')
        
        # Titre centré
        fig2.text(
            0.5, 0.96, 
            "Top 5 entreprises par rôle",
            fontsize=14, 
            fontweight="bold", 
            ha="center", 
            va="top",
            color="white"
        )
        
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        st.pyplot(fig2, clear_figure=True)

with col2:
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], errors='coerce')
    filtered_df['YearMonth'] = filtered_df['Date'].dt.to_period('M')
    offers_by_month = filtered_df.groupby('YearMonth').size()
    
    fig4, ax4 = plt.subplots(figsize=(7, 4.5), dpi=120)
    
    # Dark background
    fig4.patch.set_facecolor("#1d1c1c")
    ax4.set_facecolor("#1d1c1c")
    
    # Ligne avec gradient et remplissage
    ax4.plot(
        offers_by_month.index.astype(str),
        offers_by_month.values,
        marker='o',
        linestyle='-',
        linewidth=3,
        markersize=10,
        color="#3b82f6",
        markerfacecolor="#60a5fa",
        markeredgecolor="white",
        markeredgewidth=2
    )
    
    # Remplissage sous la courbe
    ax4.fill_between(
        range(len(offers_by_month)),
        offers_by_month.values,
        alpha=0.3,
        color="#3b82f6"
    )
    
    # Ajout des valeurs sur chaque point
    for i, (month, value) in enumerate(zip(offers_by_month.index.astype(str), offers_by_month.values)):
        ax4.text(
            i,
            value + max(offers_by_month.values) * 0.03,
            f'{int(value)}',
            ha='center',
            va='bottom',
            color='white',
            fontsize=9,
            fontweight='bold'
        )
    
    # Labels en blanc
    ax4.set_xlabel(
        "Mois", 
        fontsize=12, 
        labelpad=10, 
        color="white",
        fontweight='bold'
    )
    ax4.set_ylabel(
        "Nombre d'offres", 
        fontsize=12, 
        labelpad=10, 
        color="white",
        fontweight='bold'
    )
    
    # Grille subtile
    ax4.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax4.set_axisbelow(True)
    
    # Ticks en blanc
    ax4.tick_params(axis='x', colors='white', labelsize=9)
    ax4.tick_params(axis='y', colors='white', labelsize=10)
    plt.xticks(rotation=45, ha="right")
    
    # Suppression des bordures
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['left'].set_color('white')
    ax4.spines['bottom'].set_color('white')
    
    # Titre centré
    fig4.text(
        0.5, 0.96, 
        "Évolution du nombre d'offres par mois",
        fontsize=14, 
        fontweight="bold", 
        ha="center", 
        va="top",
        color="white"
    )
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    st.pyplot(fig4, clear_figure=True)

with col3:
    recent_offers = filtered_df[filtered_df['Date'] >= (pd.Timestamp.today() - pd.Timedelta(days=7))]
    kpi_card("Offres récentes", len(recent_offers))

    if not filtered_df.empty and not filtered_df['Date'].isna().all():
        most_active_month = (
            filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).size().idxmax()
        )
        month_name = most_active_month.to_timestamp().strftime("%B")
    else:
        month_name = "N/A"
    kpi_card("Mois le plus actif", month_name)


# Job listings table 
st.markdown(
    "<h3 style='font-size:20px; color:white;'>Liste des offres :</h1>", 
    unsafe_allow_html=True
)
display_df = filtered_df[['Titre', 'Entreprise', 'Localisation','Date','Compétences','Lien']].copy()
st.dataframe(
    display_df,
    column_config={"Lien": st.column_config.LinkColumn("Lien")},
    height=300
)
