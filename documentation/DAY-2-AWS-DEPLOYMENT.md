# AWS EC2 Deployment – Project Progress Log

**Date:** 23 November 2026  
**Project:** Multi-Tier Monitoring Application  
**Platform:** AWS EC2  
**Region:** US East (N. Virginia)

## 1. Objective

Deploy my existing multi-tier User Management System on an AWS EC2 instance using Docker Compose.

The application consists of:
- Nginx – Reverse proxy
- Frontend – User interface
- Flask – Backend API
- PostgreSQL – Database

## 2. AWS EC2 Configuration

| Component | Configuration |
|---|---|
| Operating System | Ubuntu Server 24.04 LTS |
| Instance Type | t3.small |
| vCPUs | 2 |
| RAM | 2 GB |
| Storage | 12 GB gp3 EBS |
| Region | us-east-1 |
| Security Group | launch-wizard-1 |

### Security Group Rules

| Service | Port | Access |
|---|---|---|
| SSH | 22 | My IP |
| HTTP | 80 | Anywhere (0.0.0.0/0) |

SSH access was initially open to all IP addresses and was restricted to my own IP after deployment.

## 3. Work Completed

### Step 1: EC2 Setup
- Launched an Ubuntu 24.04 EC2 instance.
- Created and downloaded an RSA key pair.
- Connected to the instance using SSH from Windows PowerShell.
- Verified that all three EC2 status checks passed.

### Step 2: Docker Installation
- Installed Docker Engine using the official Docker Ubuntu repository.
- Installed and verified Docker Compose.
- Confirmed that the Docker service was running.
- Used `sudo docker` commands to manage containers.

### Step 3: Project Configuration
- Accessed my existing GitHub project repository.
- Reviewed the Docker Compose configuration.
- Created a `.env` file containing PostgreSQL database configuration.
- Set restrictive permissions on `.env` using `chmod 600`.
- Verified that `.env` was ignored by Git.
- Validated the Compose configuration using:

```bash
sudo docker compose config --quiet
```

### Step 4: Building Docker Images

Built the backend image:

```bash
sudo docker compose build backend
```

Built the frontend image:

```bash
sudo docker compose build frontend
```

Both images built successfully.

### Step 5: Deploying Containers

Started the PostgreSQL database:

```bash
sudo docker compose up -d db
```

Verified that PostgreSQL became healthy.

Started the Flask backend:

```bash
sudo docker compose up -d backend
```

Verified that the backend passed its health check.

Started the frontend:

```bash
sudo docker compose up -d frontend
```

Started the Nginx reverse proxy:

```bash
sudo docker compose up -d nginx
```

### Step 6: Nginx Reverse Proxy

Configured Nginx to route requests:

- `/` → Frontend container
- `/api/` → Flask backend container

Only port 80 was exposed publicly. PostgreSQL and Flask remained accessible through the internal Docker network.

### Step 7: Application Testing

Tested the frontend locally:

```bash
curl -I http://localhost
```

Result: `HTTP 200 OK`

Tested the backend health endpoint:

```bash
curl -i http://localhost/api/health
```

Result:

```json
{"status":"healthy"}
```

Tested public access through the EC2 public IPv4 address.

The User Management System loaded successfully in the browser.

Finally:
- Added a test user.
- Verified that the user appeared in the list.
- Refreshed the page.
- Confirmed that the user remained saved.

This verified communication between the frontend, Flask backend and PostgreSQL database, including persistent storage.

## 4. Troubleshooting Performed

- Investigated initial browser connection timeout.
- Checked Ubuntu UFW status; firewall was inactive.
- Verified that Docker was listening on port 80.
- Checked AWS Security Group inbound rules.
- Tested external connectivity using Windows PowerShell:

```powershell
Test-NetConnection <EC2-PUBLIC-IP> -Port 80
```

- Confirmed successful TCP connectivity.
- Resolved the browser access issue and verified the application.

## 5. Final Architecture

```text
             Internet
                 |
                 v
          AWS EC2 Instance
                 |
                 v
          Nginx Reverse Proxy
              Port 80
                 |
          +------+------+
          |             |
          v             v
       Frontend      Flask API
                         |
                         v
                    PostgreSQL
                         |
                         v
                  Docker Volume
```

## 6. End-of-Day Status

All four containers were running successfully, and the application was accessible publicly.

The EC2 instance was stopped after completing deployment to avoid unnecessary compute charges. The EBS volume and its data were retained.

## 7. Next Steps
Restart EC2 and verify that the application starts correctly.
