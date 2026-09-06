# ============================================================
# Application Load Balancer
# ============================================================

resource "aws_lb" "app" {
  name               = "${var.project_name}-${var.environment}"
  internal           = false
  load_balancer_type = "application"

  security_groups = [
    aws_security_group.alb.id
  ]

  subnets = module.vpc.public_subnets

}


# ============================================================
# Target Group
# ============================================================

resource "aws_lb_target_group" "app" {
  name = "${var.project_name}-${var.environment}"

  port     = 8000
  protocol = "HTTP"

  target_type = "ip"

  vpc_id = module.vpc.vpc_id

  health_check {
    enabled = true

    path                = "/health"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    matcher             = "200"
  }
}


# ============================================================
# HTTP Listener
# ============================================================

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn

  port     = 80
  protocol = "HTTP"

  default_action {
    type = "forward"

    forward {
      target_group {
        arn = aws_lb_target_group.app.arn
      }
    }
  }

}