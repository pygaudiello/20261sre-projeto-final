# Canvas de Modelagem do Problema - Desafio Olist

## 1. Stakeholders
- **Operação Olist**: time responsável pelo marketplace e vendas
- **Time de dados**: engenheiros de dados e analistas
- **Clientes internos**: equipes de produto, suporte e tomada de decisão
- **SRE/Plataforma**: operação e infraestrutura de sistemas

## 2. Fluxos críticos
- **Ingestão CSV→Postgres**: pipeline ETL diário processando ~100k pedidos diários
- **Consulta Grafana**: dashboards para monitoramento e análise de métricas
- **Observação SLA**: monitoramento contínuo de disponibilidade e performance

## 3. Requisitos Funcionais do ETL
- Ingestão diária de ~100k registros CSV
- Transformação e limpeza dos dados
- Carregamento no banco analítico (Postgres)
- Geração de dados para dashboards Grafana
- Suporte a reprocessamento (idempotência)
- Logs de processamento detalhados
- Métricas de qualidade dos dados

## 4. Modos de falha
- **Arquivo corrompido**: dados inválidos ou incomplete no arquivo de ingestão
- **Reprocessamento duplicando**: falha na idempotência causando duplicatas
- **Queda EC2**: indisponibilidade do nó de processamento
- **Banco indisponível**: indisponibilidade temporária do Postgres

## 5. Arquitetura de Dados

### Camadas:
1. **Camada de Ingestão (Raw)**:
   - Bucket S3 para arquivos CSV brutos
   - Metadados de arquivo (checksum, hash, timestamp)
   
2. **Camada de Processamento (Staging)**:
   - Tabelas temporárias no Postgres
   - Dados parciais transformados
   - Validação de schema
   
3. **Camada Mestre (Master)**:
   - Tabelas dimensionais e fatos normalizados
   - Dados históricos preservados
   - Índices para consulta performática
   
4. **Camada de Apresentação (Analytics)**:
   - Views materializadas para dashboards
   - Dados agregados e pré-calculados
   - API para consulta

### Tecnologias:
- **Armazenamento**: S3 (CSV brutos), Postgres (analítico)
- **Processamento**: Python/SQL (pandas, SQLAlchemy)
- **Orquestração**: Airflow/Apache DAGs
- **Observabilidade**: Prometheus + Grafana
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)

## 6. Mecanismos de Observabilidade

### Métricas coletadas:
- **Throughput**: registros processados/minuto
- **Taxa de erro**: falhas por tipo
- **Tempo de processamento**: duração do ETL
- **Qualidade dos dados**: % de registros válidos
- **Uso de recursos**: CPU, memória, disco

### Logs estruturados:
- Início/fim do processamento
- Erros com stack trace
- Alertas críticos (falhas, timeouts)
- Sumário estatístico (registros lidos, gravados, ignorados)

### Alertas configurados:
- Falha na ingestão → Slack/Email
- Dados fora do SLA → PagerDuty
- Qualidade abaixo do limiar → Time de dados
- Backup automático de falhas

## 7. Estratégias de Idempotência e Prevenção de Duplicatas

### Mecanismos de idempotência:
1. **Identificação única por arquivo**:
   - Hash do arquivo (SHA256) como identificador único
   - Registro de processamentos bem-sucedidos
   
2. **Chaves naturais nos dados**:
   - Usar `order_id` como chave primária única
   - Índice único em colunas de identificação
   
3. **Técnica de upsert**:
   - `INSERT ... ON CONFLICT DO UPDATE`
   - Verificação prévia de existência
   
4. **Tabela de controle de processamento**:
   ```sql
   CREATE TABLE etl_control (
       file_hash VARCHAR(64) PRIMARY KEY,
       processed_at TIMESTAMP,
       status VARCHAR(20),
       records_count INTEGER
   );
   ```

5. **Modo de reprocessamento seguro**:
   - Deletar apenas dados específicos do arquivo
   - Usar transações para consistência
   - Backup antes de reprocessar

## 8. Plano de Mitigação de Falhas e Resiliência

### Estratégias:
- **Transações distribuídas**: Garantir ACID mesmo em falhas
- **Retry com backoff**: Tentativas inteligentes em falhas temporárias
- **Circuit breaker**: Evitar cascata de falhas
- **Fallback gracefully**: Degradação funcional controlada
- **Validação pós-processamento**: Consistência dos dados
- **Alertas proativos**: Detecção precoce de problemas
- **Testes de carga**: Verificar capacidade sob estresse
- **Playbooks de emergência**: Procedures documentadas para falhas críticas