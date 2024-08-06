"""Pagina de Análise de Preços de Combustíveis por Time Series."""

import pandas as pd
import plotly.express as px
import streamlit as st
from utils.load import load_dataset, load_toml

labels = load_toml('ui_labels')
df_combustiveis = load_dataset('combustiveis-estados')


def montar_grafico(data: pd.DataFrame) -> None:
    """Monta o gráfico de linhas para análise de preços por time series."""
    # Renomeando as colunas
    data.rename(
        columns={
            'gasolina_comum_preco_revenda_avg': 'Gasolina',
            'gasolina_aditivada_preco_revenda_avg': 'Gasolina Aditivada',
            'etanol_hidratado_preco_revenda_avg': 'Etanol ',
            'oleo_diesel_preco_revenda_avg': 'Óleo Diesel',
            'oleo_diesel_s10_preco_revenda_avg': 'Óleo Diesel S10',
            'gas_natural_veicular_gnv_preco_revenda_avg': 'GNV',
        },
        inplace=True,
    )

    # Garantir que a coluna 'referencia' está no formato datetime
    data['referencia'] = pd.to_datetime(data['referencia'], format='%Y-%m')

    # Criação do gráfico de linhas
    fig = px.line(
        data,
        x='referencia',
        y=[
            'Gasolina',
            'Gasolina Aditivada',
            'Etanol ',
            'Óleo Diesel',
            'Óleo Diesel S10',
            'GNV',
        ],
        labels={
            'referencia': 'Data',
            'value': 'Preço (R$)',
            'variable': 'Média de preços de Combustível',
        },
        title='Preços Médios de Combustíveis ao Longo do Tempo',
    )

    # Exibindo o gráfico na página do Streamlit
    st.plotly_chart(fig)


def show_page() -> None:
    """Mostra a página de análise de preços de combustíveis por time series."""
    # Título do dashboard
    st.title(labels['por_timeseries']['titulo'])

    montar_grafico(df_combustiveis)
