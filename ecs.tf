resource "aws_ecs_cluster" "webapp" {
  name = "${var.project_name}-cluster"
}

resource "aws_ecs_task_definition" "webapp_backend" {
  cpu                      = 256
  memory                   = 512
  network_mode             = "awsvpc"
  family                   = "${var.project_name}-backend"
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = aws_iam_role.webapp_backend.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = templatefile(
    "templates/backend_container.json.tpl",
    {
      region  = var.region
      name    = "${var.project_name}-backend"
      image   = aws_ecr_repository.backend.repository_url
      command = ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
    }
  )
}

resource "aws_ecs_service" "webapp_backend" {
  task_definition                    = aws_ecs_task_definition.webapp_backend.arn
  deployment_minimum_healthy_percent = 50
  name                               = "${var.project_name}-backend"
  cluster                            = aws_ecs_cluster.webapp.id
  deployment_maximum_percent         = 200
  launch_type                        = "FARGATE"
  desired_count                      = 1

  network_configuration {
    subnets          = [aws_subnet.public_sn.id]
    security_groups  = [aws_security_group.webapp_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.webapp_backend.arn
    container_name   = "${var.project_name}-backend"
    container_port   = 8000
  }
}