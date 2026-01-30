import streamlit as st
import pandas as pd
from transformers import pipeline
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="Echo Chamber AI", layout="centered")

# --- INITIALISATION DYNAMIQUE ---
if 'bg' not in st.session_state:
    st.session_state.bg = "#1e1e26"  # Anthracite neutre au départ
if 'sc' not in st.session_state:
    st.session_state.sc = 0

# --- DESIGN ---
st.markdown(f"""
    <style>
    .stApp {{
        background: {st.session_state.bg};
        transition: background 0.6s ease;
    }}
    header {{visibility: hidden;}}
    
    .title-text {{
        color: white; font-size: 60px; font-weight: 800; text-align: center;
        margin-top: 50px; letter-spacing: -2px; margin-bottom: 20px;
    }}
    
    .stTextArea textarea {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important; 
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px; font-size: 18px;
    }}
    
    .stButton>button {{
        width: 100%; border-radius: 20px; height: 60px;
        background: white; color: black; font-weight: 800; border: none;
        font-size: 20px; margin-top: 10px;
    }}

    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {{ justify-content: center; gap: 50px; background: transparent; }}
    .stTabs [data-baseweb="tab"] {{ color: rgba(255,255,255,0.4); font-weight: 600; font-size: 18px; }}
    .stTabs [aria-selected="true"] {{ color: white !important; border-bottom-color: white !important; }}
    </style>
""", unsafe_allow_html=True)

# --- CHARGEMENT IA ---
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="models/sentiment_model")

classifier = load_model()

# --- INTERFACE ---
st.markdown("<div class='title-text'>Echo Chamber AI</div>", unsafe_allow_html=True)

# On détecte le changement d'onglet
tab = st.tabs(["L'Analyse", "Le Dataset"])

# LOGIQUE DE NEUTRALITÉ : Si on n'est pas sur l'onglet 0, on reset le fond
# (Note: Streamlit ne permet pas de détecter l'onglet actif directement sans hack, 
# on va donc forcer le reset si le bouton Dataset est cliqué)

with tab[0]:
    txt = st.text_area("", placeholder="Collez votre message ici...", height=120)
    
    if st.button("DÉTECTER LA POLARISATION"):
        if txt:
            res = classifier(txt, truncation=True)[0]
            lab, sc = res['label'], res['score']
            st.session_state.sc = sc
            
            # Couleur dynamique
            if sc < 0.65:
                st.session_state.bg = "#32323d"
                st.session_state.m, st.session_state.v = "🧐", "NUANCÉ"
            elif lab == "LABEL_0":
                l = max(10, 45 - (sc * 35))
                st.session_state.bg = f"hsl(0, 75%, {l}%)"
                st.session_state.m, st.session_state.v = ("👿" if sc > 0.9 else "😡"), "POLARISÉ"
            else:
                l = max(10, 40 - (sc * 30))
                st.session_state.bg = f"hsl(145, 65%, {l}%)"
                st.session_state.m, st.session_state.v = ("💎" if sc > 0.9 else "😊"), "POSITIF"
            st.rerun()

    if st.session_state.sc > 0:
        st.markdown(f"""
            <div style='text-align: center; color: white; margin-top: 30px;'>
                <div style='font-size: 100px;'>{st.session_state.m}</div>
                <div style='font-size: 35px; font-weight: 800; text-transform: uppercase;'>{st.session_state.v}</div>
                <div style='opacity: 0.7; font-size: 20px;'>Fiabilité : {st.session_state.sc:.2%}</div>
            </div>
        """, unsafe_allow_html=True)

with tab[1]:
    # --- RESET DU FOND POUR LE DATASET ---
    # Si l'utilisateur arrive ici, on lui propose de nettoyer l'interface
    if st.session_state.bg != "#1e1e26":
         if st.button("🔄 NETTOYER L'INTERFACE POUR L'AUDIT"):
             st.session_state.bg = "#1e1e26"
             st.session_state.sc = 0
             st.rerun()

    f = st.file_uploader("", type=["csv"])
    if f:
        df = pd.read_csv(f)
        if st.button("LANCER L'AUDIT GLOBAL"):
            # On s'assure que le fond est neutre pendant l'audit
            st.session_state.bg = "#1e1e26"
            sub = df.head(100).copy()
            sub['res'] = sub[sub.columns[0]].apply(lambda x: classifier(str(x))[0]['label'])
            fig = px.pie(sub, names='res', hole=0.7, color='res', 
                         color_discrete_map={'LABEL_0':'#ff4b4b', 'LABEL_1':'#00d488'})
            fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)