import os
import time
import boto3
import clickhouse_connect
from concurrent.futures import ThreadPoolExecutor
import logging

# Configuração de Logging (Tática de Observabilidade)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BUCKET_NAME = os.getenv('BUCKET_NAME', 'northwind-data-pipeline-403783416520')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
RAW_PREFIX = os.getenv('RAW_PREFIX', 'raw/')

CH_HOST = os.getenv('CLICKHOUSE_HOST', 'clickhouse')
CH_USER = os.getenv('CLICKHOUSE_USER', 'admin')
CH_PASS = os.getenv('CLICKHOUSE_PASSWORD', 'password')
CH_DB = os.getenv('CLICKHOUSE_DB', 'northwind_db')

def get_ch_client():
    return clickhouse_connect.get_client(
        host=CH_HOST, username=CH_USER, password=CH_PASS, database=CH_DB
    )

FILE_TABLE_MAP = {
    'northwind_orders': 'raw_orders',
    'northwind_order_details': 'raw_order_details',
}

def ingest_native_s3(file_key, table_name, retries=3):
    """
    Ingestão nativa S3 -> ClickHouse com Táticas de Disponibilidade (Retries)
    e Idempotência (Cleanup por source_file).
    """
    ch = get_ch_client()
    s3_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
    
    # Tática de Idempotência: Remove dados do mesmo arquivo antes de re-ingerir
    # Isso evita duplicidade em caso de reprocessamento (Reprodutibilidade Bass)
    cleanup_query = f"ALTER TABLE {table_name} DELETE WHERE source_file = '{file_key}'"
    
    ingest_query = f"""
        INSERT INTO {table_name}
        SELECT
            *,
            now() as ingested_at,
            '{file_key}' as source_file
        FROM s3('{s3_url}', 'CSVWithNames')
    """

    for attempt in range(retries):
        try:
            logger.info(f"Tentativa {attempt+1}: Limpando dados antigos de {file_key} em {table_name}...")
            ch.command(cleanup_query)
            
            logger.info(f"Tentativa {attempt+1}: Ingerindo {file_key} -> {table_name}...")
            ch.command(ingest_query)
            
            logger.info(f"Sucesso: {file_key} carregado.")
            return True
        except Exception as e:
            logger.error(f"Erro na tentativa {attempt+1} para {file_key}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt) # Exponential backoff
            else:
                logger.critical(f"Falha definitiva na ingestão de {file_key}")
                return False

def sync_all():
    """
    Orquestração com Tática de Performance (Paralelismo)
    """
    s3 = boto3.client('s3', region_name=AWS_REGION)
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=RAW_PREFIX)
    except Exception as e:
        logger.error(f"Erro ao listar bucket S3: {e}")
        return

    if 'Contents' not in response:
        logger.warning("Nenhum arquivo encontrado no bucket.")
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
        else:
            logger.debug(f"Arquivo ignorado: {file_key}")

    if not files_to_process:
        logger.warning("Nenhum arquivo mapeado para processamento.")
        return

    # Tática de Performance (Bass): Processamento paralelo
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda p: ingest_native_s3(*p), files_to_process))
    
    success_count = sum(1 for r in results if r)
    logger.info(f"Sincronização finalizada: {success_count}/{len(files_to_process)} arquivos com sucesso.")

if __name__ == "__main__":
    sync_all()

if __name__ == "__main__":
    sync_all()
