import streamlit as st
import importlib

st.set_page_config(page_title="Reinhart's Chatbot", page_icon=":material/home:")

plain = st.Page("main_llm.py", title="Plain Chatbot", icon=":material/chat_bubble:")
rag = st.Page("main_rag.py", title="RAG Chatbot", icon=":material/chat_bubble:")

menu = st.navigation([plain, rag])

menu.run()