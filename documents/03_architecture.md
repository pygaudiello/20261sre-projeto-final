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
- **Pilha de Observabilidade**: Alertas de MTTD, Status do pipeline e Dashboards nativos no CloudWatch. (RF-17, RF-18, RNF-13, RNF-14)
- **Atendimento**: RF-03, RF-11, RF-13, RF-14, RF-15, RF-16, RF-17, RF-18. RNF-01, RNF-05, RNF-06, RNF-11, RNF-13, RNF-14, RNF-16, RNF-17.

## 5. Technology Viewpoint (Visão de Tecnologia)
**Objetivo**: Escolha tecnológica limitada ao AWS Academy Learner Lab.
- **Processamento**: AWS Lambda (Python 3.x) para ingestão e transformações leves. (RNF-01, RNF-11, RNF-12)
- **Orquestração**: Apache Airflow em Docker ou AWS Step Functions (Conforme custo/benefício do Lab). (RNF-02, RNF-03)
- **Dados**: RDS PostgreSQL (db.t3.micro) e S3 Buckets. (RNF-16)
- **Segurança**: AWS IAM Roles e SSM Parameter Store (Secrets). (RNF-08, RNF-10)
- **Observabilidade**: CloudWatch Dashboards, Logs e SNS (Sem instâncias dedicadas). (RNF-13, RNF-14)
- **Atendimento**: RNF-01, RNF-02, RNF-03, RNF-08, RNF-10, RNF-11, RNF-12, RNF-13, RNF-14, RNF-16.

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
   * Observabilidade: A Visão de Engenharia inclui uma pilha de observabilidade com Grafana e CloudWatch para monitorar o status do
     pipeline em tempo real (RF-17).
   * Escalabilidade: A escolha de Python modular e S3 permite que o sistema suporte o volume de 100k pedidos/dia e picos de carga
     (RNF-01/03).


      Resumo Executivo da Arquitetura: Pipeline de Dados Olist (SRE-Focused)

  "A arquitetura proposta para o desafio da Olist foi desenhada sob o framework RM-ODP (ISO/IEC 10746), focando em processar 100 mil
  pedidos diários com garantias rigorosas de integridade e baixo custo operacional no ambiente AWS Academy.

  Nossas principais escolhas estratégicas foram guiadas por três pilares: Simplicidade de Desenvolvimento, Eficiência de Custo e
  Resiliência SRE.

  1. Estratégia de Processamento: Serverless-First (ADR-05)
  Optamos por substituir instâncias EC2 e containers Docker por AWS Lambda (Python). 
   * Por que? Reduzimos o tempo de desenvolvimento ao eliminar o gerenciamento de servidores e patchings. O Lambda oferece escalabilidade
     automática e integração nativa com o S3, sendo disparado via eventos assim que um arquivo é carregado. Isso garante que o custo seja
     proporcional ao volume processado, aproveitando o Free Tier da AWS.

  2. Armazenamento e Camadas de Dados (ADR-01 & ADR-03)
  O fluxo segue o padrão de Data Lakehouse simplificado:
   * Bronze (Raw): Armazenamento imutável no S3 em formato original, garantindo a capacidade de reprocessamento total em caso de desastre.
   * Gold (Analytics): Os dados processados são carregados via upsert em um RDS PostgreSQL. Escolhemos o Postgres pela maturidade em
     operações analíticas e suporte nativo a índices, essencial para alimentar os dashboards diários com baixa latência.

  3. Observabilidade e Monitoramento Nativo (ADR-04)
  Em vez de ferramentas externas como Grafana ou Prometheus, centralizamos tudo no AWS CloudWatch.
   * Por que? Reduzimos o consumo de créditos do Lab ao não manter instâncias dedicadas. Utilizamos o CloudWatch para logs estruturados,
     métricas de saúde do pipeline e dashboards de SLOs (como tempo de processamento e taxa de erro). Alertas críticos são disparados via
     SNS (Simple Notification Service) para garantir um baixo MTTD (Tempo Médio de Detecção).

  4. Garantias de Confiabilidade (SRE)
  Para atender aos requisitos de 'Confialibilidade Zero Perda':
   * Idempotência: A lógica de carga no banco utiliza order_id como chave de unicidade, permitindo que o mesmo lote seja reprocessado
     múltiplas vezes sem duplicar dados.
   * Dead-Letter Queues (DLQ): Registros que falham em validações de schema ou regras de negócio são isolados para análise posterior,
     impedindo que erros silenciosos corrompam o Analytics.
   * Orquestração: O fluxo é resiliente a falhas temporárias com políticas de Retries automáticos configuradas no Lambda ou Step
     Functions.

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
