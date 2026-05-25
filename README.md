# Provisionamento de Infraestrutura Local com Terraform e LocalStack

Automacao Local DevOps | Infraestrutura como Codigo Idempotente | Simulacao de Nuvem AWS sem Custos

Desenvolvido por L. A. Leandro - Sao Jose dos Campos, SP - 25/05/2026

---

## 1. OBJETIVO DO PROGRAMA

Criar um pipeline de provisionamento de infraestrutura local declarativa e idempotente que emula servicos essenciais da AWS (S3, SQS e DynamoDB) dentro de containers Docker utilizando LocalStack, permitindo que equipes de desenvolvimento testem fluxos de nuvem localmente sem custos e com total fidelidade arquitetural.

---

## 2. REQUISITOS

### 2.1. Requisitos Funcionais

- RF01: Provisionar um bucket S3 com criptografia em repouso e bloqueio de acesso publico
- RF02: Provisionar uma fila SQS com parametros de retencao e visibilidade ajustaveis
- RF03: Provisionar uma tabela DynamoDB em modo on-demand com chave de particao simples
- RF04: Emular APIs AWS localmente via LocalStack em container Docker
- RF05: Validar a infraestrutura com script automatizado de smoke test
- RF06: Permitir destruicao completa e reversivel dos recursos provisionados
- RF07: Garantir idempotencia nas execucoes (aplicacoes repetidas geram o mesmo estado)

### 2.2. Requisitos Nao Funcionais

- RNF01: Todas as operacoes devem rodar em maquina local sem dependencia de nuvem publica
- RNF02: Credenciais devem ser ficticias para evitar vazamento de dados reais
- RNF03: Arquivos de estado (.tfstate) devem ser excluidos do repositorio via .gitignore
- RNF04: O Terraform deve falhar de forma elegante se o LocalStack estiver indisponivel

---

## 3. ARQUITETURA DO SISTEMA

```
+------------------------------------------------------------------+
|                        MAQUINA LOCAL                               |
|                                                                   |
|  +------------------+       +----------------------------+        |
|  |    Terraform     |       |     Docker Compose         |        |
|  |  (terraform CLI) |       |                            |        |
|  |                  |       |  +----------------------+  |        |
|  |  main.tf         |------>|  |    LocalStack         |  |        |
|  |  variables.tf    | HTTP  |  |  (emulador AWS)       |  |        |
|  |  outputs.tf      |       |  |                       |  |        |
|  |  terraform.tfvars|       |  |  Porta 4566           |  |        |
|  +------------------+       |  |                       |  |        |
|           |                  |  |  +-----------------+  |  |        |
|           |                  |  |  | S3   (Storage)   |  |  |        |
|           |                  |  |  +-----------------+  |  |        |
|           |                  |  |  | SQS  (Messaging) |  |  |        |
|           |                  |  |  +-----------------+  |  |        |
|           |                  |  |  | DynamoDB (NoSQL) |  |  |        |
|           |                  |  |  +-----------------+  |  |        |
|           |                  |  +----------------------+  |        |
|           |                  +----------------------------+        |
|           |                                                       |
|           v                                                       |
|  +------------------+                                             |
|  |  tests/          |                                             |
|  |  verify_infra.py |------> HTTP (localhost:4566)                |
|  |  (boto3)         |                                             |
|  +------------------+                                             |
|                                                                   |
+------------------------------------------------------------------+

Fluxo de operacao:

1. docker compose up -d              --> Inicia o LocalStack
2. terraform init                     --> Inicializa providers
3. terraform plan                     --> Mostra o plano de recursos
4. terraform apply --auto-approve     --> Provisiona S3 + SQS + DynamoDB
5. python tests/verify_infra.py       --> Smoke test nos recursos
6. terraform destroy --auto-approve   --> Remove todos os recursos
```

---

## 4. STACK TECNOLOGICA

| Componente           | Tecnologia                     | Versao Minima |
|----------------------|--------------------------------|---------------|
| Orquestrador IaC     | Terraform                      | >= 1.5.0      |
| Emulador AWS         | LocalStack (Docker)            | latest        |
| Virtualizacao        | Docker                         | 20.x+         |
| Orquestracao Docker  | Docker Compose                 | 2.x+          |
| Runtime de Testes    | Python                         | 3.9+          |
| SDK AWS para Testes  | boto3                          | 1.28+         |
| Armazenamento        | Amazon S3 (emulado)            | -             |
| Mensageria           | Amazon SQS (emulado)           | -             |
| Banco NoSQL          | Amazon DynamoDB (emulado)      | -             |

