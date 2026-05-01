# Plano de Testes de Modelagem

## 1. Metodologias de Revisão

### 1.1. ATAM (Architecture Tradeoff Analysis Method)
- Avaliar como as decisões de arquitetura (ex: escolha do Postgres vs NoSQL) afetam os atributos de qualidade (RNFs).
- Identificar "Risks", "Non-risks", "Sensitivity Points" e "Tradeoffs".

### 1.2. FMEA (Failure Mode and Effects Analysis)
- **Falha**: Arquivo CSV corrompido. **Impacto**: Dados inconsistentes. **Mitigação**: Validação de Hash.
- **Falha**: Banco indisponível. **Impacto**: Interrupção do ETL. **Mitigação**: Retry com Backoff.
- **Falha**: Queda do Airflow. **Impacto**: Atraso no dashboard. **Mitigação**: HA para o orquestrador.

### 1.3. Architecture Walkthrough
- Sessão estruturada para percorrer os fluxos críticos (Ingestão -> Transformação -> Carga) com os stakeholders.

## 2. Validação de Cenários
- Simulação de falhas controladas (Chaos Engineering leve) para validar os modos de mitigação descritos no `spec/00_problem.md`.
