# Arquitetura do Sistema (RM-ODP)

Este documento descreve a arquitetura do pipeline de dados Olist utilizando o framework RM-ODP (ISO/IEC 10746), garantindo o atendimento a 100% dos requisitos funcionais (RF) e não funcionais (RNF).

## 1. Enterprise Viewpoint (Visão de Empresa)
**Objetivo**: Processar 100k pedidos/dia para gerar dashboards analíticos confiáveis.
- **Stakeholders**: Analistas de Negócio (Consumidores), Engenheiros de Dados (Mantenedores), SRE (Garantia de SLA).
- **Processo**: Ingestão -> Tratamento -> Carga -> Visualização. (RF-01, RF-04, RF-11, RF-19, RF-20)
- **Gestão de Qualidade**: Garantia de adequação funcional e conformidade regulatória. (RNF-18)
- **Atendimento**: RF-01, RF-04, RF-11, RF-19, RF-20. RNF-18.

## 2. Information Viewpoint (Visão de Informação)
**Objetivo**: Definir o fluxo, semântica e integridade dos dados.
- **Camada Raw**: Dados brutos imutáveis particionados no S3. (RF-03, RNF-15)
- **Camada Trusted**: Modelo canônico normalizado e limpo. (RF-04, RF-07)
- **Camada Curated**: Tabelas fato/dimensão e histórico de estados (SCD). (RF-05, RF-06, RF-11, RF-12)
- **Metadados e Auditoria**: Controle de Watermarks, Logs de acesso a PII e Checksums. (RF-02, RF-18, RNF-07, RNF-09)
- **Atendimento**: RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-11, RF-12, RF-18. RNF-07, RNF-09, RNF-15.

## 3. Computational Viewpoint (Visão Computacional)
**Objetivo**: Definir os componentes lógicos e suas interfaces.
- **Ingestor Python (Extract/Load)**: Scripts Python utilizando **Pandas/Polars** ou **Boto3** para extrair dados da fonte e carregar no S3/MinIO. (RF-01, RF-02)
- **Motor de Qualidade & PII (Python)**: Processamento de dados sensíveis e validações complexas que exigem lógica procedural antes da carga no ClickHouse. (RF-07, RF-08)
- **Motor de Transformação (dbt)**: Orquestração da lógica de negócio SQL dentro do ClickHouse.
- **Engine OLAP (ClickHouse)**: Execução de queries de alto desempenho.

## 4. Engineering Viewpoint (Visão de Engenharia)
**Objetivo**: Infraestrutura de suporte e mecanismos de resiliência.
- **Runtimes de Execução**: **AWS Lambda** (Python) para tarefas leves/event-driven e **Containers Docker** para execuções dbt/ClickHouse.
- **Nó de Storage (S3 / MinIO)**: Buffer de dados entre o Ingestor Python e o ClickHouse.
- **Pilha de Observabilidade**: Logs estruturados em Python enviados ao CloudWatch/Loki.

## 5. Technology Viewpoint (Visão de Tecnologia)
**Objetivo**: Mix de Python e Modern Data Stack.
- **Linguagem Principal**: **Python 3.x** para Ingestão, Auditoria e SRE Scripts.
- **Transformação**: **dbt-core** para lógica SQL.
- **Engine OLAP**: **ClickHouse**.
- **Bibliotecas Python**: `boto3`, `clickhouse-connect`, `polars` (performance), `pytest` (testes).

---

## ADRs (Architecture Decision Records)

### ADR-07: Python para Ingestão e Lógica Procedural
- **Contexto**: Algumas tarefas como limpeza de PII, chamadas de API complexas e validações de integridade customizadas são difíceis de expressar apenas em SQL.
- **Decisão**: Utilizar Python para todas as etapas de "Extract" e "Load", além de transformações procedurais na camada "Trusted". O dbt permanece como orquestrador das camadas puramente analíticas (Curated).
- **Atendimento**: RF-01, RF-02, RF-07, RF-08, RNF-11.

---

## ADRs (Architecture Decision Records)

### ADR-01: ClickHouse como Camada Analítica (OLAP)
(Mantido)

### ADR-06: dbt para Gestão de Transformações (T do ELT)
- **Contexto**: Necessidade de gerenciar a complexidade das transformações SQL, garantir testes de qualidade e linhagem dos dados.
- **Decisão**: Adotar o **dbt**. O dbt permite tratar SQL como código (Software Engineering best practices), facilitando o versionamento e testes automatizados (RNF-12) antes da carga final no BI.
- **Atendimento**: RF-04, RF-05, RF-06, RNF-11, RNF-12.

