# Plano de Testes de Carga

## 1. Escopo
Validar se o pipeline de dados e o banco Postgres suportam o volume de ~100k registros diários e consultas concorrentes no Grafana.

## 2. Cenários de Teste

### 2.1. Load Test (Carga Normal)
- **Objetivo**: Verificar comportamento sob carga esperada (~100k reg/dia).
- **Métrica**: Tempo de processamento < 2 horas.

### 2.2. Soak Test (Carga Constante/Longa)
- **Objetivo**: Identificar memory leaks ou exaustão de disco/conexões em execuções sucessivas.
- **Duração**: 24 horas de ingestão contínua.

### 2.3. Spike Test (Picos Súbitos)
- **Objetivo**: Simular chegada massiva de arquivos no S3 simultaneamente.
- **Cenário**: 5x o volume diário em uma única janela.

### 2.4. Stress Test (Limite do Sistema)
- **Objetivo**: Encontrar o "breaking point" da instância Postgres e do processamento Python.

## 3. Ferramentas
- **Locust** ou **k6** para simulação de queries.
- **Custom scripts** para geração de CSVs massivos no S3.
- **Grafana/Prometheus** para monitoramento de recursos durante os testes.
