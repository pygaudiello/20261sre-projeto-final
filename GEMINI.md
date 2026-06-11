# Project Context: Northwind SRE & Data Engineering Challenge

This repository contains the specifications and architectural modeling for a reliable data engineering pipeline. It focuses on the ingestion, processing, and visualization of Northwind marketplace data while ensuring system resilience and data trustworthiness.

## Project Overview

The project implements a **Medallion Architecture pipeline** (Raw → Trusted → Curated) processing orders from CSV files stored in **AWS S3** into a **ClickHouse** analytical database, with **dbt** transformations and **Streamlit** dashboards.

## BASS & ATAM — Architectural Context (NÃO ESQUECER)

> Este contexto documenta os **cenários de qualidade BASS** e as **análises de tradeoff ATAM** aplicadas a cada camada do pipeline. Ao alterar qualquer componente, revise estes princípios para manter a integridade arquitetural.

### BASS Quality Attribute Scenarios (Software Architecture in Practice)

| Atributo | Estímulo | Resposta Arquitetural | Métrica |
|:---|:---|:---|:---|
| **Disponibilidade** | Falha no ClickHouse / S3 indisponível | Retries automáticos via docker-compose healthcheck; dados brutos imutáveis no S3 para reprocessamento | 99.9% disponibilidade para consulta |
| **Performance** | 100k pedidos em um lote diário | Ingestão nativa `s3()` do ClickHouse + paralelismo (ThreadPoolExecutor) | Ingestão + transformação < 10 min |
| **Modificabilidade** | Nova coluna no CSV ou regra de negócio | Alteração centralizada nos modelos dbt (staging/marts); scripts de ingestão isolados | Tempo de implementação < 1 dia |
| **Confiabilidade** | Registro inválido ou duplicado | dbt tests + idempotência (MergeTree ORDER BY) + colunas de auditoria | Zero perda, zero duplicação |

### ATAM Tradeoffs (Architecture Tradeoff Analysis Method)

| Decisão | Benefício (+) | Custo (-) | Onde Impacta |
|:---|:---|:---|:---|
| Ingestão nativa S3 → ClickHouse | Performance altíssima (sem gargalo Python) | Flexibilidade de pré-processamento | `scripts/ingest_data.py` |
| dbt para transformações | Modificabilidade, linhagem, testes versionados | Latência batch (vs streaming) | `dbt_project/models/` |
| ClickHouse como OLAP | Queries sub-segundo para milhões de linhas | Complexidade operacional (partições, índices) | `docker-compose.yml`, Streamlit |
| Docker Compose local + CloudFormation prod | Paridade dev/prod | Duas stacks para manter | `cloudformation.yml`, `docker-compose*.yml` |

### Camadas do Pipeline

1. **Ingestão (Raw):** S3 → ClickHouse via `s3()` function nativa. Arquivos CSV imutáveis.
   - *BASS Performance:* Pipeline paralelo com até 4 workers.
   - *ATAM:* Performance (+) vs flexibilidade de limpeza em Python (-).
2. **Transformação (Trusted → Curated):** dbt models SQL.
   - `staging/stg_pedidos.sql`: Limpeza, cast de tipos, métricas calculadas (approval_hours, delivery_hours).
   - `marts/dim_orders.sql`: Dimensão com classificação de performance (on_time/late).
   - `marts/fact_order_status.sql`: Fato com funil de status (aprovado → transportadora → entregue).
   - *BASS Modifiability:* Regras de negócio centralizadas no dbt.
   - *ATAM:* Modificabilidade (+) vs latência de batch (-).
3. **Camada Analítica (Curated):** ClickHouse + Streamlit.
   - Dashboards consultam `dim_orders` e `fact_order_status` (não as raw).
   - SLOs/SLIs visíveis no dashboard.
   - *BASS Availability:* Healthchecks + dados imutáveis para recovery.

### Modelo de Dados Atual (CSVs no S3)

O dataset real agora contém duas tabelas relacionadas:

**1. `northwind_orders.csv`**
`order_id,customer_id,employee_id,order_date,required_date,shipped_date,ship_via,freight,ship_name,ship_address,ship_city,ship_region,ship_postal_code,ship_country`

**2. `northwind_order_details.csv`**
`order_id,product_id,unit_price,quantity,discount`

**Bucket S3:** `northwind-data-pipeline-{AccountId}`
**CSVs:** `raw/northwind_orders.csv`, `raw/northwind_order_details.csv`

---

## Documentation Structure

- **[Index](documents/00_index.md)**: Map of all documentation files.
- **[Functional Requirements](documents/01_functional_requirements.md)**: RF-01 to RF-20.
- **[Non-Functional Requirements](documents/02_non_functional_requirements.md)**: RNF, SLOs, and SLIs.
- **[Architecture](documents/03_architecture.md)**: RM-ODP 5 viewpoints + BASS & ATAM.
- **[System Design](documents/08_system_design.md)**: Mermaid diagrams and technical narrative.
- **[Test Plans](documents/05_test_plan_load.md, 06_test_plan_security.md, 07_test_plan_modeling.md)**.

## AI Agents & Skills

Specific instructions and skills for AI agents are located in `documents/agents/`.

---

*Note: This GEMINI.md includes BASS & ATAM architectural context. Always review these principles when modifying pipeline components.*
