"""Dashboard de Atividades da Bolsa de Valores B3."""

import pandas as pd
import plotly.graph_objs as go
import streamlit as st
import yfinance as yf

# Título do dashboard
st.title('Dashboard de Atividades da Bolsa de Valores B3')

# Seleção de ativos
st.sidebar.header('Selecione o ativo')
ticker = st.sidebar.text_input('Ticker do ativo', 'PETR4.SA')

# Período de análise
st.sidebar.header('Selecione o período')
start_date = st.sidebar.date_input('Data inicial', pd.to_datetime('2024-07-01'))
end_date = st.sidebar.date_input('Data final', pd.to_datetime('today'))


# Função para carregar dados
@st.cache_data
def load_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Carregar dados do ativo.

    Args:
    ----
        ticker (str): Ticker do ativo.
        start_date (str): Data inicial.
        end_date (str): Data final.

    """
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)  # noqa: PD002
    return data


# Carregar dados
data = load_data(ticker, start_date, end_date)

# Mostrar dados
st.subheader('Dados brutos')
st.write(data.tail())

# Gráfico de preços de fechamento
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=data['Date'],
        y=data['Close'],
        mode='lines',
        name=ticker,
    ),
)
fig.update_layout(
    title=f'Preço de Fechamento do Ativo {ticker}',
    xaxis_title='Data',
    yaxis_title='Preço de Fechamento (R$)',
)

st.plotly_chart(fig)
