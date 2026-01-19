import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
import numpy as np
import textwrap

st.set_page_config(
    page_title="Plateforme Emploi Tech",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        background-color: #0f0e0f;   
        color: #F6F6F6;
    }
    .stApp {
        background-color: #0f0e0f;
        color: #F6F6F6;
    }
    section[data-testid="stSidebar"] {
        background-color: #141515 ; 
        color: #F6F6F6; 
    }
    
    /* Sidebar divider */
    .sidebar-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
        margin: 20px 0;
    }
    
    /* Filter section headers */
    .filter-header {
        color: #3b82f6;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 20px;
        margin-bottom: 10px;
        padding-left: 5px;
        border-left: 3px solid #3b82f6;
    }
    
    /* Stats box in sidebar */
    .sidebar-stats {
        background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
        border: 1px solid #3b82f6;
    }
    
    .sidebar-stats-title {
        color: #60a5fa;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .sidebar-stats-value {
        color: white;
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Filter section headers */
    .filter-header {
        color: #3b82f6;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 20px;
        margin-bottom: 10px;
        padding-left: 5px;
        border-left: 3px solid #3b82f6;
    }

   .kpi-card {
        background: #1d1c1c;
        border: 1px solid white;
        border-radius: 18px;
        padding: 22px 20px;
        text-align: center;
        transition: all 0.3s ease;
        color: white; /* default text color */
    }

    .kpi-card:hover {
        background: #9cf35b;
        border: none;
        color: #1d1c1c; /* text color on hover */
    }

    .kpi-card .card-value,
    .kpi-card .card-title {
        transition: color 0.3s ease; /* smooth transition */
        color: inherit; /* inherit from parent */
    }

    .card-value {
        font-size: 28px; 
        font-weight: 800; 
        /* remove color */
    }

    .card-title {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 6px;
        /* remove color */
    }


    .hero-section {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.1) 100%);
        padding: 60px 40px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    .hero-title {
        color: #60a5fa;
        font-size: 48px;
        font-weight: 900;
        margin: 0 0 15px 0;
        letter-spacing: -1px;
        text-shadow: 0 0 30px rgba(96, 165, 250, 0.3);
    }

    .hero-subtitle {
        color: #e0e0e0;
        font-size: 20px;
        margin: 0;
        opacity: 0.95;
        font-weight: 300;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .stat-card:hover::before {
        opacity: 1;
    }

    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
    }
    .stat-card svg {
        width: 52px;
        height: 52px;
    }

    .stat-icon {
        font-size: 40px;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.5));
    }

    .stat-value {
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
        line-height: 1;
    }

    .stat-label {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 10px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #f1f5f9;
        margin: 40px 0 25px 0;
        padding-left: 15px;
        border-left: 4px solid #3b82f6;
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }

    .info-card {
        background: linear-gradient(135deg, #1e293b, #111827);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .info-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.1), transparent);
        transition: left 0.5s ease;
    }

    .info-card:hover::after {
        left: 100%;
    }

    .info-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
        transform: translateY(-4px);
    }

    .info-value {
        font-size: 32px;
        font-weight: 800;
        color: #60a5fa;
        margin-bottom: 8px;
    }

    .info-label {
        font-size: 13px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }


    </style>
    """, unsafe_allow_html=True)

df = pd.read_csv("data/dataset_final.csv")

st.sidebar.image("TechSight.png", width=220)

def kpi_card(title, value):
    st.markdown(f"""
        <div class="kpi-card" style="margin-bottom:4px;">
            <div class="card-value">
                {value}
            </div>
            <div class="card-title">
                {title}
            </div>
        </div>
    """, unsafe_allow_html=True)


# Navigation Menu (for multi-page)
st.sidebar.markdown('<div class="filter-header">Navigation</div>', unsafe_allow_html=True)
page = st.sidebar.radio(
    "",
    ["Accueil", "Analyse par Rôle"],
    label_visibility="collapsed"
)



if page == "Accueil":
    # Hero Section - Nouvelle version
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">
                TechSight Platform
            </h1>
            <p class="hero-subtitle">
                Analysez le marché de l'emploi tech au Maroc en temps réel
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Stats Grid - 4 grandes cartes
    st.markdown("""
        <div class="stats-grid">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 0 0 .75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 0 0-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0 1 12 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 0 1-.673-.38m0 0A2.18 2.18 0 0 1 3 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 0 1 3.413-.387m7.5 0V5.25A2.25 2.25 0 0 0 13.5 3h-3a2.25 2.25 0 0 0-2.25 2.25v.894m7.5 0a48.667 48.667 0 0 0-7.5 0M12 12.75h.008v.008H12v-.008Z" />
                </svg>
                <div class="stat-value">{len(df)}</div>
                <div class="stat-label">Total Offres</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                </svg>
                <div class="stat-value">{df['mapped_role'].nunique()}</div>
                <div class="stat-label">Rôles Disponibles</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
                </svg>
                <div class="stat-value">{df['Entreprise'].nunique()}</div>
                <div class="stat-label">Entreprises</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-card">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                </svg>
                <div class="stat-value">{df['Localisation'].nunique()}</div>
                <div class="stat-label">Villes</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    


