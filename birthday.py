import streamlit as st
import datetime
import time
from zoneinfo import ZoneInfo

# ==========================================
# CONFIGURATION & SAMPLE DATA
# ==========================================
RECIPIENT_NAME = "Ir.² Antoine Grosjean"

# Configuration du fuseau horaire pour éviter les décalages sur le serveur
LOCAL_TZ = ZoneInfo("Europe/Brussels")
# Set the expected delivery date for the physical gift (Year, Month, Day, Hour, Minute)
DELIVERY_DATE = datetime.datetime(2026, 8, 12, 18, 30, tzinfo=LOCAL_TZ) 

GIFT_TITLE = "Ceinture La Boucle - The York"
GIFT_DESC = "Elle est actuellement en chemin et arrivera très bientôt."
GIFT_FILENAME = "belt.png"
GIFT_URL = "https://laboucle.com/products/the-york" # Remplacez par le lien exact du produit

PERSONAL_MESSAGE = """
**Joyeux anniversaire Antoine !!!** 🎂

Félicitations pour tes 24 ans ! 

C'est à cet âge avancé qu'on peut enfin souhaiter un joyeux anniversaire à notre ingénieur DIPLOMÉ !

On te souhaite plein de bonheur et de réussite dans le futur !

de Florent, Selim, Louis et Olivier
"""

# ==========================================
# PAGE SETUP & CSS
# ==========================================
st.set_page_config(
    page_title="Joyeux anniversaire !",
    page_icon="🎉",
    layout="centered"
)

# CSS mis à jour pour cibler explicitement le texte (balise p) dans le bouton
st.markdown("""
    <style>
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        border-radius: 15px !important;
        border: 2px solid #DAA520 !important;
        box-shadow: 0 8px 15px rgba(255, 215, 0, 0.4) !important;
        transition: all 0.3s ease !important;
        padding: 15px 10px !important;
    }
    
    /* Ciblage spécifique du texte à l'intérieur du bouton */
    .stButton > button p {
        color: #000 !important;
        font-family: 'Arial Black', 'Impact', sans-serif !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        margin: 0 !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 12px 20px rgba(255, 215, 0, 0.6) !important;
        background: linear-gradient(45deg, #FFEA00, #FFB300) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "gift_opened" not in st.session_state:
    st.session_state.gift_opened = False
if "just_opened" not in st.session_state:
    st.session_state.just_opened = False

# ==========================================
# APP LAYOUT & LOGIC
# ==========================================

# A. HERO SECTION
st.markdown('<h1 style="text-align: center;">Joyeux anniversaire ! 🎉</h1>', unsafe_allow_html=True)
st.markdown(f'<h3 style="text-align: center; opacity: 0.7; margin-bottom: 2rem;">Une livraison spéciale pour {RECIPIENT_NAME}</h3>', unsafe_allow_html=True)

# B. INTERACTIVE REVEAL BUTTON & GIFT DISPLAY
if not st.session_state.gift_opened:
    st.write("### On a un petit quelque chose pour toi...")
    st.write("Ça n'a pas tout à fait réussi à arriver à temps pour le grand jour, parce qu'on est des génies de l'organisation !")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎁 Ouvrir ton cadeau", width='stretch'):
            with st.spinner("Déballage en cours..."):
                time.sleep(1.5) # Suspense simulé
            
            # On met à jour les variables d'état avant de recharger
            st.session_state.gift_opened = True
            st.session_state.just_opened = True
            st.rerun()

else:
    # Déclenchement des effets visuels UNE SEULE FOIS juste après l'ouverture
    if st.session_state.just_opened:
        st.balloons()
        st.session_state.just_opened = False # On réinitialise
    
    img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
    with img_col2:
        try:
            st.image(GIFT_FILENAME, width='stretch')
        except FileNotFoundError:
            st.warning(f"*(Image introuvable. Assurez-vous de placer **{GIFT_FILENAME}** dans le même dossier que app.py !)*")
        
    st.markdown(f"<h3 style='text-align: center;'>{GIFT_TITLE}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{GIFT_DESC}</p>", unsafe_allow_html=True)
    
    # Ajout du bouton vers le lien du produit
    link_col1, link_col2, link_col3 = st.columns([1, 2, 1])
    with link_col2:
        st.link_button("🔗 Voir le produit en ligne", url=GIFT_URL, width='stretch')
    
    st.divider()

    # C. COUNTDOWN TIMER
    st.markdown("#### ⏳ Quand est-ce que ça arrive ?")
    
    # Récupération de l'heure actuelle avec le bon fuseau horaire
    now = datetime.datetime.now(LOCAL_TZ)
    time_diff = DELIVERY_DATE - now
    
    if time_diff.total_seconds() > 0:
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Passage à 3 colonnes pour mieux s'adapter aux écrans mobiles
        col1, col2, col3 = st.columns(3)
        col1.metric("Jours", days)
        col2.metric("Heures", hours)
        col3.metric("Min", minutes)
        
        st.caption("*Note : Actualise cette page pour mettre à jour le compte à rebours !*")
    else:
        st.info("📦 D'après le suivi, ça devrait déjà être livré ! Va vérifier !")

    st.divider()

    # D. PERSONAL MESSAGE SECTION
    with st.expander("💌 Lire ta carte d'anniversaire", expanded=True):
        st.markdown(PERSONAL_MESSAGE)