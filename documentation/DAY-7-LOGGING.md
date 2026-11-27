# Day 7 — Logging, Troubleshooting & Linux Diagnostics

## 1. Objective

Implement Docker log rotation, inspect application and infrastructure logs, simulate a service failure, verify recovery, and create a reusable Linux system diagnostic script.

## 2. Docker Log Rotation

Configured the Docker `json-file` logging driver for all eight services using a shared YAML anchor in `docker-compose.yml`.

**Configuration:**
- Logging driver: `json-file`
- Maximum log file size: `10m`
- Maximum number of files: `3`
- Approximate retained log allowance: 30 MB per container

Applied the configuration using Docker Compose and verified the effective settings with `docker inspect`.

All eight containers were verified with the expected logging driver and rotation options.

## 3. Container Log Inspection

Inspected logs from the following services:

| Container | Observations |
|---|---|
| flask-backend | PostgreSQL connection successful; Flask application started; health requests returned HTTP 200 |
| postgres-db | PostgreSQL 16.16 started successfully; database was already initialized |
| nginx-proxy | Nginx startup completed without observed startup errors |

The Flask development server warning was observed and recorded. Replacing the development server was outside the scope of this day's work.

## 4. Backend Failure Simulation and Recovery

Performed a controlled backend outage test:

1. Stopped the Flask backend container using `docker stop flask-backend`.
2. Requested `/api/health` through Nginx.
3. The request timed out after 10 seconds with curl error 28.
4. Restarted the backend using `docker start flask-backend`.
5. Verified that the API returned HTTP 200 OK with:

`{"status":"healthy"}`

This demonstrated the observable impact of backend unavailability and successful manual recovery.

## 5. Linux System Diagnostics

Created a reusable Bash script:

`scripts/system-check.sh`

The script checks:

- Memory usage and availability using `free -h`
- Root filesystem capacity using `df -h /`
- System uptime and load averages using `uptime`
- Top memory-consuming processes using `ps`

The script was given owner-only permissions:

`chmod 700 scripts/system-check.sh`

Successfully executed the script on the EC2 instance.

### Container Health Check Script

Created a second reusable Bash script:

`scripts/container-health.sh`

The script performs three checks:

- Validates the Docker Compose configuration.
- Displays the status of all Compose services.
- Checks the application API health endpoint using curl.

Successfully executed the script. Compose validation passed, all eight containers were running, and the API returned HTTP 200 OK.

The script is executable and intended to be run from the project directory.
### Observed EC2 Metrics

| Metric | Observed value |
|---|---:|
| Total RAM | 1.9 GiB |
| Available RAM | 1.2 GiB |
| Swap | 0 B |
| Root disk usage | 51% |
| Root disk available | 5.3 GiB |
| Load average | 0.04, 0.05, 0.00 |

Grafana was the largest memory-consuming process in the observed process listing, using approximately 236 MB RSS.

These measurements represent one diagnostic snapshot, not continuous monitoring results.

## 6. Outcome

- Configured and verified Docker log rotation for all eight services.
- Inspected application, database, and reverse-proxy logs.
- Simulated a backend failure and verified manual recovery.
- Created a reusable Linux diagnostic script.
- Checked EC2 memory, disk, system load, and process usage.

## 7. Files Updated

- `docker-compose.yml`
- `scripts/system-check.sh`
- `documentation/DAY-7-LOGGING.md`
- `scripts/container-health.sh`
