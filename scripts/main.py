import os
import sys

def check_environment():
    required_vars = [
        'CLICKHOUSE_HOST', 'CLICKHOUSE_USER', 'CLICKHOUSE_PASSWORD', 'CLICKHOUSE_DB',
        'BUCKET_NAME', 'AWS_REGION'
    ]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"Variáveis ausentes: {missing}")
        return False
    return True

def main():
    print("Northwind Data Pipeline — Camada de Ingestão")
    print("=" * 40)

    if not check_environment():
        sys.exit(1)

    print("Ambiente OK. Executando ingestão...")
    from ingest_data import sync_all
    sync_all()

if __name__ == "__main__":
    main()
