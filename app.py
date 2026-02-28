import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import base64

# ---- Page Config -------------------
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

st.set_page_config(
    page_title="TechSight Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CSS --------------------------
def load_css(filepath):
    with open(filepath, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/main.css")

# ---- Data ------------------------

def load_data():
    return pd.read_csv("data/dataset_final.csv")

df = load_data()

# ---- Helpers ---------------------
def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

def kpi_card(title, value, color="#9cf35b"):
    st.markdown(f"""
        <div class="kpi-card">
            <div class="card-value" style="background: linear-gradient(135deg, {color}, #60a5fa);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                {value}
            </div>
            <div class="card-title">{title}</div>
        </div>
    """, unsafe_allow_html=True)


# ---- Sidebar ----------------------
st.sidebar.image("TechSight-sidebar.png", width=200)
with st.sidebar:
    
    st.markdown(
        '<div class="filter-header">Navigation</div>',
        unsafe_allow_html=True
    )

    if st.button("Accueil", use_container_width=True):
        st.session_state.page = "Accueil"

    if st.button("Analytics", use_container_width=True):
        st.session_state.page = "Analytics"

# ---- ACCUEIL -----------------------
if st.session_state.page == "Accueil":
    img_base64 = get_base64_image("TechSight.png")

    st.markdown(f"""
        <div class="hero-section">
            <div class="hero-text">
                <div class="hero-badge">🇲🇦 Marché Tech Maroc</div>
                <h1 class="hero-title">TechSight</h1>
                <p class="hero-subtitle">
                    TechSight analyse le marché de l'emploi tech au Maroc via web scraping des offres LinkedIn.
                    Transformez les données en insights sur les compétences, tendances et opportunités du secteur.
                </p>
            </div>
            {"<img class='hero-image' src='data:image/png;base64," + img_base64 + "'>" if img_base64 else ""}
        </div>
    """, unsafe_allow_html=True)

    # 4 grandes cartes
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

# ---- ANALYTICS -----------------
elif st.session_state.page == "Analytics":
    
    roles = sorted(df['mapped_role'].dropna().unique())
    selected_role = st.sidebar.selectbox(
        'Choisir un rôle',
        roles,
        help="Filtrer les données par rôle"
    )

    filtered_df = df[df['mapped_role'] == selected_role].copy()

    def get_top_skills(data, n=10):
        skills = [s.strip().lower()
                  for row in data['Compétences'].dropna().astype(str)
                  for s in row.split(",") if s.strip()]
        return dict(Counter(skills).most_common(n))

    top_skills = get_top_skills(filtered_df, n=10)

    # --- KPI ------------------
    col1, col2, col3, col4 = st.columns([0.4, 0.4, 0.7, 0.8])

    with col1:
        kpi_card("Total Offres", len(filtered_df), "#9cf35b")
        kpi_card("Entreprises", filtered_df['Entreprise'].nunique(), "#60a5fa")

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

    # ---- Répartition géo ----------------------
    with col3: 
        colors = ["#9cf35b", "#3b82f6", "#a78bfa", "#f59e0b", "#f87171"]

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
            top_cities = list(loc_counts.index[:2])
            
            for i, (wedge, city) in enumerate(zip(wedges[:2], top_cities)):
               
                angle = (wedge.theta2 + wedge.theta1) / 2
                
                x = 0.6 * np.cos(np.radians(angle))
                y = 0.6 * np.sin(np.radians(angle))
                
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

    # ---- Top 10 Skills ---------------------
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
        
        colors = ["#3b82f6","#60a5fa","#7dd3fc","#a5f3fc",
                  "#6366f1","#818cf8","#c084fc","#e879f9","#f0abfc","#fae8ff"]
        
        fig3.patch.set_facecolor("#1d1c1c")
        ax3.set_facecolor("#1d1c1c")
        
        bars = ax3.bar(
            top_skills.keys(), 
            top_skills.values(), 
            color=colors,
            edgecolor='white',
            linewidth=1.5,
            alpha=0.9
        )
        
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
        
        ax3.grid(axis="y", linestyle="--", alpha=0.3, color='gray')
        ax3.set_axisbelow(True)
        
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
        
        ax3.tick_params(axis='x', colors='white', labelsize=10)
        ax3.tick_params(axis='y', colors='white', labelsize=10)
        plt.xticks(rotation=45, ha='right')
        
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.spines['left'].set_color('white')
        ax3.spines['bottom'].set_color('white')
        
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

    # ---- Companies / Timeline / Recent KPIs ----------------
    col1, col2, col3 = st.columns([1, 1, 0.5])

    with col1:
        top_companies = filtered_df['Entreprise'].value_counts().head(5)
        if top_companies.empty:
            st.info("Pas d'entreprise à afficher pour ce rôle.")
        else:
            fig2, ax2 = plt.subplots(figsize=(7, 4.5), dpi=120)
            
            fig2.patch.set_facecolor("#1d1c1c")
            ax2.set_facecolor("#1d1c1c")
            
            colors = ["#9cf35b","#4ecdc4","#45b7d1","#96ceb4","#ffeaa7"]
            
            def truncate_label(label, max_len=20):
                return label if len(label) <= max_len else label[:max_len-3] + "..."
            
            truncated_labels = [truncate_label(name, max_len=20) for name in top_companies.index]
            
            bars = ax2.barh(
                truncated_labels, 
                top_companies.values, 
                color=colors,
                edgecolor='white',
                linewidth=1.5,
                alpha=0.9
            )
            
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
            
            ax2.grid(axis="x", linestyle="--", alpha=0.3, color='gray')
            ax2.set_axisbelow(True)
            
            ax2.invert_yaxis()
            
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
            
            ax2.tick_params(axis='x', colors='white', labelsize=10)
            ax2.tick_params(axis='y', colors='white', labelsize=10)
            
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color('white')
            ax2.spines['bottom'].set_color('white')
            
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

        
        fig4, ax4 = plt.subplots(figsize=(7, 4.3), dpi=120)
        fig4.patch.set_facecolor("#111113")
        ax4.set_facecolor("#111113")

        x = range(len(offers_by_month))
        ax4.plot(x, offers_by_month.values, marker='o', linestyle='-',
                    linewidth=2.5, markersize=9, color="#3b82f6",
                    markerfacecolor="#9cf35b", markeredgecolor="#111113",
                    markeredgewidth=2)
        ax4.fill_between(x, offers_by_month.values, alpha=0.15, color="#3b82f6")

        peak = max(offers_by_month.values)
        for i, (month, value) in enumerate(zip(offers_by_month.index.astype(str), offers_by_month.values)):
            offset = peak * 0.04
            ax4.text(i, value + offset, f'{int(value)}',
                        ha='center', va='bottom', color='white',
                        fontsize=8, fontweight='bold')

        ax4.set_xticks(list(x))
        ax4.set_xticklabels(offers_by_month.index.astype(str), rotation=40, ha='right')
        ax4.set_xlabel("Mois", fontsize=11, color="white", fontweight='bold', labelpad=8)
        ax4.set_ylabel("Offres", fontsize=11, color="white", fontweight='bold', labelpad=8)
        ax4.grid(True, linestyle='--', alpha=0.2, color='gray')
        ax4.set_axisbelow(True)
        ax4.tick_params(axis='x', colors='white', labelsize=8)
        ax4.tick_params(axis='y', colors='white', labelsize=9)
        for sp in ['top','right']: ax4.spines[sp].set_visible(False)
        ax4.spines['left'].set_color('#1e2030')
        ax4.spines['bottom'].set_color('#1e2030')

        fig4.text(0.5, 0.96, "Évolution des offres par mois",
                    fontsize=13, fontweight="bold", ha="center", va="top", color="white")
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        st.pyplot(fig4, clear_figure=True)
        

    with col3:
        recent_offers = filtered_df[
            filtered_df['Date'] >= (pd.Timestamp.today() - pd.Timedelta(days=7))
        ]
        kpi_card("Offres (7j)", len(recent_offers), "#9cf35b")

        if not filtered_df.empty and not filtered_df['Date'].isna().all():
            most_active_month = (
                filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).size().idxmax()
            )
            month_name = most_active_month.to_timestamp().strftime("%b %Y")
        else:
            month_name = "N/A"
        kpi_card("Mois le + actif", month_name, "#f59e0b")

        
    # ---- Job Table ------------------
    st.markdown('<div class="table-header">Liste des offres</div>', unsafe_allow_html=True)

    display_df = filtered_df[['Titre','Entreprise','Localisation','Date','Compétences','Lien']].copy()
    display_df['Date'] = pd.to_datetime(display_df['Date'])

    st.dataframe(
        display_df,
        column_config={
            "Lien": st.column_config.LinkColumn("Lien", display_text="Postuler ↗"),
            "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY")
        },
        hide_index=True,
        use_container_width=True,
        height=320
    )