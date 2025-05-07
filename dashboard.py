import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Simula um dataframe de reclamações
def gerar_dados_fake():
    produtos = ["Internet", "Pós Pago", "Telefonia", "Tv Por Assinatura"]
    tipos = ["Cancelamento", "Cobrança indevida", "Ma conexão", "Mau atendimento"]
    status = ["Resolvido", "Em andamento", "Não resolvido"]
    local = ["São Paulo", "Rio de Janeiro", "Brasília"]

    data = {
        "Categorias": np.random.choice(produtos, 200),
        "Tipo de Reclamação": np.random.choice(tipos, 200),
        "Status": np.random.choice(status, 200),
        "Data": pd.date_range(end=datetime.date.today(), periods=200).to_pydatetime(),
        "Local": np.random.choice(local, 200)
    }
    return pd.DataFrame(data)

# Análise simulada
def gerar_analise_ia(df):
    total = len(df)
    mais_reclamado = df["Categorias"].value_counts().idxmax()
    tipo_mais_frequente = df["Tipo de Reclamação"].value_counts().idxmax()
    resolucao = df["Status"].value_counts(normalize=True) * 100
    taxa_resolucao = resolucao.get("Resolvido", 0)

    insights = f"""

    🔍 **Resumo da Análise :**

    - Foram processadas **{total} reclamações** no total.
    - A categoria com o maior número de reclamações foi **{mais_reclamado}**, indicando possível foco de insatisfação.
    - O tipo de reclamação mais recorrente foi **{tipo_mais_frequente}**, sugerindo uma área crítica de melhoria.
    - A taxa de resolução atual é de **{taxa_resolucao:.1f}%**, o que pode indicar uma oportunidade de aumentar a eficiência no atendimento.

    📌 **Recomendações:**
    - Reforce os canais de suporte relacionados a **{mais_reclamado}** e **{tipo_mais_frequente}**.
    - Avalie processos internos que impactam diretamente esses pontos.
    - Estabeleça metas de melhoria para aumentar a taxa de resolução e a satisfação do cliente.
    """
    return insights

# --- Interface do Streamlit ---
st.set_page_config(page_title="Análise de Reclamações", layout="wide")

st.title("🚀 Bem-vindo à AnalisIA")
st.markdown("""
Somos especialistas em transformar dados de atendimento ao cliente em **insights poderosos**.
Para começar, envie um arquivo `.csv` com as reclamações da sua empresa ou **use dados simulados** para testar a plataforma.
""")

# Upload de arquivo
arquivo_csv = st.file_uploader("📁 Envie seu arquivo CSV de reclamações", type="csv")
usar_dados_fake = st.button("Ou clique aqui para usar dados simulados")

# Decisão sobre a fonte dos dados
if arquivo_csv is not None:
    df = gerar_dados_fake()
    st.success("✅ Arquivo carregado com sucesso!")
elif usar_dados_fake:
    df = gerar_dados_fake()
    st.info("🔧 Dados simulados carregados.")
else:
    st.stop()  # Para a execução até o usuário interagir

# --- Filtros na barra lateral ---
st.sidebar.title("Filtros")
empresa_filtro = st.sidebar.multiselect("Categorias", options=df["Categorias"].unique(), default=df["Categorias"].unique())
status_filtro = st.sidebar.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())
local_filtro  = st.sidebar.multiselect("Local", options=df["Local"].unique(), default=df["Local"].unique())

# --- Aplicar filtros ---
df_filtrado = df[
    (df["Categorias"].isin(empresa_filtro)) &
    (df["Status"].isin(status_filtro)) &
    (df["Local"].isin(local_filtro))
]

# --- Exibição principal ---
st.title("📊 Análise de Reclamações")
st.metric("Total de Reclamações", len(df_filtrado))
st.metric("Resolvidas", len(df_filtrado[df_filtrado["Status"] == "Resolvido"]))
st.metric("Percentual Resolvido", f"{(len(df_filtrado[df_filtrado['Status'] == 'Resolvido']) / len(df_filtrado) * 100):.1f}%" if len(df_filtrado) else "0%")

st.subheader("Reclamações por Tipo")
st.bar_chart(df_filtrado["Tipo de Reclamação"].value_counts())

st.subheader("Reclamações por Local")
st.bar_chart(df_filtrado["Local"].value_counts())

st.subheader("📌 Conclusões da IA")
st.markdown(gerar_analise_ia(df_filtrado))
