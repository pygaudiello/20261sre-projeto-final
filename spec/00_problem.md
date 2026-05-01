# Contexto do Problema: Pipeline de Dados Olist

## Visão Geral
O marketplace Olist necessita de uma infraestrutura de dados robusta para processar o volume diário de vendas e gerar insights analíticos. O sistema deve transformar dados brutos de pedidos em informações estratégicas para dashboards de monitoramento diário.

## Desafio Técnico
Processar aproximadamente **100 mil pedidos diários** provenientes do marketplace.

## Requisitos de Confiabilidade (SRE-First)
Para garantir a integridade do negócio, o pipeline de ETL (Extract, Transform, Load) deve aderir aos seguintes pilares:

1.  **Idempotência**: Reprocessar os mesmos dados não deve causar duplicidade ou inconsistência no banco analítico.
2.  **Observabilidade**: O sistema deve fornecer logs, métricas e alertas claros sobre o estado do processamento.
3.  **Resiliência**: O pipeline deve ser capaz de lidar com falhas parciais (ex: indisponibilidade temporária de um serviço) e recuperar-se sem intervenção manual excessiva.
4.  **Integridade de Dados**: 
    *   **Zero Perda**: Nenhum pedido pode ser "perdido" durante o transporte ou transformação.
    *   **Zero Duplicação**: O banco analítico deve refletir a realidade exata do marketplace.
    *   **Falha Explícita**: O sistema não deve sofrer "silenciosamente". Qualquer erro crítico deve interromper o fluxo ou alertar imediatamente os responsáveis.

## Objetivo Final
Carregamento de dados em um banco de dados analítico (Postgres) para alimentação de dashboards diários (Grafana), garantindo que a tomada de decisão seja baseada em dados confiáveis e atuais.