---

## 5. DEPENDENCIAS

### 5.1. Ferramentas Obrigatorias

- Docker Engine 20.x ou superior
- Docker Compose V2
- Terraform CLI 1.5 ou superior
- Python 3.9 ou superior
- Git

### 5.2. Dependencias Python (testes)

```
boto3>=1.28.0
botocore>=1.31.0
```

### 5.3. Providers Terraform

```hcl
hashicorp/aws ~> 5.0
```

---

## 6. ESTRUTURA DO PROJETO

```
/
|-- docker-compose.yml        Inicializacao do LocalStack em container
|-- .gitignore                Bloqueio de artefatos sensiveis no repositorio
|-- main.tf                   Providers AWS com mapeamento endpoints locais e recursos
|-- variables.tf              Variaveis declarativas (nomes, regiao, timeouts)
|-- terraform.tfvars          Valores padrao para as variaveis
|-- outputs.tf                Retorno de metadados (ARNs, URLs, endpoint)
|-- tests/
|   |-- verify_infra.py       Script de smoke test com boto3
|-- README.md                 Documentacao do projeto
|-- LICENSE                   Licenca MIT
```

---

## 7. ESPECIFICACAO DOS RECURSOS

### 7.1. Bucket S3: empresa-arquivos-locais

- Nome: `empresa-arquivos-locais`
- Criptografia: AES-256 (Server-Side Encryption)
- Bloqueio de acesso publico: ativo em todas as camadas (ACLs, policies)
- Destruicao forcada permitida para limpeza de ambiente

### 7.2. Fila SQS: fila-processamento-erros

- Nome: `fila-processamento-erros`
- Tempo de retencao: 345600 segundos (4 dias)
- Timeout de visibilidade: 30 segundos
- Delay: 5 segundos
- Polling longo: 10 segundos
- Tamanho maximo da mensagem: 256 KB

### 7.3. Tabela DynamoDB: tabela-auditoria-logs

- Nome: `tabela-auditoria-logs`
- Modo de capacidade: PAY_PER_REQUEST (on-demand)
- Chave de particao: `id` (tipo String)
- Tags: Name, Environment, ManagedBy

---

## 8. INSTALACAO E CONFIGURACAO

### 8.1. Clonar o repositorio

```bash
git clone https://github.com/seu-usuario/Provisionamento-de-Infraestrutura-Local-Terraform-LocalStack.git
cd Provisionamento-de-Infraestrutura-Local-Terraform-LocalStack
```

### 8.2. Verificar ferramentas instaladas

```bash
docker --version
docker compose version
terraform --version
python --version
```

### 8.3. Iniciar o LocalStack

```bash
docker compose up -d
```

Aguardar 10 segundos e verificar:

```bash
docker compose ps
docker logs localstack-iaco --tail 20
```

### 8.4. Verificar saude do LocalStack

```bash
curl -s http://localhost:4566/_localstack/health | python -m json.tool
```

Saida esperada (trecho):

```json
{
    "services": {
        "s3": "available",
        "sqs": "available",
        "dynamodb": "available"
    }
}
```

---

## 9. MANUAL DO USUARIO (EXECUCAO)

### 9.1. Inicializar o Terraform

```bash
terraform init
```

Resultado esperado:

```
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 5.0"...
- Installing hashicorp/aws v5.x.x...
- Installed hashicorp/aws v5.x.x (signed by HashiCorp)

Terraform has been successfully initialized!
```

### 9.2. Visualizar o plano de execucao

```bash
terraform plan
```

### 9.3. Aplicar a infraestrutura

```bash
terraform apply --auto-approve
```

Saida esperada:

```
Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

Outputs:

bucket_arn = "arn:aws:s3:::empresa-arquivos-locais"
bucket_name = "empresa-arquivos-locais"
dynamodb_table_arn = "arn:aws:dynamodb:us-east-1:000000000000:table/tabela-auditoria-logs"
dynamodb_table_name = "tabela-auditoria-logs"
localstack_endpoint = "http://localhost:4566"
queue_arn = "arn:aws:sqs:us-east-1:000000000000:fila-processamento-erros"
queue_url = "http://localhost:4566/000000000000/fila-processamento-erros"
```

### 9.4. Executar os testes de validacao

```bash
pip install boto3
python tests/verify_infra.py
```

Saida esperada:

