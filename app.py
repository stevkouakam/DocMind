import html as html_lib
import streamlit as st
from rag import index_document, query

st.set_page_config(
    page_title="DocMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 860px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stFileUploader > label { display: none; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent;
    border: 1px solid #334155;
    color: #94a3b8 !important;
    border-radius: 8px;
    font-size: 0.85rem;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #ef4444;
    color: #ef4444 !important;
    background: rgba(239,68,68,0.05);
}

/* ── Chat bubbles ── */
.chat-wrapper { display: flex; flex-direction: column; gap: 0.75rem; padding-bottom: 1rem; }

.msg-row-user { display: flex; justify-content: flex-end; }
.msg-row-assistant { display: flex; justify-content: flex-start; align-items: flex-end; gap: 0.6rem; }

.avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
    background: #1e293b; border: 1px solid #334155;
}

.bubble-user {
    background: #2563eb;
    color: #ffffff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.7rem 1rem;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 2px 12px rgba(37,99,235,0.25);
}

.bubble-assistant {
    background: #f8fafc;
    color: #1e293b;
    border-radius: 18px 18px 18px 4px;
    padding: 0.7rem 1rem;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.6;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* ── Welcome screen ── */
.welcome {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 60vh;
    text-align: center; color: #64748b;
}
.welcome-icon { font-size: 3.5rem; margin-bottom: 1.2rem; }
.welcome h2 { color: #1e293b; font-size: 1.75rem; margin: 0 0 0.5rem 0; }
.welcome p { font-size: 1rem; max-width: 380px; margin: 0 auto; line-height: 1.6; }

/* ── Doc badge ── */
.doc-badge {
    background: rgba(37,99,235,0.1);
    border: 1px solid rgba(37,99,235,0.25);
    border-radius: 8px;
    padding: 0.45rem 0.75rem;
    margin: 0.3rem 0;
    font-size: 0.82rem;
    color: #93c5fd !important;
    display: flex; align-items: center; gap: 0.5rem;
    word-break: break-all;
}

/* ── Section label ── */
.section-label {
    font-size: 0.7rem; font-weight: 600;
    color: #475569 !important; text-transform: uppercase;
    letter-spacing: 0.1em; margin: 0 0 0.5rem 0;
}

.sidebar-divider {
    border: none; border-top: 1px solid #1e293b; margin: 1rem 0;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    border-radius: 12px;
    border: 1.5px solid #e2e8f0;
    font-family: 'Inter', sans-serif;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_docs" not in st.session_state:
    st.session_state.indexed_docs = []


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="padding: 1.5rem 0 1.2rem; border-bottom: 1px solid #1e293b; margin-bottom: 1.2rem; text-align:center;">
            <div style="font-size:2rem;">🧠</div>
            <div style="font-size:1.25rem; font-weight:700; color:#f8fafc; margin-top:0.3rem;">DocMind</div>
            <div style="font-size:0.78rem; color:#475569; margin-top:0.2rem;">Chat with your documents</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Upload a document</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "file",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        if uploaded_file.name not in st.session_state.indexed_docs:
            with st.spinner("Indexing..."):
                index_document(uploaded_file)
            st.session_state.indexed_docs.append(uploaded_file.name)
            st.success("Indexed!")

    if st.session_state.indexed_docs:
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Loaded documents</p>', unsafe_allow_html=True)
        for doc in st.session_state.indexed_docs:
            st.markdown(f'<div class="doc-badge">📄 {html_lib.escape(doc)}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    if st.button("🗑️  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
        <div style="margin-top:2rem; text-align:center;">
            <p style="font-size:0.72rem; color:#334155;">GPT-4o-mini · ChromaDB · LlamaIndex</p>
        </div>
    """, unsafe_allow_html=True)


# ── Main area ─────────────────────────────────────────────────────────────────
has_documents = bool(st.session_state.indexed_docs)

if not st.session_state.messages and not has_documents:
    st.markdown("""
        <div class="welcome">
            <div class="welcome-icon">🧠</div>
            <h2>Welcome to DocMind</h2>
            <p>Upload a PDF or TXT file in the sidebar, then ask any question about its content.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        safe = html_lib.escape(msg["content"]).replace("\n", "<br>")
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="msg-row-user">
                    <div class="bubble-user">{safe}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="msg-row-assistant">
                    <div class="avatar">🧠</div>
                    <div class="bubble-assistant">{safe}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("Ask a question about your document...")

if user_input:
    if not has_documents:
        st.warning("Please upload a document first.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Searching relevant content..."):
            response = query(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
