# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}


# Create a VPC
resource "aws_vpc" "webapp_vpc" {
  cidr_block = "10.0.0.0/16"


  tags = {
    Name        = "webapp-vpc"
    Description = "Web application VPC"
  }
}


# Create public subnet
resource "aws_subnet" "pub_sbn" {
  vpc_id                  = aws_vpc.webapp_vpc.id
  cidr_block              = "10.0.16.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name        = "wba-public-sbn"
    Description = "Web application public subnet to manage resources publicly accessible"
  }
}


# Create private subnet
resource "aws_subnet" "priv_sbn" {
  vpc_id     = aws_vpc.webapp_vpc.id
  cidr_block = "10.0.32.0/24"

  tags = {
    Name        = "wba-private-sbn"
    Description = "Web application private subnet to manage resources to be kept private from public"
  }
}


# Create an internet gateway
resource "aws_internet_gateway" "webapp_igw" {
  vpc_id = aws_vpc.webapp_vpc.id

  tags = {
    Name        = "webapp_igw"
    Description = "Web application IPv4 gateway"
  }
}


# Create route tables and routes
resource "aws_route_table" "webapp_pub_rtbl" {
  vpc_id = aws_vpc.webapp_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.webapp_igw.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.webapp_igw.id
  }

  tags = {
    Name        = "webapp_pub_rtbl"
    Description = "Web application public route table"
  }
}

# Associate subnet with route table
resource "aws_route_table_association" "webapp_pub_rtbl_ass" {
  subnet_id      = aws_subnet.pub_sbn.id
  route_table_id = aws_route_table.webapp_pub_rtbl.id
}


# Create TLS security group
resource "aws_security_group" "webapp_sg" {
  name        = "webapp-tls-sg"
  description = "Allow inbound traffic into web application VPC"
  vpc_id      = aws_vpc.webapp_vpc.id

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.webapp_vpc.cidr_block]
  }

  ingress {
    description = "SSH from VPC"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.webapp_vpc.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "webapp_tls_sg"
  }
}

# Create EC2 instance
resource "aws_instance" "webapp" {
  ami             = "ami-0b5eea76982371e91"
  instance_type   = "t2.micro"
  subnet_id       = aws_subnet.pub_sbn.id
  security_groups = [aws_security_group.webapp_sg.id]

  tags = {
    Name = "webapp"
  }
}