# Create TLS security group
resource "aws_security_group" "webapp_sg" {
  name        = "webapp-tls-sg"
  description = "Allow inbound traffic into web application VPC"
  vpc_id      = aws_vpc.web_vpc.id

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.web_vpc.cidr_block]
  }

  ingress {
    description = "SSH from VPC"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.web_vpc.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-tls-sg"
  }
}