import os
import boto3
import clickhouse_connect
from concurrent.futures import ThreadPoolExecutor

BUCKET_NAME = os.getenv('BUCKET_NAME', 'olist-data-pipeline-403783416520')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
RAW_PREFIX = os.getenv('RAW_PREFIX', 'raw/')

CH_HOST = os.getenv('CLICKHOUSE_HOST', 'clickhouse')
CH_USER = os.getenv('CLICKHOUSE_USER', 'admin')
CH_PASS = os.getenv('CLICKHOUSE_PASSWORD', 'password')
CH_DB = os.getenv('CLICKHOUSE_DB', 'olist_db')

def get_ch_client():
    return clickhouse_connect.get_client(
        host=CH_HOST, username=CH_USER, password=CH_PASS, database=CH_DB
    )

FILE_TABLE_MAP = {
    'data_teste_atualizado': 'raw_orders',
    'data_teste_olist': 'raw_orders',
}

def ingest_native_s3(file_key, table_name):
    ch = get_ch_client()
    s3_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
    print(f"Ingestão nativa: {file_key} -> {table_name}...")
    query = f"""
        INSERT INTO {table_name}
        SELECT
            *,
            now() as ingested_at,
            '{file_key}' as source_file
        FROM s3('{s3_url}', 'CSVWithNames')
    """
    try:
        ch.command(query)
        print(f"Sucesso: {file_key} carregado em {table_name}.")
    except Exception as e:
        print(f"Erro na ingestão de {file_key}: {e}")

def sync_all():
    s3 = boto3.client('s3', region_name=AWS_REGION)
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=RAW_PREFIX)
    if 'Contents' not in response:
        print("Nenhum arquivo encontrado no bucket.")
        return
    files_to_process = []
    for obj in response['Contents']:
        file_key = obj['Key']
        if not file_key.endswith('.csv'):
            continue
        file_name = file_key.split('/')[-1].replace('.csv', '')
        table = FILE_TABLE_MAP.get(file_name)
        if table:
            files_to_process.append((file_key, table))
            print(f"Arquivo mapeado: {file_key} -> {table}")
        else:
            print(f"Arquivo ignorado (sem mapeamento): {file_key}")
    if not files_to_process:
        print("Nenhum arquivo CSV com mapeamento encontrado.")
        return
    with ThreadPoolExecutor(max_workers=4) as executor:
        for file_key, table in files_to_process:
            executor.submit(ingest_native_s3, file_key, table)

if __name__ == "__main__":
    sync_all()
