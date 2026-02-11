import streamlit as st
from snowflake.snowpark.context import get_active_session
import snowflake.cortex
import uuid

# --- 1. CONFIGURATION DE LA PAGE & DESIGN ---
st.set_page_config(
    layout="wide",
    page_title="SnowChat Pro",
    page_icon="❄️",
    initial_sidebar_state="expanded"
)

# Custom CSS pour cacher le menu hamburger et le footer Streamlit (Look plus propre)
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stChatInput {padding-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

session = get_active_session()

# --- 2. FONCTIONS BACKEND (Moteur) ---
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Prompt système un peu plus pro
        st.session_state.messages.append({
            "role": "system", 
            "content": "Tu es SnowChat, un assistant IA expert en données, hébergé sécurisé sur Snowflake. Tu es concis, précis et professionnel."
        })
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())

def save_message(role, content, model):
    """Sauvegarde silencieuse dans Snowflake"""
    safe_content = content.replace("'", "''")
    cid = st.session_state.conversation_id
    query = f"""
    INSERT INTO DB_LAB.CHAT_APP.CONVERSATION_HISTORY (conversation_id, role, content, model_used)
    VALUES ('{cid}', '{role}', '{safe_content}', '{model}')
    """
    try:
        session.sql(query).collect()
    except:
        pass # On ne dérange pas l'utilisateur si la sauvegarde échoue

def get_response(messages, model, temperature):
    """Appel Cortex avec paramètres"""
    prompt_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in messages])
    
    # Configuration avancée (Cortex supporte des options comme la température)
    # Note: Pour COMPLETE simple, on passe juste le prompt et le modèle
    return snowflake.cortex.Complete(model, prompt_text)

# --- 3. INTERFACE UTILISATEUR (Frontend) ---
init_session()

# --- SIDEBAR (Barre latérale) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/ff/Snowflake_Logo.svg", width=50)
    st.title("Paramètres")
    st.markdown("---")
    
    # Sélection du modèle avec description
    st.subheader("🧠 Cerveau de l'IA")
    model = st.selectbox(
        "Modèle sélectionné",
        ["mistral-large", "llama3-70b", "reka-flash", "gemma-7b"],
        index=0,
        help="Mistral-Large est le plus performant pour le raisonnement complexe."
    )
    
    # Slider de température (Simulé pour l'UI, ou implémentable si supported)
    st.subheader("🌡️ Créativité")
    temperature = st.slider("Température", 0.0, 1.0, 0.7, help="0 = Précis, 1 = Créatif")
    
    st.markdown("---")
    st.caption(f"🆔 Session: {st.session_state.conversation_id[:8]}...")
    
    # Bouton de reset stylisé
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": "Tu es un assistant utile."}]
        st.session_state.conversation_id = str(uuid.uuid4())
        st.rerun()

# --- ZONE PRINCIPALE ---

# Titre et introduction
col1, col2 = st.columns([1, 5])
with col1:
    st.write("") # Spacer
    st.write("❄️ **BETA**")
with col2:
    st.title("SnowChat Enterprise")

st.markdown("Bienvenue. Posez vos questions sur vos données ou le développement Cloud.")
st.divider()

# Affichage des messages (Boucle d'affichage)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        # On définit des avatars sympas
        avatar_icon = "👤" if msg["role"] == "user" else "❄️"
        
        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.markdown(msg["content"])

# Zone de saisie (Input)
if prompt := st.chat_input("Écrivez votre message ici..."):
    
    # 1. Action Utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    save_message("user", prompt, model)

    # 2. Action Assistant
    with st.chat_message("assistant", avatar="❄️"):
        # Le spinner donne un effet de "réflexion"
        with st.spinner(f"{model} est en train d'écrire..."):
            try:
                response = get_response(st.session_state.messages, model, temperature)
                st.markdown(response)
                
                # Sauvegarde
                st.session_state.messages.append({"role": "assistant", "content": response})
                save_message("assistant", response, model)
            except Exception as e:
                st.error("Une erreur technique est survenue.")
                st.caption(f"Détail: {e}")