import streamlit as st
from streamlit_app.utils.load import load_toml


labels = load_toml('ui_labels')


def show_page():
    # Título do dashboard
    st.title(labels['por_mes']['titulo'])
