# Skill: Elicit Non-Functional Requirements (ISO 25010 Model)

## Quando usar
Quando o usuário pedir RNFs e já existir `spec/00_problem.md` e/ou `documents/01_functional_requirements.md`.

## Entrada
- `spec/00_problem.md` (obrigatório)
- `documents/01_functional_requirements.md` (opcional)

## Passos
1. **Análise de Contexto**: Ler stakeholders e fluxos críticos descritos no problema.
2. **Mapeamento ISO**: Mapear cada fluxo aos 8 atributos da **ISO 25010** (Adequação Funcional, Eficiência de Desempenho, Compatibilidade, Usabilidade, Confiabilidade, Segurança, Manutenibilidade e Portabilidade).
3. **Definição de Métricas**: Para cada atributo, propor 1 a 3 RNFs com SLI (Service Level Indicator) mensurável.
4. **Priorização**: Marcar prioridade seguindo o método **MoSCoW** (Must have, Should have, Could have, Won't have).
5. **Validação Técnica**: Listar premissas e fontes de medição para cada requisito.

## Saída
Arquivo `documents/02_non_functional_requirements.md` contendo:
- Seção detalhada por atributo ISO 25010.
- IDs `RNF-NN` únicos e estáveis.
- Tabela consolidada final com as colunas: (ID, Atributo, SLI, SLO, Fonte, Prioridade).

## Critérios de Aceitação
- **Cobertura Total**: Todos os 8 atributos da ISO 25010 devem ser abordados.
- **Mensurabilidade**: Todo RNF deve ter unidade (ex: ms, %, registros) e janela (ex: por lote, mensal).
- **Não-Aspiracional**: Proibido usar termos vagos como "ser confiável" ou "ser rápido". Use métricas exatas.
