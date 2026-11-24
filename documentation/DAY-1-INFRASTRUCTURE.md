# Day 1 – Local Infrastructure & Docker Compose

## Objective

Build a multi-tier web application infrastructure using Docker Compose, configure communication between services, implement health checks, and establish reliable service startup dependencies.

## 1. Project Overview

The project is a containerized User Management System consisting of four main services:

- **Frontend:** Web interface served through Nginx.
- **Backend:** Flask application handling API requests.
- **Database:** PostgreSQL for persistent user data.
- **Reverse Proxy:** Nginx routing incoming HTTP traffic to the frontend and backend.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Python / Flask | Backend API |
| PostgreSQL 16 | Relational database |
| Nginx | Reverse proxy and frontend web server |
| Linux / Ubuntu | Development environment |

## 3. Container Architecture

```text
                  Client / Browser
                         |
                         |
                    Nginx Proxy
                     Port 80
                         |
                -------------------
                |                 |
                v                 v
             Frontend          Backend
             Nginx             Flask
             Port 80            Port 5000
                                   |
                                   |
                                   v
                               PostgreSQL
                               Port 5432
```

All services communicate through Docker's internal network.

Only the Nginx reverse proxy exposes an HTTP port to the host. PostgreSQL and Flask remain accessible internally through the Docker network.

## 4. Docker Compose Configuration

Configured the following services in `docker-compose.yml`:

- PostgreSQL database using `postgres:16`.
- Flask backend built from the backend Dockerfile.
- Frontend built from the frontend Dockerfile.
- Nginx reverse proxy using `nginx:alpine`.

Used Docker Compose to manage the complete application stack.

```bash
docker compose up -d --build
```

To inspect running containers:

```bash
docker compose ps
```

## 5. Service Dependencies and Health Checks

Configured service dependencies to improve startup reliability.

Implemented health checks for:

- PostgreSQL database.
- Flask backend health endpoint.

The backend health endpoint is:

```text
/health
```

The health checks allow Docker Compose to determine whether critical services are ready.

Configured dependent services to wait for the required service health conditions before starting.

## 6. Networking and Reverse Proxy

Configured Nginx to route incoming requests:

| Request Path | Destination |
|---|---|
| `/` | Frontend |
| `/api/` | Flask Backend |

The reverse proxy communicates with other containers using their Docker Compose service names.

This avoids exposing internal service ports directly to the host.

## 7. Persistent Database Storage

Configured a named Docker volume:

```yaml
volumes:
  postgres-data:
```

Mounted this volume inside the PostgreSQL container to preserve database data beyond the lifetime of an individual container.

This separates persistent database storage from the container itself.

## 8. Testing and Verification

Verified the application using Docker Compose and HTTP requests.

Check running containers:

```bash
docker compose ps
```

Test frontend:

```bash
curl -I http://localhost
```

Test backend health through Nginx:

```bash
curl -i http://localhost/api/health
```

Expected backend response:

```json
{
  "status": "healthy"
}
```

Verified that the frontend loaded successfully and that user creation and retrieval worked through the application.

## 9. Key Concepts Learned

- Docker images and containers.
- Docker Compose service orchestration.
- Container networking and service discovery.
- Health checks and service dependencies.
- Nginx reverse proxy configuration.
- Named volumes and persistent storage.
- Internal versus externally exposed ports.
- Multi-tier application architecture.

## Outcome

Successfully built and tested a multi-container application locally using Docker Compose.

The infrastructure established the foundation for deploying the application to AWS EC2.

**Next: Day 2 – AWS EC2 Deployment.**
