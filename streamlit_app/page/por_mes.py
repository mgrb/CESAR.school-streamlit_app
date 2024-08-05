"""Tela de seleção de mês e estado para análise de dados por mês."""

import pandas as pd
import plotly.express as px
import streamlit as st
from pandas.core.frame import DataFrame
from streamlit_app.utils.load import (
    load_dataset,
    load_meses_refeferencia,
    load_toml,
    load_ufs,
)

labels = load_toml('ui_labels')

# Lista de meses e estados do Brasil
meses = load_meses_refeferencia()
estados = load_ufs()
estados.insert(0, 'Todos')

df_combustiveis = load_dataset('combustiveis-estados')


def montar_grafico(mes: str, data: DataFrame) -> None:
    """Monta o gráfico de análise de dados por mês."""
    df_filtrado = data[(data['referencia'] == mes)]

    # Lista com os nomes das colunas dos preços médios
    precos_medios = [
        'gasolina_comum_preco_revenda_avg',
        'gasolina_aditivada_preco_revenda_avg',
        'etanol_hidratado_preco_revenda_avg',
        'oleo_diesel_preco_revenda_avg',
        'oleo_diesel_s10_preco_revenda_avg',
        'gas_natural_veicular_gnv_preco_revenda_avg',
    ]

    # Adicionar uma nova coluna com a média dos preços médios dos combustíveis
    df_filtrado['media_precos_combustiveis'] = df_filtrado[precos_medios].mean(
        axis=1,
    )
    combustiveis = {
        'Tipo de Combustível': [
            'Gasolina Comum',
            'Gasolina Aditivada',
            'Etanol Hidratado',
            'Óleo Diesel',
            'Óleo Diesel S10',
            'Gás Natural Veicular GNV',
        ],
        'Preço Médio (R$)': [
            df_filtrado['gasolina_comum_preco_revenda_avg'].mean(),
            df_filtrado['gasolina_aditivada_preco_revenda_avg'].mean(),
            df_filtrado['etanol_hidratado_preco_revenda_avg'].mean(),
            df_filtrado['oleo_diesel_preco_revenda_avg'].mean(),
            df_filtrado['oleo_diesel_s10_preco_revenda_avg'].mean(),
            df_filtrado['gas_natural_veicular_gnv_preco_revenda_avg'].mean(),
        ],
    }

    # Criar um dataframe a partir do dicionário
    df_combustiveis = pd.DataFrame(combustiveis)

    # Criar o gráfico de colunas usando plotly.express
    fig = px.bar(
        df_combustiveis,
        x='Tipo de Combustível',
        y='Preço Médio (R$)',
        title='Média dos Preços dos Combustíveis',
        labels={'Preço Médio (R$)': 'Preço Médio (R$)'},
    )

    # Mostrar o gráfico
    st.plotly_chart(fig)


def show_page() -> None:
    """Mostra a página análise de dados por mês."""
    # Título do dashboard
    st.title(labels['por_mes']['titulo'])

    colunas = st.columns(2)
    with colunas[0]:
        mes_selecionado = st.selectbox(
            labels['por_mes']['lbl_select_mes'] + ':', meses
        )

    with colunas[1]:
        estado_selecionado = st.selectbox(
            labels['por_mes']['lbl_select_estado'] + ':', estados
        )

    # Mostrar seleção para verificação
    st.write(f'Você selecionou: {mes_selecionado} e {estado_selecionado}')

    montar_grafico(mes_selecionado, df_combustiveis)
