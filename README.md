# App_Terra_Monit
This repo contains an end to end DevOps project with application, IAC, monitoring and observability using Ansible, Terraform and EKS cluster



```markdown
# Gandalf Web App

## Overview
This is a simple Python Flask web application with three main features:

1. **`/gandalf`** – Shows an image of Gandalf.  
2. **`/colombo`** – Shows the current time in Colombo, Sri Lanka in JSON format.  
3. **`/metrics`** – Provides Prometheus metrics counting requests to `/gandalf` and `/colombo`.

The app uses Python 3 and the Flask framework. Gandalf’s image is stored in the `static/` folder as `gandalf.jpg`.

---

## Project Structure

```

gandalf-webapp/

1. app.py             # Main Flask application code
2. requirements.txt   # Python dependencies
3. Dockerfile         # Dockerfile to containerize the app
4. README.md          # This README
5. static/
   └── gandalf.jpg    # Gandalf image
6. venv/              # Optional: local Python virtual environment

````

---

## Step 1: Download the Code

1. Clone the repository:

```bash
git clone <your-repo-url>
cd gandalf-webapp
````

2. Ensure the following files exist:

* `app.py`
* `requirements.txt`
* `static/gandalf.jpg`
* `Dockerfile`
* `README.md`

---

## Step 2: Set Up Python Environment

1. Check Python version (Python 3.12+ required):

```bash
python3 --version
```

2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
```

> **Why virtual environment (venv)?**
> It keeps all project dependencies isolated from other Python projects and avoids conflicts.

3. Activate the virtual environment:

```bash
source venv/bin/activate   # MacOS/Linux
venv\Scripts\activate      # Windows
```

---

## Step 3: Install Dependencies

1. Upgrade pip and install required packages:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

> Make sure the file name is exactly `requirements.txt`.

---

## Step 4: Run the Flask App Locally

```bash
python3 app.py
```

You should see something like:

```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.0.16:8080
```

---

## Step 5: Test the Application

Open your browser or use `curl`:

* Gandalf image:

```bash
http://127.0.0.1:8080/gandalf
```

* Colombo time:

```bash
http://127.0.0.1:8080/colombo
```

* Prometheus metrics:

```bash
http://127.0.0.1:8080/metrics
```

---

## Step 6: Dockerize the Application

Your Dockerfile is configured as follows:

```dockerfile
FROM python:3.12-slim-bookworm AS base

WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code and static folder
COPY . .

# Expose the internal Flask port
EXPOSE 8080

# Run the Flask app
ENTRYPOINT ["python", "app.py"]
```

Build and run the container:

```bash
docker build -t gandalf-webapp:1.0 .
sudo docker run -d -p 80:8080 gandalf-webapp:1.0
```

### Explanation:

* **Internal Flask port:** 8080 (inside container)
* **External port:** 80 (host/public), satisfies assignment requirement “only port 80 should be open”
* Browser and Prometheus can access the app using port 80.

Explanation:

The container itself does not have a public IP.

Your host machine’s IP (127.0.0.1 or 192.168.x.x) is what you can use to access it from your laptop.

This is fine for local testing only.

Check running containers:

```bash
docker ps
```

You should see something like:

```
CONTAINER ID   IMAGE                 COMMAND        STATUS     PORTS
8cb653912f8f   gandalf-webapp:1.0   "python app.py"  Up 5s   0.0.0.0:80->8080/tcp
```

---


````markdown
# EKS-Terraform

## Overview

This repository contains Terraform code to provision a VPC and Amazon EKS cluster with remote state management using S3 and DynamoDB.  
It also includes setup instructions for essential DevOps tooling on Linux — AWS CLI, Terraform, kubectl, and eksctl — to manage and interact with the EKS environment.

---

## Repository Structure

1. backend/  
   Terraform backend configuration for remote state.  
   - terraform.tfstate – Terraform state placeholder (ignored in Git)  
   - Creates S3 bucket for state storage  
   - Creates DynamoDB table for state locking and consistency

