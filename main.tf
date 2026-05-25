# Desenvolvido por L. A. Leandro - Sao Jose dos Campos, SP - 25/05/2026
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  region                      = var.aws_region
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3       = "http://localhost:4566"
    sqs      = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
  }
}

# ──────────────────────────────────────────
# Bucket S3 – Armazenamento de objetos
# ──────────────────────────────────────────
resource "aws_s3_bucket" "arquivos" {
  bucket = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "arquivos_encrypt" {
  bucket = aws_s3_bucket.arquivos.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "arquivos_block" {
  bucket = aws_s3_bucket.arquivos.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ──────────────────────────────────────────
# Fila SQS – Mensageria assíncrona
# ──────────────────────────────────────────
resource "aws_sqs_queue" "erros" {
  name                        = var.queue_name
  delay_seconds               = 5
  max_message_size            = 262144
  message_retention_seconds   = var.queue_retention_seconds
  receive_wait_time_seconds   = 10
  visibility_timeout_seconds  = var.queue_visibility_timeout
}

# ──────────────────────────────────────────
# Tabela DynamoDB – Banco NoSQL chave-valor
# ──────────────────────────────────────────
resource "aws_dynamodb_table" "auditoria" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name        = var.table_name
    Environment = "local"
    ManagedBy   = "terraform"
  }
}
