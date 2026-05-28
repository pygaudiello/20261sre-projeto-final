# Olist SRE & Data Engineering Pipeline

Pipeline de dados em **Medallion Architecture** (Raw → Trusted → Curated) para processamento de pedidos do marketplace Olist, com foco em **SRE**, **BASS Quality Attributes** e **ATAM tradeoffs**.

## Stack

| Camada | Tecnologia |
|:---|---:|
| Storage | AWS S3 |
| OLAP | ClickHouse |
| Transformação | dbt-core (staging → marts) |
| Dashboard | Streamlit |
| Infra | Docker Compose / CloudFormation |

## Dados

O modelo atual no S3 contém uma única tabela de pedidos:
- `raw/data_teste_atualizado.csv` — 5 pedidos (2026)
- `raw/data_teste_olist.csv` — 5 pedidos (2017-2018)

## Pipeline

```
S3 (CSV) → ClickHouse raw_orders (ingestão nativa s3())
         → dbt staging (stg_pedidos)
         → dbt marts (dim_orders, fact_order_status)
         → Streamlit Dashboard
```

## Execução Local

```bash
# 1. Sobe infra
docker compose up -d

# 2. Setup completo (automático)
./scripts/auto_setup.sh
```

## Arquitetura

- **BASS**: Disponibilidade (99.9%), Performance (<10min 100k pedidos), Modificabilidade (<1 dia)
- **ATAM**: Ingestão S3 nativa → Performance vs Flexibilidade; dbt → Modificabilidade vs Latência
- Documentação completa em `/documents/` e `GEMINI.md`
