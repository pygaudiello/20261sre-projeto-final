import urllib.request
import base64
import time
import os
import sys

host = os.getenv('CLICKHOUSE_HOST', 'clickhouse')
user = os.getenv('CLICKHOUSE_USER', 'admin')
password = os.getenv('CLICKHOUSE_PASSWORD', 'password')
max_retries = 15

for i in range(max_retries):
    try:
        req = urllib.request.Request(f'http://{host}:8123/ping')
        auth = base64.b64encode(f'{user}:{password}'.encode()).decode()
        req.add_header('Authorization', f'Basic {auth}')
        urllib.request.urlopen(req, timeout=5)
        print('ClickHouse OK')
        sys.exit(0)
    except Exception:
        print(f'Aguardando ClickHouse... tentativa {i+1}/{max_retries}')
        time.sleep(5)

print('ClickHouse não respondeu após', max_retries, 'tentativas')
sys.exit(1)
