"""Application entry point."""

import streamlit as st
import streamlit_app.page.home as home_page
import streamlit_app.page.por_mes as mes_page
import streamlit_app.page.por_timeseries as timeseries_page
from streamlit_app.utils.load import load_image

# Page config
st.set_page_config(page_title='Combustíveis')

st.sidebar.image(load_image('logo-combustiveis.png'), use_column_width=True)


PAGES = {
    '🏠 Home': home_page,
    '📄 Análise mensal': mes_page,
    '📊 Histórico geral': timeseries_page,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio('Go to', list(PAGES.keys()))

page = PAGES[selection]
page.show_page()
