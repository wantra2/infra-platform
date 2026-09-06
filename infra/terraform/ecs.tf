# ============================================================
# ECS Cluster
# ============================================================

resource "aws_ecs_cluster" "app" {
  name = "${var.project_name}-${var.environment}"


}

# ============================================================
# ECS Task Execution Role
# ============================================================

resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project_name}-${var.environment}-ecs-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

}


# AWS-managed policy required for standard ECS task execution:
# - Pull container images
# - Write logs to CloudWatch
# - Other standard ECS execution operations

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


# Our additional permission:
# ECS needs to retrieve the RDS-managed master password
# from Secrets Manager.

resource "aws_iam_policy" "ecs_secrets" {
  name = "${var.project_name}-${var.environment}-ecs-secrets"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "secretsmanager:GetSecretValue"
        ]

        Resource = aws_db_instance.postgres.master_user_secret[0].secret_arn
      }
    ]
  })

}

resource "aws_iam_role_policy_attachment" "ecs_secrets" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = aws_iam_policy.ecs_secrets.arn
}


# ============================================================
# CloudWatch Logs
# ============================================================

resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 7

}

# ============================================================
# ECS Task Definition
# ============================================================

resource "aws_ecs_task_definition" "app" {
  family = "${var.project_name}-${var.environment}"

  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  cpu    = 256
  memory = 512

  execution_role_arn = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = var.container_image
      essential = true

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]

      # These are deliberately NOT DATABASE_URL.
      #
      # The application config.py builds database_url
      # from these values when DATABASE_URL is absent.

      environment = [
        {
          name  = "DB_HOST"
          value = aws_db_instance.postgres.address
        },
        {
          name  = "DB_PORT"
          value = tostring(aws_db_instance.postgres.port)
        },
        {
          name  = "DB_NAME"
          value = var.db_name
        },
        {
          name  = "DB_USERNAME"
          value = var.db_username
        },
        {
          name  = "ENVIRONMENT"
          value = var.environment
        }
      ]

      # Only the password comes from Secrets Manager.
      secrets = [
        {
          name = "DB_PASSWORD"

          valueFrom = "${aws_db_instance.postgres.master_user_secret[0].secret_arn}:password::"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"

        options = {
          awslogs-group         = aws_cloudwatch_log_group.app.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "app"
        }
      }
    }
  ])

}


# ============================================================
# ECS Service
# ============================================================

resource "aws_ecs_service" "app" {
  name = "${var.project_name}-${var.environment}"

  cluster = aws_ecs_cluster.app.id

  task_definition = aws_ecs_task_definition.app.arn

  desired_count = 1

  launch_type = "FARGATE"

  network_configuration {
    # ECS tasks run in the private subnets.
    subnets = module.vpc.private_subnets

    security_groups = [
      aws_security_group.ecs.id
    ]

    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port    = 8000
  }

}