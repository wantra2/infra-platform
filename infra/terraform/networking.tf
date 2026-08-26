module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  name = "${var.project_name}-${var.environment}"
  cidr = "10.0.0.0/16"

  azs = [
    "${var.aws_region}a",
    "${var.aws_region}b",
  ]

  public_subnets = [
    "10.0.1.0/24",
    "10.0.2.0/24",
  ]

  private_subnets = [
    "10.0.11.0/24",
    "10.0.12.0/24",
  ]

  enable_nat_gateway   = true
  one_nat_gateway_per_az = true
  enable_vpn_gateway   = false

}