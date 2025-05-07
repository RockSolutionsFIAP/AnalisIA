import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Simula um dataframe de reclamações
def gerar_dados_fake():
    produtos = ["Internet", "Pós Pago", "Telefonia", "Tv Por Assinatura"]
    tipos = ["Cancelamento", "Cobrança indevida", "Ma conexão", "Mau atendimento"]
    status = ["Resolvido", "Em andamento", "Não resolvido"]
    local = ["São paulo", "Rio de Janeiro", "Brasilia"]

    data = {
        "Categorias": np.random.choice(produtos, 200),
        "Tipo de Reclamação": np.random.choice(tipos, 200),
        "Status": np.random.choice(status, 200),
        "Data": pd.date_range(end=datetime.date.today(), periods=200).to_pydatetime(),
        "Local": np.random.choice(local, 200)
    }

    return pd.DataFrame(data)


def gerar_analise_ia(df):
    total = len(df)
    mais_reclamado = df["Categorias"].value_counts().idxmax()
    tipo_mais_frequente = df["Tipo de Reclamação"].value_counts().idxmax()
    resolucao = df["Status"].value_counts(normalize=True) * 100
    taxa_resolucao = resolucao.get("Resolvido", 0)

    insights = f"""
    🔍 **Análise Simulada por IA:**

    - Foram analisadas **{total} reclamações** nos últimos meses.
    - A categoria com mais reclamações é: **{mais_reclamado}**
    - O tipo de reclamação mais comum é: **{tipo_mais_frequente}**
    - A taxa de resolução está em **{taxa_resolucao:.1f}%**, o que pode indicar oportunidades de melhoria.
    """

    return insights


# Carrega os dados (poderia ser de um CSV, banco, etc.)
df = gerar_dados_fake()

# --- Sidebar: Filtros ---
st.sidebar.title("Filtros")
empresa_filtro = st.sidebar.multiselect("Categorias", options=df["Categorias"].unique(), default=df["Categorias"].unique())
status_filtro = st.sidebar.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())
local_filtro  = st.sidebar.multiselect("Local", options=df["Local"].unique(), default=df["Local"].unique())

# Filtragem
df_filtrado = df[(df["Categorias"].isin(empresa_filtro)) & (df["Status"].isin(status_filtro))]

# --- Layout Principal ---
st.title("Dashboard de Reclamações - Protótipo ReclameAQUI")
st.title("📊 Análise de Reclamações por IA")

st.metric("Total de Reclamações", len(df_filtrado))
st.metric("Reclamações Resolvidas", len(df_filtrado[df_filtrado["Status"] == "Resolvido"]))
st.metric("Percentual Resolvido", f"{(len(df_filtrado[df_filtrado['Status'] == 'Resolvido']) / len(df_filtrado) * 100):.1f}%" if len(df_filtrado) else "0%")

# --- Gráficos ---
st.subheader("Reclamações por Tipo")
st.bar_chart(df_filtrado["Tipo de Reclamação"].value_counts())

st.subheader("Reclamações por Localizacao")
st.bar_chart(df_filtrado["Local"].value_counts())

# "Relatório da IA"
st.subheader("📌 Conclusões da IA")
st.markdown(gerar_analise_ia(df))

