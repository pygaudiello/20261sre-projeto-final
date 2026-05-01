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
- **Ingestor Incremental**: Módulo de captura via offset/timestamp. (RF-01, RF-02)
- **Motor de Qualidade**: Validação de schemas e segregação para Dead-Letter. (RF-07, RF-08, RNF-15)
- **Transformador Idempotente**: Engine de normalização e unicidade. (RF-04, RF-05, RF-09, RF-10, RNF-04)
- **Interface Analítica**: Camada semântica e queries otimizadas. (RF-19, RF-20, RNF-02)
- **Atendimento**: RF-01, RF-02, RF-04, RF-05, RF-07, RF-08, RF-09, RF-10, RF-19, RF-20. RNF-02, RNF-04, RNF-15.

## 4. Engineering Viewpoint (Visão de Engenharia)
**Objetivo**: Infraestrutura de suporte e mecanismos de resiliência.
- **Orquestrador (Airflow on EC2)**: Gestão de DAGs, Retries, Agendamento e Reprocessamento manual/granular. (RF-13, RF-14, RF-15, RF-16, RNF-01, RNF-05, RNF-11)
- **Nó de Storage (S3)**: Persistência distribuída e portabilidade de formatos (Parquet). (RF-03, RNF-16)
- **Data Warehouse (RDS Postgres)**: Banco analítico com suporte a concorrência e disponibilidade. (RF-11, RNF-06, RNF-17)
- **Pilha de Observabilidade**: Alertas de MTTD, Status do pipeline e Dashboards SRE. (RF-17, RF-18, RNF-13, RNF-14)
- **Atendimento**: RF-03, RF-11, RF-13, RF-14, RF-15, RF-16, RF-17, RF-18. RNF-01, RNF-05, RNF-06, RNF-11, RNF-13, RNF-14, RNF-16, RNF-17.

## 5. Technology Viewpoint (Visão de Tecnologia)
**Objetivo**: Escolha tecnológica limitada ao AWS Academy Learner Lab.
- **Processamento**: Python 3.x com bibliotecas modulares e testes unitários. (RNF-11, RNF-12)
- **Orquestração**: Apache Airflow em Docker (EC2 t3.medium). (RNF-02, RNF-03)
- **Dados**: RDS PostgreSQL (db.t3.micro) e S3 Buckets. (RNF-16)
- **Segurança**: AWS IAM Roles e SSM Parameter Store (Secrets). (RNF-08, RNF-10)
- **Observabilidade**: CloudWatch, SNS e Grafana. (RNF-13, RNF-14)
- **Atendimento**: RNF-02, RNF-03, RNF-08, RNF-10, RNF-11, RNF-12, RNF-13, RNF-14, RNF-16.

---

## ADRs (Architecture Decision Records)

### ADR-01: RDS Postgres como Camada Analítica (Warehouse)
- **Contexto**: Restrição de uso de Redshift no Lab e necessidade de performance em queries analíticas.
- **Decisão**: Utilizar o RDS Postgres com índices otimizados e particionamento.
- **Atendimento**: RNF-02, RNF-06, RNF-16.

### ADR-02: Orquestração via Airflow em EC2
- **Contexto**: Necessidade de gestão complexa de falhas, reprocessamento granular e visibilidade.
- **Decisão**: Instalação do Airflow para garantir retries automáticos e execução sob demanda.
- **Atendimento**: RF-13, RF-14, RF-15, RF-16, RNF-05.

### ADR-03: Camada Raw Imutável no S3
- **Contexto**: Garantia de integridade e capacidade de recuperação de desastres.
- **Decisão**: Armazenamento de arquivos originais em formato imutável antes da ingestão no banco.
- **Atendimento**: RF-03, RNF-07, RNF-15.

---
**Validação do Critério de Pronto**:
- **Todos os RFs (01-20) mapeados?** Sim.
- **Todos os RNFs (01-18) mapeados?** Sim.
- **Todos os componentes vinculados a requisitos?** Sim.