if page == "Analyse par Rôle":
    # Role Filter with icon
    roles = sorted(df['mapped_role'].dropna().unique())
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    selected_role = st.sidebar.selectbox(
        "Sélectionnez un rôle",
        roles,
        help="Filtrer les offres par domaine d'expertise"
    )
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Quick Stats in Sidebar
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


    # KPI section 
    col1, col2, col3, col4 = st.columns([0.4, 0.4, 0.7, 0.8])

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
            .head(5)  
        )

        fig1, ax1 = plt.subplots(figsize=(7, 4.5), dpi=120)

        fig1.patch.set_facecolor("#1d1c1c")
        ax1.set_facecolor("#1d1c1c")

        wedges, texts, autotexts = ax1.pie(
            loc_counts,
            labels=None,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors[:len(loc_counts)],
            wedgeprops={
                'width': 0.45,
                'edgecolor': '#1d1c1c',
                'linewidth': 2
            },
            pctdistance=0.75
        )

        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(13)

        # Add city names for top 2 cities
        if len(loc_counts) >= 2:
            # Get top 2 cities
            top_cities = list(loc_counts.index[:2])
            
            # Add text labels for top 2 wedges
            for i, (wedge, city) in enumerate(zip(wedges[:2], top_cities)):
                # Calculate the angle at the center of the wedge
                angle = (wedge.theta2 + wedge.theta1) / 2
                
                # Calculate position (radius of 0.6 to place it on the donut)
                x = 0.6 * np.cos(np.radians(angle))
                y = 0.6 * np.sin(np.radians(angle))
                
                # Add city name
                ax1.text(
                    x, y, 
                    city,
                    ha='center', 
                    va='center',
                    fontsize=11,
                    fontweight='bold',
                    color='white',
                    bbox=dict(
                        boxstyle='round,pad=0.3',
                        facecolor='black',
                        edgecolor='white',
                        alpha=0.7,
                        linewidth=1.5
                    )
                )

        wrapped_labels = [
            f"{label} ({val})"
            for label, val in zip(loc_counts.index, loc_counts.values)
        ]

        legend = ax1.legend(
            wedges,
            wrapped_labels,
            title="Villes (Top 5)",
            bbox_to_anchor=(1.15, 1),
            loc='upper left',
            fontsize=10,
            labelcolor="white",
            frameon=False,
            title_fontsize=12
        )

        plt.setp(legend.get_title(), color="white", fontsize=13, weight='bold')

        ax1.set(aspect="equal")

        fig1.text(
            0.5, 0.98,
            "Répartition géographique des offres",
            fontsize=14,
            fontweight="bold",
            color="white",
            ha="center",
            va="top"
        )

        plt.tight_layout(rect=[0, 0, 1, 0.92])
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
    display_df['Date'] = pd.to_datetime(display_df['Date'])

    st.dataframe(
        display_df,
        column_config={
            "Lien": st.column_config.LinkColumn("Lien", display_text="Postuler"),
            "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY")
        },
        hide_index=True,
        use_container_width=True,
        height=300
    )
