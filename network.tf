
# Provision VPC
resource "aws_vpc" "web_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.project_name}-webapp-vpc"
    Description = "Web application VPC"
  }
}

# Provision public subnet
resource "aws_subnet" "public_sn" {
  vpc_id                  = aws_vpc.web_vpc.id
  cidr_block              = "10.0.16.0/24"
  map_public_ip_on_launch = true
  availability_zone       = var.availability_zones[0]

  tags = {
    Name        = "${var.project_name}-public-sn"
    Description = "Web application public subnet to manage resources publicly accessible"
  }
}

resource "aws_subnet" "public_sn_1" {
  vpc_id                  = aws_vpc.web_vpc.id
  cidr_block              = "10.0.17.0/24"
  map_public_ip_on_launch = true
  availability_zone       = var.availability_zones[1]

  tags = {
    Name        = "${var.project_name}-public-sn-1"
    Description = "Web application public subnet to manage resources publicly accessible"
  }
}

# Provision private subnet
resource "aws_subnet" "private_sn" {
  vpc_id            = aws_vpc.web_vpc.id
  cidr_block        = "10.0.32.0/24"
  availability_zone = var.availability_zones[0]

  tags = {
    Name        = "${var.project_name}-private-sn"
    Description = "Web application private subnet to manage resources to be kept private from public"
  }
}

# Provision internet gateway
resource "aws_internet_gateway" "web_igw" {
  vpc_id = aws_vpc.web_vpc.id

  tags = {
    Name        = "${var.project_name}-igw"
    Description = "Web application IPv4 gateway"
  }
}

# Create route tables and routes
resource "aws_route_table" "public_tbl" {
  vpc_id = aws_vpc.web_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.web_igw.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.web_igw.id
  }

  tags = {
    Name        = "${var.project_name}-public"
    Description = "Web application public route table"
  }
}

# Associate subnet with route table
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public_sn.id
  route_table_id = aws_route_table.public_tbl.id
}