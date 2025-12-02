output "website_url" {
  value = "http://${aws_s3_bucket_website_configuration.website.website_endpoint}"
}

output "api_url" {
  value = "${aws_apigatewayv2_stage.default.invoke_url}/api"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.frontend.id
}