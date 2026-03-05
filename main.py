# importar bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import timedelta

# cache para não baixar dados toda interação
@st.cache_data(ttl=3600)
def carregar_dados(acoes):

    dados = pd.DataFrame()

    for acao in acoes:
        df = yf.download(
            acao,
            period="5y"
        )

        dados[acao] = df["Close"]

    dados = dados.dropna(how="all")

    # reduzir peso do gráfico
    dados = dados.resample("W").mean()

    return dados.round(2)


# lista de ações
acoes = ["VALE3.SA", "PETR4.SA", "SUZB3.SA", "GGBR4.SA"]

# carregar dados
dados = carregar_dados(acoes)

# título
st.title("Commodities Brasil")

st.write(
    "Dashboard interativo com a evolução do preço das principais ações de commodities brasileiras."
)

# filtro de ações
lista_acoes = st.sidebar.multiselect(
    "Escolha as ações",
    dados.columns,
    default=dados.columns
)

if not lista_acoes:
    st.warning("Selecione pelo menos uma ação.")
    st.stop()

dados_filtrados = dados[lista_acoes]

# pegar datas
data_inicial = dados_filtrados.index.min().to_pydatetime()
data_final = dados_filtrados.index.max().to_pydatetime()

# slider de datas
intervalo_data = st.sidebar.slider(
    "Selecione o período",
    min_value=data_inicial,
    max_value=data_final,
    value=(data_inicial, data_final),
    step=timedelta(days=7)
)

# filtrar dados
dados_filtrados = dados_filtrados.loc[
    intervalo_data[0]:intervalo_data[1]
]

# transformar formato para plotly
dados_plot = dados_filtrados.reset_index().melt(
    id_vars="Date",
    var_name="Ação",
    value_name="Preço"
)

# gráfico interativo
fig = px.line(
    dados_plot,
    x="Date",
    y="Preço",
    color="Ação",
    title="Evolução do preço das ações"
)

st.plotly_chart(fig, use_container_width=True)
