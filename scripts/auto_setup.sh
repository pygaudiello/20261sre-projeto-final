#!/bin/bash
# Auto Setup: Upload CSV, Create Tables, Ingest, Run dbt
# BASS: Script idempotente — pode ser executado múltiplas vezes sem efeito colateral
# ATAM: Tradeoff entre automação (confiabilidade) vs complexidade de script

set -euo pipefail

BUCKET="olist-data-pipeline-403783416520"
CSV_FILE="data_teste_atualizado.csv"
S3_PATH="raw/"

echo "Olist Pipeline — Setup Automatizado"
echo "==================================="

# 1. Upload CSV para o S3 (se ainda não estiver lá)
echo "[1/4] Verificando CSV no S3..."
if aws s3 ls "s3://$BUCKET/$S3_PATH$CSV_FILE" 2>/dev/null; then
    echo "  CSV já existe no S3. Pulando upload."
else
    echo "  Enviando $CSV_FILE para s3://$BUCKET/$S3_PATH..."
    aws s3 cp "$CSV_FILE" "s3://$BUCKET/$S3_PATH"
fi

# 2. Criar tabelas no ClickHouse
echo "[2/4] Criando tabelas raw no ClickHouse..."
docker compose exec -T clickhouse clickhouse-client --multiquery < scripts/create_raw_tables.sql

# 3. Executar ingestão
echo "[3/4] Executando ingestão S3 -> ClickHouse..."
docker compose run --rm ingestion

# 4. Executar dbt transformations
echo "[4/4] Executando dbt (staging -> marts)..."
docker compose run --rm dbt run --profiles-dir .

echo "Pipeline concluído com sucesso!"
echo "Acesse o dashboard em http://localhost:8501"
