import streamlit as st
from auth2 import ensure_auth
from ui import init_session, clear_chat, chat_ui, export_history
from agent import get_agent

# UI setup
st.set_page_config(page_title="Autonomous ChatBot")
st.markdown("""<style>.stApp { background-color: #d4f9e8; }</style>""", unsafe_allow_html=True)

# Auth
ensure_auth()

# Title
st.title("Autonomous ChatBot Agent (General + SAP HANA DB)")

# Session
init_session()

# Sidebar buttons
if st.sidebar.button("Clear Chat"):
    clear_chat()
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.success("Logged out.")
    st.rerun()

# Chat
agent_executor = get_agent()
chat_ui(agent_executor)

# Export
export_history()
