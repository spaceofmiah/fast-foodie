output "prod_lb_domain" {
  value = aws_lb.webapp_backend.dns_name
}