2. modules/ – Reusable Terraform modules  
   - vpc/ – Contains networking resources such as VPC, subnets, route tables, and security groups  
   - eks/ – Handles EKS cluster creation, node groups, and IAM roles  

3. main.tf – Main Terraform configuration tying together modules and resources  
4. variables.tf – Input variables for customizing infrastructure  
5. outputs.tf – Outputs for resources created (e.g., VPC ID, EKS endpoint)

---

## Features

- VPC creation with public and private subnets, internet gateway, and route tables  
- Managed EKS cluster with worker nodes and IAM roles  
- Terraform backend configuration using S3 and DynamoDB  
- Modular, reusable, and maintainable Terraform code  
- Follows Terraform best practices for state management and separation of components

---

## Prerequisites

Before deploying this setup, ensure that you have the following:

- AWS account with appropriate IAM permissions  
- Linux-based environment or WSL  
- AWS CLI, Terraform, kubectl, and eksctl installed  
- Configured AWS credentials (aws configure)

---

## DevOps Tooling Setup Guide on Linux

This section guides you through installing and configuring the required tools to manage the EKS environment.

---
### Prerequisites

Ensure you have the following installed on your Linux system:
---
### Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
aws configure
````

---

### Install Terraform

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt-get update && sudo apt-get install terraform -y

terraform -version
```

---

### Configure kubeconfig for EKS

```bash
aws eks --region eu-north-1 update-kubeconfig --name my-eks-cluster
```

---

### Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

---

### Install eksctl

```bash
curl -sLO "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz"
tar -xzf eksctl_$(uname -s)_amd64.tar.gz
sudo mv eksctl /usr/local/bin
eksctl version
```

---

## Usage

1. Initialize Terraform:

   ```bash
   terraform init
   ```

2. Plan infrastructure:

   ```bash
   terraform plan
   ```

3. Apply changes:

   ```bash
   terraform apply
   ```

4. Destroy resources (if needed):

   ```bash
   terraform destroy
   ```

---

## Notes

* .terraform directories and terraform.tfstate files are ignored in Git
* Modify variables in variables.tf or terraform.tfvars to customize the setup
* Run Terraform commands from the root directory
* Always destroy resources when not in use to avoid unwanted AWS costs

---

## Author

Nikhil MG

```
```markdown

## Why This Project?
I created this automation to monitor my Kubernetes applications running on AWS. Instead of manual setup, this Ansible project automatically deploys Prometheus to collect and visualize metrics from my K8s cluster.

## What Problem It Solves
- **Manual setup eliminated** - No more installing Prometheus manually on each server
- **Consistent deployments** - Same configuration every time
- **Quick monitoring** - Get metrics in minutes instead of hours
- **Cost control** - Easy to shutdown when not needed

## How It Helps My K8s Cluster
- Tracks application performance
- Monitors service health
- Collects metrics from Load Balancer endpoints
- Provides visibility into my applications

## Files:

### 1. Create EC2 Instance
**File:** `ec2_create.yaml`
- Creates security group with SSH and Prometheus ports
- Launches EC2 instance
- Shows public IP address

### 2. Install Prometheus  
**File:** `galaxy_prometheus.yml`
- Downloads Prometheus
- Sets up configuration
- Starts Prometheus service on port 9090

### 3. Shutdown EC2
**File:** `ec2_shutdown.yml`
- Safely shuts down the EC2 instance

## Quick Commands:

```bash
# Create EC2
ansible-playbook ec2_create.yaml --vault-password-file vault.pass

# Install Prometheus  
ansible-playbook -i inventory.ini galaxy_prometheus.yml --vault-password-file vault.pass

# Shutdown EC2
ansible-playbook -i inventory.ini ec2_shutdown.yml --vault-password-file vault.pass
```

## What it Monitors:
- Prometheus itself (localhost:9090)
- My Kubernetes apps (13.61.235.125:80, 51.21.111.226:80)

## Access:
After installation, go to: `http://<EC2_IP>:9090`


```


