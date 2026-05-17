import streamlit as st
from rag import index_document, query

# Configuration de la page
st.set_page_config(page_title="Mon RAG", page_icon="📄")
st.title("📄 Chatbot RAG")
st.caption("Uploade un document et pose des questions dessus.")

# --- Section Upload ---
st.subheader("1. Uploade ton document")
uploaded_file = st.file_uploader("Choisis un fichier PDF ou TXT", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Indexation en cours..."):
        index_document(uploaded_file)
    st.success(f"✅ Document '{uploaded_file.name}' indexé avec succès !")

# --- Section Chat ---
st.subheader("2. Pose ta question")

# Historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input utilisateur
user_input = st.chat_input("Ta question ici...")

if user_input:
    # Vérifier qu'un doc est uploadé
    if not uploaded_file:
        st.warning("⚠️ Uploade d'abord un document !")
    else:
        # Afficher la question
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Générer et afficher la réponse
        with st.chat_message("assistant"):
            with st.spinner("Recherche en cours..."):
                response = query(user_input)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})