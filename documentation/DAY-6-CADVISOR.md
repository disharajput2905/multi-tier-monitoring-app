# Day 6 — Docker Container Monitoring with cAdvisor

## Objective

Integrate cAdvisor into the existing Docker Compose monitoring infrastructure to collect and visualize resource usage metrics for individual Docker containers.

## 1. Monitoring Architecture

Added cAdvisor to the existing monitoring stack.

The monitoring architecture now consists of:

- **Node Exporter:** Collects Linux host-level metrics.
- **Prometheus:** Scrapes and stores monitoring metrics.
- **Grafana:** Visualizes infrastructure and container metrics.
- **cAdvisor:** Collects resource usage metrics from running Docker containers.

cAdvisor exposes container metrics on port `8080`, which Prometheus scrapes internally through the Docker Compose network.

## 2. cAdvisor Deployment

Deployed cAdvisor using:

`ghcr.io/google/cadvisor:v0.60.6`

Configured the following:

- Docker socket access for container discovery.
- Read-only access to host filesystem and system information.
- Automatic container restart using `unless-stopped`.
- Memory limit of 128 MB.
- CPU limit of 0.25 cores.

The cAdvisor service was integrated into the existing Docker Compose configuration without replacing the existing application or monitoring services.

## 3. Prometheus Configuration

Added cAdvisor as a Prometheus scrape target.

Target:

`cadvisor:8080`

Configured a 30-second scrape interval.

Prometheus successfully discovered the cAdvisor endpoint and reported the target status as **UP**.

## 4. Grafana Dashboard Implementation

Created and saved a separate Grafana dashboard named:

**Docker Container Monitoring**

The dashboard contains the following panels:

### Panel 1: Docker Container CPU Usage

PromQL query:

```promql
rate(container_cpu_usage_seconds_total{id=~".*docker-.*"}[5m]) * 100
```

Displays CPU consumption over time for individual Docker container cgroups.

### Panel 2: Docker Container Memory Usage

PromQL query:

```promql
container_memory_working_set_bytes{id=~".*docker-.*"}
```

Displays the working-set memory consumption of individual Docker container cgroups.

Both panels successfully returned multiple container metric series.

## 5. Verification and Testing

Successfully verified:

- cAdvisor container started successfully.
- Prometheus cAdvisor scrape target reported UP.
- Container CPU metrics were available.
- Container memory metrics were available.
- Grafana CPU panel displayed multiple metric series.
- Grafana memory panel displayed multiple metric series.
- Dashboard was saved separately from the existing EC2 Infrastructure Monitoring dashboard.
- Existing application and monitoring services were preserved.

Container network metrics were found in Prometheus, but the filtered network queries did not produce usable panel results. Network monitoring was therefore left out of the completed dashboard.

## 6. Security and Resource Considerations

- cAdvisor communicates with Prometheus through the internal Docker Compose network.
- No public inbound security-group rule was added for cAdvisor.
- Existing Prometheus and Grafana access restrictions were preserved.
- cAdvisor was configured with explicit CPU and memory limits to reduce resource consumption on the 2 GiB EC2 instance.
- Existing application and monitoring data volumes were preserved.

## 7. Outcome

Successfully integrated cAdvisor into the existing monitoring infrastructure.

The project now provides two separate monitoring views:

- **EC2 Infrastructure Monitoring:** Host-level CPU, RAM, disk, and network metrics.
- **Docker Container Monitoring:** Individual container CPU and memory metrics.

This extends the project's observability capabilities from host-level monitoring to container-level resource monitoring.

## 8. Technologies Used

- Docker Compose
- cAdvisor
- Prometheus
- Grafana
- PromQL
