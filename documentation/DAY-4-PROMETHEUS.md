# Day 4 — Prometheus Monitoring

## Objective
Implement server monitoring using Prometheus and Node Exporter, allowing the EC2 instance's resource metrics and monitoring health to be collected and queried.

## 1. Monitoring Architecture

Two monitoring services were added to the existing Docker Compose infrastructure:

- **Prometheus:** Collects and stores time-series metrics.
- **Node Exporter:** Exposes Linux host-level metrics, including CPU and memory information.

Prometheus scrapes both itself and Node Exporter every 30 seconds.

## 2. Prometheus Configuration

Created `prometheus/prometheus.yml`.

Configuration:
- Scrape interval: 30 seconds
- Evaluation interval: 30 seconds
- Prometheus target: `localhost:9090`
- Node Exporter target: `node-exporter:9100`

## 3. Docker Compose Implementation

Added two services:

### Node Exporter
- Image: `prom/node-exporter:v1.9.1`
- Collects host-level Linux metrics.
- Uses the host PID namespace.
- Mounts the host filesystem read-only.
- Memory limit: 64 MB
- CPU limit: 0.25 CPU

### Prometheus
- Image: `prom/prometheus:v3.5.0`
- Dashboard bound to `127.0.0.1:9090`.
- Persistent storage using the `prometheus-data` Docker volume.
- Data retention: 7 days.
- Storage retention limit: 512 MB.
- Memory limit: 256 MB
- CPU limit: 0.50 CPU

Port 9090 was not exposed publicly. Dashboard access was configured through an SSH tunnel.

## 4. Verification and Testing

Successfully verified:

- Docker Compose configuration validation.
- Both monitoring containers started successfully.
- Prometheus loaded its configuration.
- Prometheus server became ready.
- Prometheus target API reported both targets as `UP`.
- Prometheus Targets dashboard was accessible.
- Prometheus Graph interface was accessible through SSH tunnelling.

### Verified Targets

| Target | Status |
|---|---|
| Prometheus | UP |
| Node Exporter | UP |

## 5. Security Considerations

- Prometheus dashboard is bound to localhost on the EC2 host.
- No public inbound security-group rule was added for port 9090.
- Node Exporter port 9100 was not published to the host.
- Dashboard access uses SSH port forwarding.
- Prometheus data is stored in a persistent Docker volume.

## 6. Outcome

Successfully integrated Prometheus monitoring into the existing multi-tier application without intentionally recreating or interrupting the application containers.

The infrastructure now supports basic monitoring of server health, CPU activity, and memory usage.

## 7. Technologies Used

- AWS EC2
- Docker Compose
- Prometheus
- Node Exporter

