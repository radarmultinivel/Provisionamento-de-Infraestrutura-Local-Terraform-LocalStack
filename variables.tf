# Desenvolvido por L. A. Leandro - Sao Jose dos Campos, SP - 25/05/2026
variable "aws_region" {
  description = "Região AWS utilizada no ambiente local"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Nome do bucket S3 para armazenamento de arquivos"
  type        = string
  default     = "empresa-arquivos-locais"
}

variable "queue_name" {
  description = "Nome da fila SQS de processamento de erros"
  type        = string
  default     = "fila-processamento-erros"
}

variable "queue_retention_seconds" {
  description = "Tempo de retenção de mensagens na fila (segundos)"
  type        = number
  default     = 345600
}

variable "queue_visibility_timeout" {
  description = "Timeout de visibilidade das mensagens (segundos)"
  type        = number
  default     = 30
}

variable "table_name" {
  description = "Nome da tabela DynamoDB de auditoria de logs"
  type        = string
  default     = "tabela-auditoria-logs"
}
