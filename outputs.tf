# Desenvolvido por L. A. Leandro - Sao Jose dos Campos, SP - 25/05/2026
output "bucket_arn" {
  description = "ARN do bucket S3 provisionado"
  value       = aws_s3_bucket.arquivos.arn
}

output "bucket_name" {
  description = "Nome do bucket S3 criado"
  value       = aws_s3_bucket.arquivos.bucket
}

output "queue_arn" {
  description = "ARN da fila SQS provisionada"
  value       = aws_sqs_queue.erros.arn
}

output "queue_url" {
  description = "URL da fila SQS para envio de mensagens"
  value       = aws_sqs_queue.erros.url
}

output "dynamodb_table_arn" {
  description = "ARN da tabela DynamoDB provisionada"
  value       = aws_dynamodb_table.auditoria.arn
}

output "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB criada"
  value       = aws_dynamodb_table.auditoria.name
}

output "localstack_endpoint" {
  description = "Endpoint local do LocalStack para testes"
  value       = "http://localhost:4566"
}
