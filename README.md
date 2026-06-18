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

## 🛠️ Táticas Arquiteturais Implementadas (Bass et al.)

Este projeto não apenas segue uma arquitetura moderna, mas implementa **táticas específicas** para garantir os atributos de qualidade desejados:

### 1. Disponibilidade (Availability)
*   **Retries com Exponential Backoff:** Implementado em `scripts/ingest_data.py` (função `ingest_native_s3`) para lidar com instabilidades de rede no S3 ou ClickHouse.
*   **Ping de Prontidão:** O script `scripts/wait_for_clickhouse.py` garante que o pipeline só inicie após a saúde do banco ser confirmada.

### 2. Confiabilidade & Idempotência (Reliability)
*   **Cleanup-before-Ingest:** Em `scripts/ingest_data.py`, implementamos a remoção de registros pré-existentes do mesmo arquivo (`DELETE WHERE source_file = ...`) antes da nova carga, garantindo que o pipeline possa ser reiniciado sem duplicar dados.
*   **Testes Automatizados de Qualidade:** Localizados em `dbt_project/models/schema.yml` e `sources.yml`. Utilizamos testes de `unique`, `not_null` e `relationships` para validar a integridade referencial entre Pedidos e Detalhes.

### 3. Performance
*   **Ingestão Paralela:** Uso de `ThreadPoolExecutor` no Python para carregar múltiplos arquivos simultaneamente.
*   **Native S3 Engine:** Uso da função `s3()` do ClickHouse, que transfere o processamento da carga do Python (lento) para o motor C++ do banco (ultra-rápido).

### 4. Observabilidade (Observability)
*   **Logging Estruturado:** Uso da biblioteca `logging` no Python para rastrear cada etapa do ETL.
*   **Health Dashboard:** O Streamlit (`streamlit_app/app.py`) exibe o status em tempo real da ingestão e dos testes do dbt, servindo como um "Single Pane of Glass" para o estado do sistema.

---

---

## 📈 Inteligência de Negócio (BI) no Streamlit Dashboard

O dashboard Streamlit é a principal interface para explorar os dados e responder a perguntas de negócio cruciais. Ele agora está otimizado para apresentar análises detalhadas, focando na performance de produtos:

### Pergunta Central de Negócio:
**"Quais são os 10 produtos com maior receita líquida acumulada e como essa receita evolui mês a mês ao longo do período do dataset?"**

Para responder a isso, o dashboard apresenta:

#### 1. Ranking dos Top 10 Produtos por Receita Líquida:
*   Uma tabela clara que exibe o `ProductID`, a **Receita Líquida Acumulada** e a **Participação (%)** de cada produto na receita total, ordenada do maior para o menor.

#### 2. Evolução Mensal da Receita dos Top 10 Produtos:
*   Um **gráfico de linhas interativo** onde o Eixo X mostra o mês/ano (`OrderDate`) e o Eixo Y representa a receita líquida. Cada linha no gráfico corresponde a um dos 10 produtos do ranking, permitindo uma visualização fácil da sua trajetória de vendas ao longo do tempo.

#### Regra de Cálculo da Receita Líquida:
A receita líquida é obtida por `Σ (UnitPrice × Quantity × (1 − Discount))`, resultado do `JOIN` das tabelas `orders` e `order_details` via `OrderID`. Esta agregação é feita por `ProductID` (para o ranking) e por mês de `OrderDate` (para a série temporal).

#### Filtros Interativos:
Para uma análise flexível, o dashboard oferece filtros na barra lateral:
*   **Período de Análise**: Permite selecionar um intervalo de datas para focar em períodos específicos.
*   **Filtrar Produtos**: Possibilita selecionar um ou mais `ProductID` para análise focada.

Esta seção do dashboard utiliza a biblioteca Pandas para realizar as transformações e agregações em memória, proporcionando agilidade e flexibilidade na exploração dos dados extraídos das camadas de staging do ClickHouse.

---

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
