
variable "region" {
  description = "AWS regions to create resource in"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name to use in resource name"
  default     = "efood"
}

variable "availability_zones" {
  description = "Availability zones"
  default     = ["us-east-1a", "us-east-1b"]
}

variable "aws_access_key_id" {

}

variable "aws_secret_access_key" {

}