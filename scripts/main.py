import os
import boto3
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

def check_connections():
    print("Checking connections...")
    
    # MinIO
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=os.getenv('S3_ENDPOINT', 'http://minio:9000'),
            aws_access_key_id=os.getenv('S3_ACCESS_KEY', 'admin'),
            aws_secret_access_key=os.getenv('S3_SECRET_KEY', 'password')
        )
        s3.list_buckets()
        print("✅ MinIO Connection: OK")
    except Exception as e:
        print(f"❌ MinIO Connection Failed: {e}")

    # ClickHouse
    try:
        client = clickhouse_connect.get_client(
            host=os.getenv('CLICKHOUSE_HOST', 'clickhouse'),
            username=os.getenv('CLICKHOUSE_USER', 'admin'),
            password=os.getenv('CLICKHOUSE_PASSWORD', 'password'),
            port=8123
        )
        print(f"✅ ClickHouse Connection: OK (Version {client.server_version})")
    except Exception as e:
        print(f"❌ ClickHouse Connection Failed: {e}")

if __name__ == "__main__":
    check_connections()
