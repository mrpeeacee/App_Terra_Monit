provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "gandalf-web-app-terraform-eks-state-s3-bucket-4565"

  lifecycle {
    prevent_destroy = false
  }
}


resource "aws_dynamodb_table" "terraform_locks" {
  name         = "gandalf-web-app-terraform-eks-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}