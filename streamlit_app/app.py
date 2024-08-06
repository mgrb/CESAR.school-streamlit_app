"""Application entry point."""

import streamlit as st

# Page config
st.set_page_config(page_title='Painel de Combustíveis')

import page.home as home_page  # noqa: E402
import page.por_mes as mes_page  # noqa: E402
import page.por_timeseries as timeseries_page  # noqa: E402

# streamlit.errors.StreamlitAPIException: `set_page_config()` can only be called
#  once per app page, and must be called as the first Streamlit command in your
#  script.
from utils.load import load_image  # noqa: E402


def show_page() -> None:
    """Mostra a página inicial do dashboard."""
    st.sidebar.image(load_image('logo-combustiveis.png'), use_column_width=True)

    pages = {
        '🏠 Home': home_page,
        '📄 Análise mensal': mes_page,
        '📊 Histórico geral': timeseries_page,
    }

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio('Go to', list(pages.keys()))

    page = pages[selection]
    page.show_page()


if __name__ == '__main__':
    show_page()
