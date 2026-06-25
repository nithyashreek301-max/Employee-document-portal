# Employee Document Portal on AWS

![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)
![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900)
![Flask](https://img.shields.io/badge/App-Flask-000000)
![S3](https://img.shields.io/badge/Storage-S3-569A31)

---

## About the Project

Built a production-grade **Employee Document Management Portal** on AWS — where employees can upload and manage documents through a Flask web application. The entire infrastructure is automated using modular Terraform, with auto-scaling, load balancing, IAM security, and CloudWatch monitoring built in.

---

## Architecture Overview

```
Internet
        ↓
    ALB (Public Subnet)
        ↓
  Target Group (Health Check)
        ↓
┌─────────────────────────────────┐
│       AWS Infrastructure         │
│  VPC → NAT Gateway → ASG →     │
│  EC2 (Private Subnet) →         │
│  S3 (Document Storage)          │
│  IAM Role (No hardcoded creds)  │
│  CloudWatch (Monitoring)        │
└─────────────────────────────────┘
        ↓
  EC2 Instances (Private Subnet)
        ↓
  Flask App (Document Portal)
        ↓
  CloudWatch Alarms (Self-Healing)
```

---

## Tools & Technologies

| Category | Tools |
|---|---|
| Application | Python Flask, Boto3 |
| Cloud Storage | AWS S3 |
| Compute | AWS EC2 |
| Load Balancer | AWS ALB |
| Auto Scaling | AWS ASG |
| Networking | AWS VPC, NAT Gateway, Target Group |
| Security | AWS IAM Role, Security Groups |
| Infrastructure as Code | Terraform (Modular) |
| Remote State | S3 + DynamoDB Locking |
| Monitoring | AWS CloudWatch |
| Region | ap-south-1 (Mumbai) |

---

## Infrastructure Modules

| Module | Purpose |
|---|---|
| vpc | VPC, public/private subnets, NAT Gateway, route tables |
| alb | Application Load Balancer, listener rules |
| target_group | Target Group with health check config, registers ASG instances |
| nat | NAT Gateway in public subnet, Elastic IP, private route table entry |
| asg | Auto Scaling Group, launch template, scaling policies |
| ec2 | EC2 instance config, user data, IMDSv2 enforcement |
| s3 | S3 bucket for document storage, bucket policy |
| iam | IAM Role + Instance Profile for EC2 → S3 access |
| cloudwatch | Alarms for unhealthy ALB targets, self-healing trigger |

---

## Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Home page — shows upload form and document list |
| `/upload` | POST | Accepts file + employee name, uploads to S3 |
| `/health` | GET | Returns 200 OK — used by ALB health checks |

---

## Infrastructure Setup

### VPC & Networking
- Custom VPC with public and private subnets across 2 Availability Zones
- **NAT Gateway** deployed in public subnet with Elastic IP — allows private EC2 instances to reach internet for bootstrapping (cloning app from GitHub, installing packages)
- Route tables configured separately for public and private subnets — private subnets route outbound traffic through NAT Gateway

### Load Balancer & Target Group
- ALB deployed in public subnets, forwards traffic to EC2 on port 5000
- **Target Group** registered with ASG instances — ALB routes requests only to healthy targets
- Health check hits `/health` endpoint every 30 seconds
- Unhealthy instances automatically deregistered from Target Group and replaced by ASG

### Compute & Auto Scaling
- EC2 instances deployed in private subnets (not directly internet-accessible)
- ASG automatically replaces unhealthy instances
- Launch template with IMDSv2 enforced (HttpTokens = required)
- User data script clones app from GitHub and starts Flask on boot

### Storage & IAM
- S3 bucket stores all uploaded employee documents
- IAM Role attached to EC2 — zero hardcoded AWS credentials
- Boto3 picks up credentials automatically via instance metadata

### Remote State
- Terraform state stored in S3 bucket
- DynamoDB table used for state locking (prevents concurrent applies)

---

## Screenshots

### AWS VPC — Subnets and Networking ✅
![VPC](https://github.com/nithyashreek301-max/Employee-document-portal/blob/main/screenshots/VPC.png)

### NAT Gateway — Private Subnet Internet Access ✅
![NAT Gateway](https://github.com/nithyashreek301-max/Employee-document-portal/blob/main/screenshots/NAT.png)

### ALB — Load Balancer Active ✅
![ALB](https://github.com/nithyashreek301-max/Employee-document-portal/blob/main/screenshots/LB.png)

### ASG — Auto Scaling Group Running ✅
![ASG](https://github.com/nithyashreek301-max/Employee-document-portal/blob/main/screenshots/ASG.png)

### EC2 Instances — Running in Private Subnet ✅
![EC2](https://github.com/nithyashreek301-max/Employee-document-portal/blob/main/screenshots/EC2.png)

### Employee Document Portal — Live Application ✅
![App](https://github.com/nithyashreek301-max/Employee-document-portal/blob/main/screenshots/Portal.png)

### CloudWatch Alarm & SNS — Monitoring ✅
![CloudWatch](https://github.com/nithyashreek301-max/Employee-document-portal/blob/main/screenshots/SNS.png)

---

## Key Highlights

- ✅ **Fully automated infrastructure** — entire AWS stack provisioned with Terraform, zero manual console clicks
- ✅ **Modular Terraform** — 7 reusable modules, each managing one layer of infrastructure
- ✅ **Zero hardcoded credentials** — IAM Role on EC2, boto3 uses instance metadata
- ✅ **Self-healing architecture** — CloudWatch alarm + ASG auto-replaces failed instances
- ✅ **Production networking** — NAT Gateway enables private EC2 bootstrapping without public IPs
- ✅ **Target Group health checks** — ALB routes traffic only to healthy EC2 instances
- ✅ **Remote state management** — S3 backend with DynamoDB locking for team-safe applies
- ✅ **IMDSv2 enforced** — EC2 metadata service secured against SSRF attacks

---

## How to Run

### Prerequisites
- Terraform >= 1.5 installed
- AWS CLI configured with appropriate IAM permissions
- S3 bucket and DynamoDB table created for remote state (one-time setup)

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/nithyashreek301-max/Employee-document-portal.git

# 2. Update backend config
# Edit terraform/backend.tf with your S3 bucket and DynamoDB table names

# 3. Initialize Terraform
cd terraform/
terraform init

# 4. Preview the infrastructure
terraform plan

# 5. Deploy everything
terraform apply

# 6. Access the portal
# Copy ALB DNS name from Terraform output and open in browser

# 7. Tear down after demo (avoid NAT Gateway costs)
terraform destroy
```

> ⚠️ **Cost Note:** NAT Gateway charges apply even when EC2 is stopped. Always run `terraform destroy` after demo sessions.

---

## Key Learnings

- Understood how **modular Terraform** keeps infrastructure maintainable and reusable
- Learned how **NAT Gateway** allows private EC2 instances to bootstrap without public IPs — and why it must be in a public subnet with an Elastic IP
- Understood **Target Group** health checks — how ALB uses them to route traffic only to healthy instances and deregister failed ones
- Implemented **IAM Role-based access** eliminating all hardcoded credentials
- Configured **ALB + Target Group** to automatically detect and remove unhealthy instances
- Understood **ASG self-healing** — how CloudWatch alarms trigger instance replacement
- Gained hands-on experience with **Terraform remote state** and DynamoDB locking for safe team collaboration

---

## Author

**Nithyashree K**
- LinkedIn: [linkedin.com/in/nithya30](https://linkedin.com/in/nithya30)
- GitHub: [github.com/nithyashreek301-max](https://github.com/nithyashreek301-max)
