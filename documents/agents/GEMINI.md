# GEMINI.md · olist-sre-pipeline

## Contexto
Pipeline de dados Olist em AWS Academy Learner Lab (us-east-1).
ETL Python -> Postgres -> Grafana. SRE-first.

## Diretrizes de Resposta
1. **Surgical Updates**: Ao modificar documentos, mantenha a precisão e o estilo técnico.
2. **Context Awareness**: Sempre considere os requisitos funcionais (RF) e não-funcionais (RNF) definidos na pasta `documents/`.
3. **Traceability**: Ao sugerir uma mudança no código ou arquitetura, verifique como isso impacta a Matriz de Rastreabilidade (RTM).
4. **Resilience First**: Toda solução proposta deve incluir uma breve análise de "como isso pode falhar" e "como mitigamos".

## Fluxo de Trabalho
- **Análise**: Ler os specs atuais.
- **Proposta**: Apresentar solução técnica fundamentada.
- **Implementação**: Gerar código ou documentação.
- **Validação**: Propor testes (Carga, Segurança ou Modelagem).

## Restrições duras
- **Proibido**: Uso de AWS Glue, Redshift, ou SageMaker (não habilitados no Learner Lab).
- **Segurança**: Sem secrets em código. Tudo via SSM Parameter Store.
- **Escopo**: Sem provisionar recursos reais nesta fase. Apenas Markdown e Mermaid.

## Saída Esperada
- **Formatação**: Markdown válido com cabeçalhos hierárquicos.
- **Identificadores**: IDs estáveis: RF-NN, RNF-NN, TC-NN, ADR-NN.
- **RNF Mensurável**: Deve conter: Valor, Unidade, Janela de medição e Fonte da métrica.
- **Seção Final**: Sempre incluir Premissas e Questões em Aberto ao final de cada documento.

## Comportamento do Agente
- **Autocrítica**: Critique sua própria saída antes de entregar.
- **Análise de Risco**: Liste obrigatoriamente 3 riscos e 2 ambiguidades por arquivo gerado/modificado.
- **Uso de Skills**: Utilize as habilidades definidas em `documents/agents/skills/`.
- **Fidelidade AWS**: Não invente nomes de serviços AWS; use apenas serviços reais e disponíveis no plano Learner Lab.

## Comandos Recomendados
- Para atualizar requisitos: `gemini "Atualizar RF-05 conforme nova regra de negócio em X"`
- Para revisão de arquitetura: `gemini --skill review_architecture`
- Para gerar matriz RTM: `gemini --skill build_rtm`

## Comportamento Específico de Edição
- Utilize a ferramenta `replace` para edições cirúrgicas nos arquivos markdown de documentação.
- Mantenha o arquivo `documents/00_index.md` sempre atualizado ao criar novos arquivos na pasta.
- Ao identificar bugs no ETL (futuramente), sugira imediatamente a atualização do plano de testes de modelagem (FMEA) em `07_test_plan_modeling.md`.
