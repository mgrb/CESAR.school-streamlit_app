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
    """Monta o gráfico de análise de dados por estado e mês, mostrando os 5 estados com as maiores médias dos combustíveis."""
    df_filtrado = data[(data['referencia'] == mes)]

    # Lista com os nomes das colunas dos preços médios
    precos_medios = {
        'gasolina_comum_preco_revenda_avg': 'Gasolina',
        'gasolina_aditivada_preco_revenda_avg': 'Gasolina Adtv.',
        'etanol_hidratado_preco_revenda_avg': 'Etanol',
        'oleo_diesel_preco_revenda_avg': 'Diesel',
        'oleo_diesel_s10_preco_revenda_avg': 'Diesel S10',
        'gas_natural_veicular_gnv_preco_revenda_avg': 'GNV',
    }

    # Agrupar por estado e calcular a média dos preços médios dos combustíveis
    df_estado = (
        df_filtrado.groupby('estado')[list(precos_medios.keys())]
        .mean()
        .reset_index()
    )

    # Calcular a média das médias dos combustíveis para cada estado
    df_estado['media_das_medias'] = df_estado[list(precos_medios.keys())].mean(
        axis=1
    )

    # Selecionar os 5 estados com as maiores médias das médias dos combustíveis
    top_5_estados = df_estado.nlargest(5, 'media_das_medias')

    # Criar o dataframe de combustíveis para os 5 estados selecionados
    combustiveis = {
        'Estado': [],
        'Combustível': [],
        'Preço Médio (R$)': [],
    }

    # Adicionar os preços médios para cada combustível e estado
    for estado in top_5_estados['estado']:
        for tipo_combustivel, nome in precos_medios.items():
            combustiveis['Estado'].append(estado)
            combustiveis['Combustível'].append(nome)
            combustiveis['Preço Médio (R$)'].append(
                top_5_estados[top_5_estados['estado'] == estado][  # noqa: PD011
                    tipo_combustivel
                ].values[0],
            )

    # Criar um dataframe a partir do dicionário
    df_combustiveis = pd.DataFrame(combustiveis)

    # Criar o gráfico de colunas usando plotly.express
    fig = px.bar(
        df_combustiveis,
        x='Combustível',
        y='Preço Médio (R$)',
        color='Estado',
        # title='',
        labels={'Preço Médio (R$)': 'Preço Médio (R$)'},
        facet_col='Estado',
    )

    st.header(f'As TOP 5 Maiores Médias  por estado para o mês de {mes}')
    # Mostrar o gráfico
    st.plotly_chart(fig)


def montar_colunas_precos_medios(
    cols_avg_estado: list,
    mes_selecionado: str,
    estado_selecionado: str,
    df_combustiveis: DataFrame,
) -> None:
    """Monta as colunas com os preços médios dos combustíveis."""
    colunas_selecionadas = [
        'gasolina_comum_preco_revenda_avg',
        'gasolina_aditivada_preco_revenda_avg',
        'etanol_hidratado_preco_revenda_avg',
        'oleo_diesel_preco_revenda_avg',
        'oleo_diesel_s10_preco_revenda_avg',
        'gas_natural_veicular_gnv_preco_revenda_avg',
    ]

    # Filtrar o dataframe de combustíveis
    if estado_selecionado == 'Todos':
        df_filtrado = df_combustiveis[
            (df_combustiveis['referencia'] == mes_selecionado)
        ]
    else:
        df_filtrado = df_combustiveis[
            (df_combustiveis['referencia'] == mes_selecionado)
            & (df_combustiveis['estado'] == estado_selecionado)
        ]

    # Calcular o preço médio dos combustíveis selecionados em colunas_selecionadas
    precos_medios = df_filtrado[colunas_selecionadas].mean()
    precos_medios = precos_medios.fillna(0)
    # Mostrar os preços médios dos combustíveis
    with cols_avg_estado[0]:
        st.write('Gasolina Comum (R$)')
        st.title(f"{precos_medios['gasolina_comum_preco_revenda_avg']:.2f}")
    with cols_avg_estado[1]:
        st.write('Gasolina Aditivada(R$)')
        st.title(f"{precos_medios['gasolina_aditivada_preco_revenda_avg']:.2f}")
    with cols_avg_estado[2]:
        st.write('Etanol Hidratado(R$)')
        st.title(f"{precos_medios['etanol_hidratado_preco_revenda_avg']:.2f}")
    with cols_avg_estado[3]:
        st.write('Óleo Diesel(R$)')
        st.title(f"{precos_medios['oleo_diesel_preco_revenda_avg']:.2f}")
    with cols_avg_estado[4]:
        st.write('Óleo Diesel S10(R$)')
        st.title(f"{precos_medios['oleo_diesel_s10_preco_revenda_avg']:.2f}")
    with cols_avg_estado[5]:
        st.write('GNV(R$)')
        st.title(
            f"{precos_medios['gas_natural_veicular_gnv_preco_revenda_avg']:.2f}",
        )


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
    st.header(
        f'Preços Médios dos combustíveis em {estado_selecionado} no Ano Mês de {mes_selecionado}'
    )

    cols_avg_estado = st.columns(6)

    montar_colunas_precos_medios(
        cols_avg_estado,
        mes_selecionado,
        estado_selecionado,
        df_combustiveis,
    )

    montar_grafico(mes_selecionado, df_combustiveis)
