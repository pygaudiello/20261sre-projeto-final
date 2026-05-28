import streamlit as st
import pandas as pd
import clickhouse_connect
import os

st.set_page_config(page_title="Olist SRE Dashboard", layout="wide")

st.title("Olist Data Pipeline")
st.markdown("**Pipeline Confiável · SRE · Dados Analíticos**")

CH_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse")
CH_USER = os.getenv("CLICKHOUSE_USER", "admin")
CH_PASS = os.getenv("CLICKHOUSE_PASSWORD", "password")
CH_DB = os.getenv("CLICKHOUSE_DB", "olist_db")

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
    "**Performance (100k):** <10 min\n"
    "**Modificabilidade:** <1 dia\n"
    "**Zero Perda / Zero Duplicação**"
)

# ============================================================
# CARGA DOS DADOS
# ============================================================
try:
    total = client.query("SELECT count() FROM dim_orders").first_row[0]

    perf = client.query_df("""
        SELECT delivery_performance, count() as qtd
        FROM dim_orders GROUP BY delivery_performance ORDER BY qtd DESC
    """)

    avg_delivery = client.query("""
        SELECT round(avg(actual_delivery_days), 1)
        FROM dim_orders WHERE delivery_performance IN ('on_time','late')
    """).first_row[0]

    funnel = client.query("""
        SELECT count(), sum(is_approved), sum(is_with_carrier), sum(is_delivered)
        FROM fact_order_status
    """).first_row

    on_time_pct = client.query("""
        SELECT round(count() * 100.0 / nullIf((SELECT count() FROM dim_orders), 0), 1)
        FROM dim_orders WHERE delivery_performance = 'on_time'
    """).first_row[0]

    timeline = client.query_df("""
        SELECT toDate(order_purchase_timestamp) as dia, count() as pedidos
        FROM raw_orders GROUP BY dia ORDER BY dia
    """)

    hour_dist = client.query_df("""
        SELECT toHour(order_purchase_timestamp) as hora, count() as qtd
        FROM raw_orders GROUP BY hora ORDER BY hora
    """)

    status_dist = client.query_df("""
        SELECT order_status, count() as qtd
        FROM raw_orders GROUP BY order_status ORDER BY qtd DESC
    """)

    sample_raw = client.query_df("""
        SELECT order_id, customer_id, order_status,
               order_purchase_timestamp, order_estimated_delivery_date
        FROM raw_orders LIMIT 5
    """)

    sample_curated = client.query_df("""
        SELECT order_id, delivery_performance, actual_delivery_days, approval_hours
        FROM dim_orders LIMIT 5
    """)

except Exception as e:
    st.error(f"Erro ao consultar dados: {e}")
    st.stop()

# ============================================================
# SEÇÃO 1: DADOS DO CSV
# ============================================================
st.markdown("## 📊 Dados dos Pedidos (CSV)")
st.markdown("Métricas e visualizações extraídas dos CSVs carregados no pipeline.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Pedidos", f"{total/1000:.1f}k" if total > 1000 else total)
col2.metric("Entrega no Prazo", f"{on_time_pct}%")
col3.metric("Tempo Médio de Entrega", f"{avg_delivery} dias")
col4.metric("Taxa de Conclusão", f"{funnel[3]/funnel[0]*100:.1f}%" if funnel[0] else "N/A")

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Performance de Entrega")
    if not perf.empty:
        st.bar_chart(perf.set_index("delivery_performance")["qtd"])

with col_b:
    st.subheader("Funil de Processamento")
    if funnel[0] > 0:
        funnel_df = pd.DataFrame({
            "Etapa": ["Total", "Aprovados", "Com Transportadora", "Entregues"],
            "Pedidos": [funnel[0], funnel[1], funnel[2], funnel[3]],
            "%": [
                "100%",
                f"{funnel[1]/funnel[0]*100:.1f}%",
                f"{funnel[2]/funnel[0]*100:.1f}%",
                f"{funnel[3]/funnel[0]*100:.1f}%"
            ]
        })
        st.dataframe(funnel_df, use_container_width=True, hide_index=True)

