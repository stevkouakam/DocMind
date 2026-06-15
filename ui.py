import html as html_lib
import streamlit as st
from pathlib import Path


def load_css():
    css = Path("styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def sidebar_header():
    st.markdown("""
        <div class="sidebar-brand">
            <span class="brand-logo">🧠</span>
            <span class="brand-name">DocMind</span>
            <span class="brand-tagline">Chat with your documents</span>
        </div>
    """, unsafe_allow_html=True)


def sidebar_footer():
    st.markdown("""
        <div class="sidebar-footer">
            <p>GPT-4o-mini · ChromaDB · LlamaIndex</p>
        </div>
    """, unsafe_allow_html=True)


def section_label(text: str):
    st.markdown(
        f'<p class="section-label">{html_lib.escape(text)}</p>',
        unsafe_allow_html=True
    )


def divider():
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)


def doc_badge(filename: str):
    st.markdown(
        f'<div class="doc-badge">📄 {html_lib.escape(filename)}</div>',
        unsafe_allow_html=True
    )


def welcome_screen():
    st.markdown("""
        <div class="welcome">
            <span class="welcome-glow">🧠</span>
            <h2 class="welcome-title">Welcome to DocMind</h2>
            <p class="welcome-sub">
                Upload any PDF or text file, then ask questions in plain language.<br>
                Answers come directly from your document.
            </p>
            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">⚡</span>
                    <p class="feature-title">Instant answers</p>
                    <p class="feature-desc">Ask anything — get precise answers from your content in seconds.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🔍</span>
                    <p class="feature-title">Semantic search</p>
                    <p class="feature-desc">Finds relevant passages even when exact words don't match.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">💾</span>
                    <p class="feature-title">Persistent memory</p>
                    <p class="feature-desc">Documents stay indexed across sessions — no need to re-upload.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def chat_history(messages: list):
    for msg in messages:
        safe = html_lib.escape(msg["content"]).replace("\n", "<br>")
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="msg-row-user">
                    <div class="bubble-user">{safe}</div>
                    <div class="avatar-user">YOU</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="msg-row-assistant">
                    <div class="avatar-ai">🧠</div>
                    <div class="bubble-assistant">{safe}</div>
                </div>
            """, unsafe_allow_html=True)
