module "vpc" {
  source = "./modules/vpc"
}

module "security_groups" {

  source = "./modules/security-groups"

  vpc_id = module.vpc.vpc_id
}

module "iam" {

  source = "./modules/iam"
}

module "s3" {

  source = "./modules/s3"
}

module "alb" {

  source = "./modules/alb"

  vpc_id = module.vpc.vpc_id

  public_subnet_ids = module.vpc.public_subnet_ids

  alb_sg_id = module.security_groups.alb_sg_id
}

module "asg" {

  source = "./modules/asg"

  private_subnet_ids = module.vpc.private_subnet_ids

  app_sg_id = module.security_groups.app_sg_id

  target_group_arn = module.alb.target_group_arn

  instance_profile = module.iam.instance_profile_name
}

module "monitoring" {

  source = "./modules/monitoring"

  asg_name = module.asg.asg_name
}