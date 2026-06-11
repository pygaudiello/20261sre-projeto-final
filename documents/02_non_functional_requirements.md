# Requisitos Não Funcionais (RNF) - Modelo ISO 25010

Este documento define os atributos de qualidade para o pipeline Northwind ETL, estruturados conforme a norma ISO 25010 e priorizados pelo método MoSCoW.

## 1. Eficiência de Desempenho (Performance Efficiency)
Foco na capacidade do sistema de processar 100k pedidos/dia dentro das janelas de negócio.

| ID | Atributo | SLI (Indicador) | SLO (Objetivo) | Fonte | Prioridade |
|:---|:---|:---|:---|:---|:---|
| RNF-01 | Time Behaviour | Tempo total de processamento do lote de 100k. | < 45 minutos | Logs Airflow | Must |
| RNF-02 | Resource Utilization | Consumo de CPU/RAM da instância ETL. | < 70% pico | CloudWatch | Should |
| RNF-03 | Capacity | Suporte a picos de carga (Black Friday). | 500k reg/dia | Stress Test | Could |

## 2. Confiabilidade (Reliability)
O pilar central do projeto: garantir que nenhum dado seja perdido ou duplicado.

| ID | Atributo | SLI (Indicador) | SLO (Objetivo) | Fonte | Prioridade |
|:---|:---|:---|:---|:---|:---|
| RNF-04 | Maturity (Idempotência) | Registros duplicados no DB por `order_id`. | 0 duplicatas | SQL Audit | Must |
| RNF-05 | Recoverability (Auto-recovery) | Sucesso de retries automáticos em falhas. | > 95% sucesso | Airflow Meta | Must |
| RNF-06 | Availability | Disponibilidade do servidor ClickHouse. | 99.9% mensal | Health Check | Must |
| RNF-07 | Data Integrity | Divergência S3/MinIO Raw vs ClickHouse Curated. | 0 registros | Checksum/Audit | Must |

## 3. Segurança (Security)
Proteção dos dados do marketplace e conformidade com acessos.

| ID | Atributo | SLI (Indicador) | SLO (Objetivo) | Fonte | Prioridade |
|:---|:---|:---|:---|:---|:---|
| RNF-08 | Confidentiality | Secrets/Credenciais hardcoded no código. | 0 ocorrências | GitGuardian/Scan | Must |
| RNF-09 | Accountability | Logs de acesso a dados sensíveis (PII). | 100% auditado | CloudTrail | Should |
| RNF-10 | Authenticity | Uso de IAM Roles para acesso ao S3/SSM. | 100% via Role | IAM Audit | Must |

## 4. Manutenibilidade (Maintainability)
Garantir que o pipeline possa evoluir sem degradação técnica.

| ID | Atributo | SLI (Indicador) | SLO (Objetivo) | Fonte | Prioridade |
|:---|:---|:---|:---|:---|:---|
| RNF-11 | Modularity | Uso de scripts desacoplados por camada. | 100% modular | Code Review | Should |
| RNF-12 | Testability | Cobertura de testes unitários em transformações. | > 80% linhas | Pytest Report | Should |
| RNF-13 | Analysability | Tempo para detecção de falha (MTTD). | < 5 minutos | SNS Alertas | Must |

## 5. Usabilidade (Usability)
Foco na experiência do analista de dados e transparência do pipeline.

| ID | Atributo | SLI (Indicador) | SLO (Objetivo) | Fonte | Prioridade |
|:---|:---|:---|:---|:---|:---|
| RNF-14 | Operability | Dashboards de saúde do pipeline ativos. | 100% visível | CloudWatch | Should |
| RNF-15 | User Error Protection | Alerta de schema drift na entrada (Raw). | < 1 min alerta | Schema Val. | Must |

## 6. Compatibilidade, Portabilidade e Adequação Funcional

| ID | Atributo | Descrição | Requisito | Fonte | Prioridade |
|:---|:---|:---|:---|:---|:---|
| RNF-16 | Portability | Lock-in de serviços AWS proprietários. | Uso de SQL/Python | ADR-01 | Should |
| RNF-17 | Co-existence | Impacto do ETL no consumo de CPU do ClickHouse. | < 50% CPU pico | CH Metrics | Could |
| RNF-18 | Functional Suitability | Cobertura dos RFs definidos no doc 01. | 100% RTM | Matriz RTM | Must |

---

## Premissas Técnicas
1. O AWS Academy Learner Lab permite o uso de EC2 para rodar o ClickHouse.
2. A volumetria de 100k pedidos processada via ClickHouse utiliza compressão eficiente, mantendo o disco abaixo de 10GB/mês.
3. Formato de entrada fixo em CSV/JSON/Parquet.

## Fontes de Medição
- **CloudWatch**: Métricas de infraestrutura.
- **Airflow Metadata**: Métricas de execução e retries.
- **SQL Audit Scripts**: Validação de integridade e duplicidade (SRE Scripts).
- **Grafana**: Visualização de SLAs/SLOs.
