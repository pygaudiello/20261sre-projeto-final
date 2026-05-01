# Requisitos Funcionais (RF)

Este documento detalha os requisitos funcionais do pipeline de dados Olist, organizados pelas fases do ciclo de vida do dado.

## 1. Fase de Ingestão e Captura
| ID | Requisito | Descrição | Critérios de Aceite |
|:---|:---|:---|:---|
| **RF-01** | Ingestão de pedidos | Consumir pedidos da fonte definida (API/Arquivos). | Captura total; Registro de run_id e timestamp. |
| **RF-02** | Carga Incremental | Ingerir apenas dados novos/modificados (Watermark). | Uso de cursores; Sem duplicidade na leitura. |
| **RF-03** | Persistência Raw | Armazenar dados brutos sem modificações. | Camada Raw preservada; Particionamento por data. |

## 2. Processamento, Transformação e Qualidade
| ID | Requisito | Descrição | Critérios de Aceite |
|:---|:---|:---|:---|
| **RF-04** | Normalização | Converter Raw para Modelo Canônico (Trusted). | Tipagem correta; Schema padronizado. |
| **RF-05** | Regras de Negócio | Cálculo de valores e status de pedidos. | Regras versionadas; Consistência matemática. |
| **RF-06** | Enriquecimento | Join com dados de Produtos e Clientes. | Enriquecimento completo; Fallback para nulos. |
| **RF-07** | Validação de Dados | Check de obrigatoriedade e integridade. | Rejeição de nulos críticos; Range checks. |
| **RF-08** | Dead-Letter Queue | Segregar registros inválidos para análise. | Isolamento de erros; Log do motivo da falha. |
| **RF-09** | Garantia de Unicidade | Identificação de `order_id` único. | Zero duplicidade na camada final. |

## 3. Armazenamento e Evolução (Analytics Layer)
| ID | Requisito | Descrição | Critérios de Aceite |
|:---|:---|:---|:---|
| **RF-10** | Upsert de Pedidos | Atualizar status de pedidos existentes. | Reflete estado atual do marketplace. |
| **RF-11** | Carga no Warehouse | Persistir dados na camada Curated. | Otimizado para leitura (Star Schema/Indexes). |
| **RF-12** | Histórico (SCD) | Manter histórico de mudanças de estado. | Rastreabilidade de versões do pedido. |

## 4. Orquestração e Manutenção
| ID | Requisito | Descrição | Critérios de Aceite |
|:---|:---|:---|:---|
| **RF-13** | Agendamento Automático | Execução periódica configurável. | Trigger via Airflow/Cron; Gestão de dependência. |
| **RF-14** | Execução Manual | Trigger sob demanda via interface. | Suporte a parâmetros de data manuais. |
| **RF-15** | Reprocessamento (Full) | Reprocessar intervalos históricos. | Idempotência garantida; Sobrescrita segura. |
| **RF-16** | Reprocessamento (Granular) | Reprocessar pedidos específicos por ID. | Correção cirúrgica no banco analítico. |

## 5. Monitoramento e Observabilidade
| ID | Requisito | Descrição | Critérios de Aceite |
|:---|:---|:---|:---|
| **RF-17** | Status do Pipeline | Dashboards de saúde do ETL. | Visibilidade de Running/Success/Failed. |
| **RF-18** | Logs Estruturados | Logs detalhados por etapa do pipeline. | Rastreabilidade por ID de execução. |

## 6. Entrega e Analytics
| ID | Requisito | Descrição | Critérios de Aceite |
|:---|:---|:---|:---|
| **RF-19** | Camada Semântica | Expor tabelas prontas para consumo. | Tabelas documentadas; Facilidade de query. |
| **RF-20** | Atualização BI | Sincronia com ferramentas de visualização. | Dados atualizados na janela de SLO (< 1h). |

---
**Nota de Rastreabilidade**: Estes requisitos visam resolver o desafio de 100k pedidos/dia detalhado em `spec/00_problem.md`.
