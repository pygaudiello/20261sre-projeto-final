import streamlit as st
import pandas as pd
import clickhouse_connect
import os

st.set_page_config(page_title="Northwind SRE Dashboard", layout="wide")

st.title("Northwind Data Pipeline")
st.markdown("**Pipeline Confiável · SRE · Dados Analíticos Northwind**")

CH_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse")
CH_USER = os.getenv("CLICKHOUSE_USER", "admin")
CH_PASS = os.getenv("CLICKHOUSE_PASSWORD", "password")
CH_DB = os.getenv("CLICKHOUSE_DB", "northwind_db")

@st.cache_resource
def get_client():
    try:
        return clickhouse_connect.get_client(
            host=CH_HOST, username=CH_USER, password=CH_PASS, database=CH_DB
        )
    except Exception:
        return None

client = get_client()

if not client:
    st.error("Não foi possível conectar ao ClickHouse.")
    st.stop()

st.sidebar.success("Conectado ao ClickHouse")
st.sidebar.markdown("---")
st.sidebar.markdown("### SLOs do Pipeline")
st.sidebar.info(
    "**Disponibilidade:** 99.9%\n"
    "**Performance (Ingestão):** <10 min\n"
    "**Confiabilidade:** Zero Perda / Zero Duplicação"
)

# ============================================================
# CARGA DOS DADOS
# ============================================================
try:
    total_orders = client.query("SELECT count() FROM dim_orders").first_row[0]
    total_revenue = client.query("SELECT round(sum(total_revenue), 2) FROM dim_orders").first_row[0]

    perf = client.query_df("""
        SELECT shipping_performance, count() as qtd
        FROM dim_orders GROUP BY shipping_performance ORDER BY qtd DESC
    """)

    avg_days_to_ship = client.query("""
        SELECT round(avg(days_to_ship), 1)
        FROM dim_orders WHERE shipping_performance IN ('on_time','late')
    """).first_row[0]

    on_time_pct = client.query("""
        SELECT round(count() * 100.0 / nullIf((SELECT count() FROM dim_orders), 0), 1)
        FROM dim_orders WHERE shipping_performance = 'on_time'
    """).first_row[0]

    timeline = client.query_df("""
        SELECT toStartOfMonth(order_date) as mes, count() as pedidos, round(sum(total_revenue), 2) as receita
        FROM dim_orders GROUP BY mes ORDER BY mes
    """)

    country_dist = client.query_df("""
        SELECT ship_country, count() as qtd, round(sum(total_revenue), 2) as receita
        FROM dim_orders GROUP BY ship_country ORDER BY receita DESC LIMIT 10
    """)

    sample_raw = client.query_df("""
        SELECT order_id, customer_id, order_date, required_date, shipped_date
        FROM raw_orders LIMIT 5
    """)

    sample_curated = client.query_df("""
        SELECT order_id, ship_country, total_revenue, shipping_performance
        FROM dim_orders LIMIT 5
    """)

except Exception as e:
    st.error(f"Erro ao consultar dados: {e}")
    st.stop()

# ============================================================
# SEÇÃO 1: MÉTRICAS
# ============================================================
st.markdown("## 📊 Visão Geral das Vendas Northwind")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Pedidos", total_orders)
col2.metric("Receita Total", f"${total_revenue:,.2f}")
col3.metric("Entrega no Prazo", f"{on_time_pct}%")
col4.metric("Média Dias para Envio", f"{avg_days_to_ship} dias")

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Performance de Envio")
    if not perf.empty:
        st.bar_chart(perf.set_index("shipping_performance")["qtd"])

with col_b:
    st.subheader("Top 10 Países por Receita")
    if not country_dist.empty:
        st.bar_chart(country_dist.set_index("ship_country")["receita"])

st.markdown("---")

st.subheader("Receita e Pedidos Mensais")
if not timeline.empty:
    st.line_chart(timeline.set_index("mes")[["pedidos", "receita"]])

st.markdown("---")

col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Amostra — Dados Brutos")
    st.dataframe(sample_raw, use_container_width=True, hide_index=True)

with col_f:
    st.subheader("Amostra — Dados Analíticos")
    st.dataframe(sample_curated, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Arquivos Northwind Processados")
st.code("s3://northwind-data-pipeline-403783416520/\n├── raw/northwind_orders.csv\n└── raw/northwind_order_details.csv", language="text")

st.sidebar.info(f"Host: {CH_HOST} | DB: {CH_DB}")
st.sidebar.caption("v2.0 — Pipeline adaptado para Northwind real (Orders + Details)")