st.markdown("---")

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Pedidos por Dia")
    if not timeline.empty:
        st.bar_chart(timeline.set_index("dia")["pedidos"])

with col_d:
    st.subheader("Pedidos por Hora do Dia")
    if not hour_dist.empty:
        st.bar_chart(hour_dist.set_index("hora")["qtd"])

st.markdown("---")

col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Distribuição por Status")
    if not status_dist.empty:
        st.dataframe(status_dist, use_container_width=True, hide_index=True)

with col_f:
    st.subheader("Amostra — Dados Brutos (raw_orders)")
    st.dataframe(sample_raw, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Amostra — Dados Analíticos (dim_orders)")
st.dataframe(sample_curated, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Arquivos CSV no S3")
st.code("s3://olist-data-pipeline-403783416520/\n├── raw/data_teste_atualizado.csv  (5 pedidos, 2026)\n└── raw/data_teste_olist.csv     (5 pedidos, 2017-2018)", language="text")
st.caption("Os gráficos acima refletem 100k registros do dataset Olist completo, mais os 10 registros dos CSVs de teste.")

# ============================================================
# SEÇÃO 2: ARQUITETURA
# ============================================================
st.markdown("---")
st.markdown("---")
st.markdown("# 🏗️ Arquitetura do Pipeline")
st.markdown("**Contexto arquitetural — BASS Quality Attributes & ATAM Tradeoffs**")
st.caption("Consulte `GEMINI.md` para a documentação completa. Revise esta seção antes de alterar qualquer componente.")

col_arq1, col_arq2 = st.columns(2)

with col_arq1:
    st.markdown("### BASS — Cenários de Qualidade")
    st.markdown("""
    | Atributo | Métrica | Resposta Arquitetural |
    |:---|---|---|
    | **Disponibilidade** | 99.9% | Retries automáticos + dados imutáveis no S3 |
    | **Performance** | <10 min (100k) | Ingestão nativa S3() + paralelismo Python |
    | **Modificabilidade** | <1 dia | Regras centralizadas no dbt |
    | **Confiabilidade** | Zero perda/dup | MergeTree + colunas de auditoria |
    """)

with col_arq2:
    st.markdown("### ATAM — Tradeoffs Arquiteturais")
    st.markdown("""
    | Decisão | (+) Benefício | (-) Custo |
    |:---|---|---|
    | Ingestão S3 nativo → CH | Performance de carga | Flexibilidade de pré-processamento |
    | dbt para transformação | Modificabilidade e linhagem | Latência de processamento batch |
    | ClickHouse como OLAP | Velocidade de query analítica | Complexidade operacional |
    | Modelo único adaptado | Simplicidade e foco | Riqueza analítica limitada |
    """)

st.markdown("---")

col_fluxo, col_adrs = st.columns(2)

with col_fluxo:
    st.markdown("### Fluxo do Pipeline")
    st.markdown("""
    ```
    S3 (CSV) ──s3()──▶ raw_orders (ClickHouse)
                            │
                    ┌───────┴───────┐
                    ▼               ▼
              stg_pedidos     [dbt models]
              (staging)           │
                          ┌───────┴───────┐
                          ▼               ▼
                    dim_orders    fact_order_status
                  (dimensão)         (fato)
                          │               │
                          └───────┬───────┘
                                  ▼
                          Streamlit Dashboard
    ```
    """)

with col_adrs:
    st.markdown("### ADRs (Architecture Decision Records)")
    st.markdown("""
    - **ADR-01:** ClickHouse como camada analítica
    - **ADR-02:** Orquestração via Airflow (planejado)
    - **ADR-03:** Camada Raw imutável no S3
    - **ADR-05:** Processamento serverless (Lambda)
    - **ADR-06:** dbt para gestão de transformações
    - **ADR-08:** Adaptação para modelo único de pedidos
    """)

st.markdown("---")
st.success("Pipeline íntegro — BASS Quality Attributes documentados e ATAM Tradeoffs mapeados. Consulte `GEMINI.md` para detalhes.")

st.sidebar.info(f"Host: {CH_HOST} | DB: {CH_DB}")
st.sidebar.caption("v1.0 — Pipeline adaptado para modelo único de pedidos")
