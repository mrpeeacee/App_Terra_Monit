terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "gandalf-web-app-terraform-eks-state-s3-bucket-4565"
    key            = "terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "gandalf-web-app-terraform-eks-state-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.region
}