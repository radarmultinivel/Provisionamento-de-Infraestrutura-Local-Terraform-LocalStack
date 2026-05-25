# Desenvolvido por L. A. Leandro - Sao Jose dos Campos, SP - 25/05/2026
import sys
import uuid
import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"
BUCKET = "empresa-arquivos-locais"
QUEUE = "fila-processamento-erros"
TABLE = "tabela-auditoria-logs"

config = Config(
    region_name=REGION,
    retries={"max_attempts": 1, "mode": "standard"},
)

session = boto3.Session(
    aws_access_key_id="mock_access_key",
    aws_secret_access_key="mock_secret_key",
)


def test_s3():
    client = session.client("s3", endpoint_url=ENDPOINT, config=config)
    key = f"teste-{uuid.uuid4()}.txt"
    client.put_object(Bucket=BUCKET, Key=key, Body=b"conteudo-verificacao-localstack")
    obj = client.get_object(Bucket=BUCKET, Key=key)
    body = obj["Body"].read().decode()
    assert body == "conteudo-verificacao-localstack", f"S3: conteudo inesperado: {body}"
    client.delete_object(Bucket=BUCKET, Key=key)
    print(f"[S3 OK] Bucket '{BUCKET}' – objeto criado, lido e removido com sucesso.")
    return True


def test_sqs():
    client = session.client("sqs", endpoint_url=ENDPOINT, config=config)
    queue_url = client.get_queue_url(QueueName=QUEUE)["QueueUrl"]
    msg_body = json.dumps({"id": str(uuid.uuid4()), "origem": "verify_infra", "status": "teste"})
    client.send_message(QueueUrl=queue_url, MessageBody=msg_body)
    resp = client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=5)
    messages = resp.get("Messages", [])
    assert len(messages) == 1, f"SQS: nenhuma mensagem recebida em {QUEUE}"
    receipt = messages[0]["ReceiptHandle"]
    client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
    body = json.loads(messages[0]["Body"])
    assert body["status"] == "teste", f"SQS: payload inesperado: {body}"
    print(f"[SQS OK] Fila '{QUEUE}' – mensagem enviada, recebida e removida com sucesso.")
    return True


def test_dynamodb():
    client = session.client("dynamodb", endpoint_url=ENDPOINT, config=config)
    item_id = str(uuid.uuid4())
    client.put_item(
        TableName=TABLE,
        Item={
            "id": {"S": item_id},
            "evento": {"S": "validacao-infraestrutura"},
            "timestamp": {"S": "2026-01-01T00:00:00Z"},
        },
    )
    resp = client.get_item(TableName=TABLE, Key={"id": {"S": item_id}})
    item = resp.get("Item", {})
    assert item.get("evento", {}).get("S") == "validacao-infraestrutura", (
        f"DynamoDB: item inesperado: {item}"
    )
    client.delete_item(TableName=TABLE, Key={"id": {"S": item_id}})
    print(f"[DynamoDB OK] Tabela '{TABLE}' – item inserido, lido e removido com sucesso.")
    return True


def main():
    print("=" * 60)
    print(" Smoke Test – Infraestrutura Local (LocalStack)")
    print("=" * 60)

    tests = [
        ("S3", test_s3),
        ("SQS", test_sqs),
        ("DynamoDB", test_dynamodb),
    ]

    results = {}
    exit_code = 0

    for name, func in tests:
        try:
            func()
            results[name] = "PASS"
        except ClientError as e:
            results[name] = "FAIL"
            exit_code = 1
            print(f"[{name} ERRO] {e.response['Error']['Code']}: {e.response['Error']['Message']}")
        except AssertionError as e:
            results[name] = "FAIL"
            exit_code = 1
            print(f"[{name} FALHA] {e}")
        except Exception as e:
            results[name] = "FAIL"
            exit_code = 1
            print(f"[{name} EXCEÇÃO] {e}")

    print()
    print("-" * 60)
    for service, status in results.items():
        icon = "✓" if status == "PASS" else "✗"
        print(f" {icon} {service}: {status}")

    print("-" * 60)
    if exit_code == 0:
        print(" RESULTADO: INFRAESTRUTURA VALIDADA COM SUCESSO ✓")
    else:
        print(" RESULTADO: FALHA NA VALIDAÇÃO – revise os logs acima ✗")
    print("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
