"""Dashboard de Atividades da Bolsa de Valores B3."""

import streamlit as st
from streamlit_app.utils.load import load_toml, load_image

labels = load_toml('ui_labels')


def show_page():
    # Título do dashboard
    st.title(labels['home']['titulo'])
    st.write(labels['home']['introducao_painel'])

    col1, cal2 = st.columns(2)

    with col1:
        st.image(
            '/workspace/streamlit_app/assets/imgs/trocapreco.jpeg',
            caption='Trocando preço',
            use_column_width=True,
        )

    with cal2:
        st.image(
            '/workspace/streamlit_app/assets/imgs/abastecer.png',
            caption='Abastecendo',
            use_column_width=True,
        )

    st.subheader(labels['home']['subtitulo'])
    st.write(labels['home']['introducao_dataset'])
