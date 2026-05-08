import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Olist SRE Dashboard", layout="wide")

st.title("🚀 Olist Data Pipeline Dashboard")

st.sidebar.header("Configurações")
db_host = os.getenv("CLICKHOUSE_HOST", "clickhouse")

st.write(f"Conectado ao ClickHouse em: `{db_host}`")

# Placeholder for metrics
col1, col2, col3 = st.columns(3)
col1.metric("Pedidos Processados", "100k", "+5%")
col2.metric("SLA de Integridade", "100%", "0%")
col3.metric("Tempo Médio ETL", "42min", "-2min")

st.subheader("Amostra de Dados")
st.info("Aguardando ingestão de dados para exibir tabelas.")
