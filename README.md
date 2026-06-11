# Northwind SRE & Data Engineering Pipeline

Este projeto implementa um pipeline de dados robusto utilizando a **Medallion Architecture** (Raw → Trusted → Curated) para processar dados do marketplace Northwind. O foco principal é a aplicação de princípios de **SRE (Site Reliability Engineering)**, garantindo confiabilidade, performance e observabilidade através de métricas BASS e análises ATAM.

---

## 🏗️ Arquitetura do Sistema

O pipeline foi desenhado para ser resiliente e escalável, utilizando tecnologias líderes de mercado:

*   **Ingestão (Raw):** Dados brutos armazenados no **AWS S3** e carregados no **ClickHouse** via ingestão nativa `s3()`.
*   **Transformação (Trusted):** O **dbt (data build tool)** realiza a limpeza, tipagem e cálculos iniciais (Staging).
*   **Analítica (Curated):** Modelagem dimensional (Star Schema) no ClickHouse para consultas sub-segundo.
*   **Visualização:** Dashboard interativo em **Streamlit** para monitoramento de KPIs e SLOs.
*   **Infraestrutura:** Provisionamento via **CloudFormation** (AWS) e orquestração local via **Docker Compose**.

---

## 📊 O Dataset (Northwind)

O sistema processa dois datasets principais relacionados:

1.  **`northwind_orders.csv`**: Cabeçalho dos pedidos (datas, clientes, frete, destino).
2.  **`northwind_order_details.csv`**: Detalhes dos itens (produtos, preços unitários, quantidades e descontos).

---

## 🛡️ Pilares SRE (BASS & ATAM)

Para garantir a qualidade arquitetural (conforme *Software Architecture in Practice*), definimos os seguintes cenários:

### BASS Quality Attribute Scenarios
| Atributo | Estímulo | Resposta Arquitetural | Métrica |
| :--- | :--- | :--- | :--- |
| **Disponibilidade** | Falha de container | Healthchecks e autorrecuperação via Docker | 99.9% uptime |
| **Performance** | Carga de grandes volumes | Ingestão paralela nativa no ClickHouse | < 10 min p/ 100k linhas |
| **Modificabilidade** | Nova regra de negócio | Transformações centralizadas em SQL no dbt | Implementação < 1 dia |
| **Confiabilidade** | Dados duplicados | Tabelas `MergeTree` com chaves primárias e deduplicação | Zero duplicação na Curated |

### ATAM Tradeoffs (Análise de Compromisso)
*   **Ingestão Nativa S3 vs Python:** Ganhamos **Performance (+)** extrema ao usar o motor do ClickHouse, mas perdemos **Flexibilidade (-)** de pré-processamento em Python.
*   **Transformação Batch (dbt) vs Streaming:** Ganhamos **Consistência e Linhagem (+)**, aceitando uma **Latência (-) de alguns minutos** para atualização dos dados.

---

## 🚀 Como Executar

### 1. Requisitos
*   Docker e Docker Compose
*   Credenciais AWS (para o bucket S3)

### 2. Setup Local
```bash
# Sobe todos os serviços (ClickHouse, Streamlit, dbt, Ingestion)
docker compose up -d

# O sistema executará automaticamente:
# - Criação das tabelas
# - Ingestão dos dados do S3
# - Transformações do dbt
```

### 3. Acesso
*   **Dashboard Streamlit:** `http://localhost:8501`
*   **ClickHouse HTTP:** `http://localhost:8123`

---

## 📂 Estrutura do Repositório
*   `/dbt_project`: Modelos SQL, testes e documentação de linhagem.
*   `/scripts`: Automações de setup e scripts de ingestão Python.
*   `/streamlit_app`: Código do dashboard de visualização.
*   `/documents`: Documentação técnica detalhada (RFs, RNFs, ADRs).
*   `cloudformation.yml`: Template para deploy em produção na AWS.

---
**Projeto desenvolvido para a disciplina de SRE & Data Engineering.**