```
============================================================
 Smoke Test - Infraestrutura Local (LocalStack)
============================================================
[S3 OK] Bucket 'empresa-arquivos-locais' - objeto criado, lido e removido com sucesso.
[SQS OK] Fila 'fila-processamento-erros' - mensagem enviada, recebida e removida com sucesso.
[DynamoDB OK] Tabela 'tabela-auditoria-logs' - item inserido, lido e removido com sucesso.

------------------------------------------------------------
 o S3: PASS
 o SQS: PASS
 o DynamoDB: PASS
------------------------------------------------------------
 RESULTADO: INFRAESTRUTURA VALIDADA COM SUCESSO
============================================================
```

### 9.5. Consultar outputs a qualquer momento

```bash
terraform output
```

### 9.6. Destruir a infraestrutura

Para remover todos os recursos sem afetar o container:

```bash
terraform destroy --auto-approve
```

Para remover tambem o container e dados persistentes:

```bash
docker compose down -v
```

### 9.7. Ciclo completo (reset)

```bash
docker compose down -v
docker compose up -d
sleep 10
terraform init
terraform apply --auto-approve
python tests/verify_infra.py
```

---

## 10. TESTES

### 10.1. Smoke Test (Teste de Fumaca)

O script `tests/verify_infra.py` realiza tres operacoes em sequencia:

1. S3: Cria um objeto, le seu conteudo e o remove
2. SQS: Envia uma mensagem, recebe a mensagem e a remove da fila
3. DynamoDB: Insere um item, le o item e o remove da tabela

Se todas as tres operacoes retornarem sucesso (HTTP 200 + assert), a infraestrutura e considerada validada.

### 10.2. Teste de Idempotencia

Execute `terraform apply` multiplas vezes. O resultado deve ser sempre o mesmo:

- Primeira execucao: `Resources: 5 added, 0 changed, 0 destroyed`
- Segunda execucao em diante: `Resources: 0 added, 0 changed, 0 destroyed`

### 10.3. Teste de Resiliencia

Com o LocalStack desligado, execute `terraform plan`:

```
Error: RequestError: send request failed
caused by: Post "http://localhost:4566/": connect: connection refused
```

O erro e explicito e direciona o usuario a verificar o container.

---

## 11. TRATAMENTO DE DADOS SENSIVEIS

- `access_key` e `secret_key` sao preenchidos com valores ficticios (`mock_access_key` / `mock_secret_key`)
- Nenhuma credencial real da AWS e utilizada ou armazenada
- Arquivos `.tfstate` e diretorio `.terraform/` sao bloqueados pelo `.gitignore`
- Arquivos `.tfvars` com excecao do `terraform.tfvars` sao ignorados pelo git
- Bucket S3 e criado com criptografia AES-256 em repouso e bloqueio total de acesso publico

---

## 12. VARIAVEIS DE CONFIGURACAO

| Variavel                  | Descricao                                   | Valor Padrao            |
|---------------------------|---------------------------------------------|-------------------------|
| `aws_region`              | Regiao AWS do ambiente local                | us-east-1               |
| `bucket_name`             | Nome do bucket S3                           | empresa-arquivos-locais |
| `queue_name`              | Nome da fila SQS                            | fila-processamento-erros|
| `queue_retention_seconds` | Retencao de mensagens na fila (segundos)    | 345600                  |
| `queue_visibility_timeout`| Timeout de visibilidade (segundos)          | 30                      |
| `table_name`              | Nome da tabela DynamoDB                     | tabela-auditoria-logs   |

---

## 13. SOLUCAO DE PROBLEMAS

| Problema                                      | Causa provavel                | Solucao                                   |
|-----------------------------------------------|-------------------------------|-------------------------------------------|
| `connection refused` ao executar terraform    | LocalStack nao esta rodando   | `docker compose up -d`                    |
| `BucketAlreadyExists` ao aplicar              | Bucket ja existe (estado Ok)  | Executar novamente (idempotente)          |
| No module found `boto3`                       | Dependencia Python faltando   | `pip install boto3`                       |
| Provider download fails                       | Sem internet                  | Verificar conexao de rede                 |
| Porta 4566 em uso                             | Outro servico na porta        | Parar o servico conflictante              |
| `terraform init` falha                        | Terraform < 1.5.0             | Atualizar o Terraform                     |

---

## 14. REFERENCIAS

- Documentacao Terraform AWS Provider: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- Documentacao LocalStack: https://docs.localstack.cloud/
- Documentacao boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- Docker Compose: https://docs.docker.com/compose/

---

## 15. LICENCA

Distribuido sob licenca MIT. Consulte o arquivo LICENSE para detalhes.

---

L. A. Leandro - Sao Jose dos Campos, SP - 2026
