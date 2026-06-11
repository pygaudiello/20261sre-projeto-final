# AWS CLI Session Setup

Para conectar o AWS CLI no ambiente do GitHub Codespaces ou local:

## 1. Configuração de Credenciais
Execute o comando abaixo e insira as informações solicitadas (Access Key, Secret Key, Region):
```bash
aws configure
```

## 2. Verificação de Identidade
Confirme se as credenciais estão ativas:
```bash
aws sts get-caller-identity
```

## 3. Comandos Úteis para o Projeto
- Listar arquivos brutos no S3:
  ```bash
  aws s3 ls s3://meu-bucket-northwind/raw/
  ```
- Upload de um novo arquivo para teste:
  ```bash
  aws s3 cp dados_teste.csv s3://meu-bucket-northwind/raw/
  ```

## 4. Persistência de Sessão
Em Codespaces, lembre-se que variáveis de ambiente podem ser salvas nos "Secrets" do repositório para evitar reconfiguração:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
