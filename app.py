import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import numpy as np
import textwrap

# --- CSS styling ---
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        background-color: #eeefef;   
        color: #3B3B3B;
    }
    .stApp {
        background-color: #eeefef;
        color: #3B3B3B;
    }
    section[data-testid="stSidebar"] {
        background-color: #32625c; 
        color: #FFFFFF; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Page setup ---
st.set_page_config(
    page_title="Plateforme Emploi Tech",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load data ---
df = pd.read_csv("data/dataset_final.csv")

# --- Sidebar ---
st.sidebar.image("TechSight.png", width=220)
roles = df['mapped_role'].unique()
selected_role = st.sidebar.selectbox("Choisir un rôle :", roles)
filtered_df = df[df['mapped_role'] == selected_role]

# --- Top skills ---
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

# --- Hide Streamlit default icons ---
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

# --- KPI card ---
def kpi_card(title, value, bg_color="#265d56", text_color="#FFFFFF"):
    st.markdown(f"""
        <div style="
            text-align:center;
            margin-top:20px;
        ">
            <div style="
                font-size:16px;
                font-weight:600;
                color:#1F2933;
                margin-bottom:6px;
            ">
                {title}
            </div>
            <div style="
                display:inline-block;
                background-color:{bg_color};
                border-radius:25px;
                padding:5px 28px;
                color:{text_color};
                font-size:24px;
                font-weight:600;
                min-width:150px;
            ">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)


# --- KPI section ---
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
    colors = ["#4b7c74","#bad989","#87ada8","#7ec08c","#8cbfb6","#b0e4db","#6a9c93","#8cbfb6","#b0e4db","#787376","#623F4C"]
    loc_counts = filtered_df[~filtered_df['Localisation'].isin(["Maroc", "Morocco"])]['Localisation'].value_counts().head(10)

    fig1, ax1 = plt.subplots(figsize=(6, 6.5), dpi=100)
    wedges, texts, autotexts = ax1.pie(
        loc_counts,
        labels=None,
        autopct='%1.0f%%',
        startangle=140,
        colors=colors,
        textprops={'fontsize': 18, 'color': 'black'},
        wedgeprops={'width': 0.4},
        pctdistance=0.8
    )

    wrapped_labels = [
        f"{label} ({val*100/loc_counts.sum():.0f}%)" 
        for label, val in zip(loc_counts.index, loc_counts.values)
    ]
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

    fig3, ax3 = plt.subplots(figsize=(6, 3.4))
    colors = ["#37766f","#669986","#78a491","#92b99d","#a5c5a6","#b2ceaf","#c3dab7","#cfe3bc","#d7e7c1","#d9e9c2"]

    ax3.bar(top_skills.keys(), top_skills.values(), color=colors)
    ax3.grid(axis="y", linestyle="--", alpha=0.5)
    ax3.set_ylabel("Nombre d'occurrences", fontsize=12, labelpad=10, color="#374151")
    ax3.set_xlabel("Compétence",fontsize=12, labelpad=10, color="#374151")
    plt.xticks(rotation=45, ha='right')
    fig3.text(0.02, 0.98, "Top 10 compétences les plus demandées",
              fontsize=10, fontweight="bold", ha="left", va="top")
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    st.pyplot(fig3)
    

# --- Companies / Trends / Recents ---
col1, col2, col3 = st.columns([1, 1, 0.5])

with col1:
    top_companies = filtered_df['Entreprise'].value_counts().head(5)
    if top_companies.empty:
        st.info("Pas d'entreprise à afficher pour ce rôle.")
    else:
        fig2, ax2 = plt.subplots(figsize=(6, 3.4))
        colors = ["#37766f","#669986","#78a491","#92b99d","#a5c5a6"]

        def truncate_label(label, max_len=15):
            return label if len(label) <= max_len else label[:max_len-3] + "..."
        truncated_labels = [truncate_label(name, max_len=15) for name in top_companies.index]

        ax2.barh(truncated_labels, top_companies.values, color=colors)
        ax2.grid(axis="x", linestyle="--", alpha=0.5)
        ax2.invert_yaxis()
        ax2.set_xlabel("Nombre d'offres", fontsize=12, labelpad=10, color="#374151")
        ax2.set_ylabel("Entreprise", fontsize=12, labelpad=10, color="#374151")
        fig2.text(0.02, 0.98, "Top 5 entreprises par rôle",
                  fontsize=10, fontweight="bold", ha="left", va="top")
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        plt.tight_layout(rect=[0, 0, 1, 0.90])
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
        color="#37766f",
        markerfacecolor="#78a491",
        markeredgecolor="#2D3748"
    )

    ax4.set_xlabel("Mois", fontsize=12, labelpad=10, color="#374151")
    ax4.set_ylabel("Nombre d'offres", fontsize=12, labelpad=10, color="#374151")
    ax4.grid(True, linestyle='--', alpha=0.4)

    plt.xticks(rotation=45, fontsize=10, ha="right")
    plt.yticks(fontsize=10)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    fig4.text(0.02, 0.98, "Évolution du nombre d'offres par mois",
              fontsize=12, fontweight="bold", ha="left", va="top")
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    st.pyplot(fig4)

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


# --- Job listings table ---
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
