import os
import boto3
import polars as pl
import clickhouse_connect
from datetime import datetime

# Configurações de ambiente
S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'http://localhost:9000')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', 'admin')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', 'password')
BUCKET_NAME = os.getenv('BUCKET_NAME', 'olist')

CH_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
CH_USER = os.getenv('CLICKHOUSE_USER', 'admin')
CH_PASS = os.getenv('CLICKHOUSE_PASSWORD', 'password')
CH_DB = os.getenv('CLICKHOUSE_DB', 'olist_db')

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )

def get_ch_client():
    return clickhouse_connect.get_client(
        host=CH_HOST,
        username=CH_USER,
        password=CH_PASS,
        database=CH_DB
    )

def ingest_csv_from_s3(file_key, table_name):
    """
    Lê um CSV do S3/MinIO e carrega no ClickHouse usando Polars.
    """
    s3 = get_s3_client()
    ch = get_ch_client()
    
    print(f"📥 Baixando {file_key} do bucket {BUCKET_NAME}...")
    
    # Download do arquivo para memória/temporário
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    
    # Leitura ultra-rápida com Polars
    df = pl.read_csv(obj['Body'].read())
    
    # Adiciona metadados de auditoria (SRE Best Practice)
    df = df.with_columns([
        pl.lit(datetime.now()).alias('ingested_at'),
        pl.lit(file_key).alias('source_file')
    ])
    
    print(f"🚀 Carregando {df.height} linhas na tabela {table_name}...")
    
    # Inserção no ClickHouse
    # Nota: O clickhouse-connect aceita DataFrames do pandas, 
    # então convertemos o polars para pandas no momento da escrita
    ch.insert_df(table_name, df.to_pandas())
    
    print(f"✅ Sucesso: {file_key} -> {table_name}")

def sync_all():
    """
    Sincroniza todos os arquivos pendentes no bucket.
    """
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' not in response:
        print("📭 Nanhum arquivo encontrado no bucket.")
        return

    for obj in response['Contents']:
        file_key = obj['Key']
        if file_key.endswith('.csv'):
            # Define o nome da tabela com base no nome do arquivo (ex: orders.csv -> raw_orders)
            table_name = f"raw_{file_key.split('.')[0]}"
            try:
                ingest_csv_from_s3(file_key, table_name)
            except Exception as e:
                print(f"❌ Erro ao processar {file_key}: {e}")

if __name__ == "__main__":
    sync_all()
