# Plano de Testes de Segurança

## 1. Modelagem de Ameaças (STRIDE)
- **Spoofing**: Autenticação no S3 e Postgres (IAM/Secrets Manager).
- **Tampering**: Garantir integridade dos CSVs via checksum/hash.
- **Repudiation**: Logs de auditoria (quem acessou/modificou o quê).
- **Information Disclosure**: Criptografia em repouso e em trânsito (TLS/SSL).
- **Denial of Service**: Rate limiting e quotas na infraestrutura AWS.
- **Elevation of Privilege**: Princípio do menor privilégio em roles IAM.

## 2. Padrões e Ferramentas
- **OWASP**: Validação de inputs no código ETL.
- **SAST (Static Application Security Testing)**: Bandit para Python.
- **DAST (Dynamic Application Security Testing)**: Verificação de endpoints expostos (se houver API).
- **AWS Inspector**: Scan de vulnerabilidades nas instâncias EC2.

## 3. Verificações Manuais
- Revisão de políticas IAM.
- Verificação de visibilidade pública de buckets S3.
