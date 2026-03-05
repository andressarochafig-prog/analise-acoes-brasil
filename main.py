# importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta


# função para carregar dados
@st.cache_data
def carregar_dados(acoes):
    dados = yf.download(
        acoes,
        start="2010-01-01",
        end="2024-07-01"
    )["Close"]

    # remover linhas totalmente vazias
    dados = dados.dropna(how="all")

    return dados


# lista de ações (commodities brasileiras)
acoes = ["VALE3.SA", "PETR4.SA", "SUZB3.SA", "GGBR4.SA"]

# carregar dados
dados = carregar_dados(acoes)

# título do app
st.write("""
# Commodities Brasil
O gráfico da evolução do preço das ações ao longo dos anos.
""")

# filtro de ações
lista_acoes = st.sidebar.multiselect(
    "Escolha as ações para visualizar",
    dados.columns,
    default=dados.columns
)

if not lista_acoes:
    st.warning("Selecione pelo menos uma ação.")
    st.stop()

dados = dados[lista_acoes]

# pegar datas mínima e máxima
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()

# slider de datas
intervalo_data = st.sidebar.slider(
    "Selecione o período",
    min_value=data_inicial,
    max_value=data_final,
    value=(data_inicial, data_final),
    step=timedelta(days=1)
)

# filtrar dados
dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

# gráfico
st.line_chart(dados)
