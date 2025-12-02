terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. GET THE EXISTING LAB ROLE (Critical for Learner Lab)
data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

# 2. CREATE ECR REPOSITORY
resource "aws_ecr_repository" "repo" {
  name         = var.ecr_repo_name
  force_delete = true # Allows destroying even if it contains images
}

# 3. BUILD & PUSH DOCKER IMAGE
resource "null_resource" "docker_build_push" {
  triggers = {
    dockerfile = filemd5("../Dockerfile")
  }

  provisioner "local-exec" {
    interpreter = ["cmd", "/C"]
    
    command = "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.repo.registry_id}.dkr.ecr.${var.aws_region}.amazonaws.com && docker build --provenance=false -t ${aws_ecr_repository.repo.repository_url}:latest ../ && docker push ${aws_ecr_repository.repo.repository_url}:latest"
  }
}

# 4. LAMBDA FUNCTION
resource "aws_lambda_function" "func" {
  function_name = "${var.app_name}-function"
  role          = data.aws_iam_role.lab_role.arn # Use the imported LabRole
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.repo.repository_url}:latest"
  timeout       = 30
  memory_size   = 1024

  # Wait for the docker image to be pushed before creating the function
  depends_on = [null_resource.docker_build_push]
}

# 4a. CLOUDWATCH LOG GROUP FOR LAMBDA (so terraform can destroy it)
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.func.function_name}"
  
  retention_in_days = 1 
}

# 5. API GATEWAY (HTTP API)
resource "aws_apigatewayv2_api" "api" {
  name          = "${var.app_name}-api"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["content-type"]
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.func.invoke_arn
}

resource "aws_apigatewayv2_route" "any_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "ANY /api"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.func.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*/api"
}

# 6. S3 FRONTEND
resource "aws_s3_bucket" "frontend" {
  bucket_prefix = "${var.app_name}-frontend-"
  force_destroy = true # Allows deleting bucket even if not empty
}

# Disable "Block Public Access" (Required for static website)
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = false
  ignore_public_acls      = false
  block_public_policy     = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.frontend.id
  index_document { suffix = "index.html" }
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.frontend.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend.arn}/*"
      }
    ]
  })
  depends_on = [aws_s3_bucket_public_access_block.public_access]
}

# 7. UPLOAD FILES (With API URL Injection!)
resource "aws_s3_object" "html_files" {
  for_each     = fileset("../", "*.html")
  bucket       = aws_s3_bucket.frontend.id
  key          = each.value
  source       = "../${each.value}"
  content_type = "text/html"
}

resource "aws_s3_object" "css_files" {
  for_each     = fileset("../", "*.css")
  bucket       = aws_s3_bucket.frontend.id
  key          = each.value
  source       = "../${each.value}"
  content_type = "text/css"
}

# Special handling for script.js to inject the API URL
resource "aws_s3_object" "script_js" {
  bucket       = aws_s3_bucket.frontend.id
  key          = "script.js"
  content_type = "application/javascript"
  
  content = templatefile("../script.js.tftpl", {
    api_url = "${aws_apigatewayv2_stage.default.invoke_url}/api"
  })
}

# Upload images folder
resource "aws_s3_object" "images" {
  for_each     = fileset("../images", "*")
  bucket       = aws_s3_bucket.frontend.id
  key          = "images/${each.value}"
  source       = "../images/${each.value}"
}