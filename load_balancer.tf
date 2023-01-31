resource "aws_lb" "webapp_backend" {
  name               = "${var.project_name}-backend"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.webapp_sg.id, ]
  subnets            = [
    aws_subnet.public_sn.id, 
    aws_subnet.public_sn_1.id
  ]
}


resource "aws_lb_target_group" "webapp_backend" {
  name        = "${var.project_name}-backend"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.web_vpc.id
  target_type = "ip"
}


resource "aws_lb_listener" "webapp-http" {
  load_balancer_arn = aws_lb.webapp_backend.arn
  port              = "80"
  protocol          = "HTTP"
  depends_on        = [aws_lb_target_group.webapp_backend]

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webapp_backend.arn
  }
}