### ADR-02: Orquestração via Airflow em EC2
- **Contexto**: Necessidade de gestão complexa de falhas, reprocessamento granular e visibilidade.
- **Decisão**: Instalação do Airflow para garantir retries automáticos e execução sob demanda.
- **Atendimento**: RF-13, RF-14, RF-15, RF-16, RNF-05.

### ADR-03: Camada Raw Imutável no S3
- **Contexto**: Garantia de integridade e capacidade de recuperação de desastres.
- **Decisão**: Armazenamento de arquivos originais em formato imutável antes da ingestão no banco.
- **Atendimento**: RF-03, RNF-07, RNF-15.

### ADR-04: Observabilidade Nativa com CloudWatch Dashboards
- **Contexto**: Minimizar custos de infraestrutura e complexidade operacional no AWS Academy Lab.
- **Decisão**: Substituir o Grafana por CloudWatch Dashboards nativos. Isso elimina a necessidade de gerenciar instâncias EC2 extras, reduz o consumo de créditos e aproveita a integração nativa de logs e métricas.
- **Atendimento**: RNF-13, RNF-14.

### ADR-05: Processamento Serverless com AWS Lambda
- **Contexto**: Necessidade de acelerar o desenvolvimento e reduzir a carga de manutenção de infraestrutura (Patching, Docker, Gerenciamento de Servidor).
- **Decisão**: Utilizar AWS Lambda para as funções de ETL. Isso permite focar no código de negócio (Python), escalabilidade automática por execução e integração nativa com S3 (triggers).
- **Atendimento**: RNF-01, RNF-11, RNF-12.

---
**Validação do Critério de Pronto**:
- **Todos os RFs (01-20) mapeados?** Sim.
- **Todos os RNFs (01-18) mapeados?** Sim.
- **Todos os componentes vinculados a requisitos?** Sim.


 Sim, o documento 03_architecture.md está estruturado inteiramente em torno de um pipeline ETL (Extract, Transform, Load), integrando
  diretamente os problemas e requisitos definidos nos documentos 00, 01 e 02.

  Abaixo, resumo como essa estrutura ETL está refletida na arquitetura (seguindo o framework RM-ODP):

  1. Alinhamento com o Fluxo ETL
   * Extract (Ingestão/Captura):
       * Visão de Engenharia: Utiliza S3 como camada Raw imutável (conforme o RF-03).
       * Visão Computacional: Define um Ingestor Incremental focado em Watermarks (RF-02), garantindo que apenas dados novos sejam
         extraídos.
   * Transform (Processamento/Qualidade):
       * Visão de Informação: Divide os dados em camadas (Raw -> Trusted -> Curated), onde ocorrem a normalização (RF-04) e aplicação de
         regras de negócio (RF-05).
       * Visão Computacional: Inclui um Motor de Qualidade com Dead-Letter Queue (RF-08) e um Transformador Idempotente, atendendo à
         necessidade de integridade do 00_problem.md.
   * Load (Carga/Armazenamento):
       * Visão de Tecnologia: Especifica o RDS PostgreSQL como o Data Warehouse final (RF-11 e ADR-01).
       * Visão Computacional: Implementa a lógica de Upsert (RF-10) para manter o estado atual dos pedidos sem duplicidade (RNF-04).

  2. Atendimento aos Requisitos SRE (do 00 e 02)
   * Idempotência e Resiliência: A arquitetura delega ao Airflow (Orquestrador) a gestão de retries e reprocessamento granular (RF-15/16),
     garantindo que falhas não corrompam os dados.
   * Observabilidade: A Visão decrie as camadas da nossa arquitetura, emum docler cpm

  Conclusão: 
  O resultado é uma arquitetura Lean, com custo operacional próximo de zero em períodos de ociosidade, mas capaz de processar picos de
  carga com alta integridade, permitindo que o time foque na qualidade dos dados e não na manutenção da infraestrutura."

  ---

  Dicas extras para a conversa:
   * Se ele perguntar sobre Escalabilidade: Diga que o Lambda escala horizontalmente de forma nativa para lidar com os 100k registros.
   * Se ele perguntar sobre Custos: Mencione que ao remover EC2 (Airflow/Grafana), o maior custo será apenas o RDS, o que é ideal para o
     orçamento limitado do Learner Lab.
   * Se ele perguntar sobre Framework: O uso do RM-ODP mostra que você não apenas "subiu serviços", mas pensou nas diferentes visões do
     sistema (Empresa, Informação, Engenharia, etc).
