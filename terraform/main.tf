######
# VPC
######
# module "dwh-vpc" {
#   source           = "terraform-aws-modules/vpc/aws"
#   version          = "~> 2.0"
#   name             = "dwh-vpc"
#   cidr             = "10.10.0.0/16"
#   azs              = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
#   redshift_subnets = ["10.10.41.0/24", "10.10.42.0/24", "10.10.43.0/24"]
# }

module "sg" {
  source  = "terraform-aws-modules/security-group/aws//modules/redshift"
  version = "~> 3.0"

  name   = "dwh-redshift"
  vpc_id = "vpc-d0f07fb4"

  # Allow ingress rules to be accessed only within current VPC
  ingress_cidr_blocks = ["172.31.0.0/16"]

  # Allow all rules for all protocols
  egress_rules = ["all-all"]
}

module "redshift" {
  source  = "terraform-aws-modules/redshift/aws"
  version = "~> 2.0"

  cluster_identifier      = "dwh-cluster"
  cluster_node_type       = "dc2.large"
  cluster_number_of_nodes = 1

  cluster_database_name   = "dwh"
  cluster_master_username = "dwhuser"
  cluster_master_password = "Passw0rd"

  # Group parameters
  wlm_json_configuration = "[{\"query_concurrency\": 5}]"

  # DB Subnet Group Inputs
  subnets = ["subnet-22a1097a", "subnet-fc43d88a", "subnet-a6412fc2"]
  vpc_security_group_ids = [module.sg.this_security_group_id]

  # IAM Roles
  cluster_iam_roles = [aws_iam_role.redshift-iam-role.arn]
}