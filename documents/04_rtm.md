# RTM - Matriz de Rastreabilidade de Requisitos

| Req ID | Descrição | Componente | Teste Relacionado | Status |
|--------|-----------|------------|-------------------|--------|
| RF-01 | Ingestão S3 | `ingestion_engine.py` | Teste Unitário Ingestão | - |
| RF-03 | Carga Postgres | `db_loader.py` | Teste de Integração DB | - |
| RF-05 | Idempotência | `deduplicator.py` | Teste de Reprocessamento | - |
| RNF-01 | Disponibilidade | Infra AWS/RDS | Monitoramento Prometheus | - |
| RNF-02 | Performance | SQL Views / Index | Teste de Carga (05_test_plan_load) | - |
| RNF-03 | Segurança | IAM Roles / VPC | Scan de Segurança (06_test_plan_security) | - |
