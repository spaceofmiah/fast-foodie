resource "aws_ecr_repository" "backend" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"
}

# currently thinking either or not to 
# automate provisioning ecr or manually 
# handle it