variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "app_name" {
  description = "Application name"
  default     = "vc-app"
}

variable "ecr_repo_name" {
  description = "Name of the ECR repository"
  default     = "vc-app"
}