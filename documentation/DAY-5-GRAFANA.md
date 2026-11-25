# Day 5 — Grafana Monitoring Dashboards

## Objective

Integrate Grafana into the existing Docker Compose monitoring infrastructure and build a centralized dashboard for visualizing EC2 infrastructure metrics collected by Prometheus.

## 1. Monitoring Architecture

Grafana was added to the existing monitoring stack.

The monitoring architecture now consists of:

- **Node Exporter:** Collects Linux host-level metrics.
- **Prometheus:** Scrapes, stores, and provides metrics through PromQL.
- **Grafana:** Connects to Prometheus and visualizes infrastructure metrics through dashboards.

Grafana communicates with Prometheus internally using the Docker Compose service network.

### Data Source Configuration

Configured Prometheus as Grafana's data source using:

`http://prometheus:9090`

This allows Grafana to query Prometheus without exposing the Prometheus service publicly.

## 2. Dashboard Implementation

Created and saved a Grafana dashboard named:

**EC2 Infrastructure Monitoring**

The dashboard organizes four monitoring panels in a two-column, two-row layout.

### Panel 1: CPU Utilization (%)

Displays CPU utilization over time using Node Exporter metrics.

### Panel 2: RAM Utilization (%)

Displays the percentage of physical memory currently in use.

PromQL query:

```promql
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

Uses available memory rather than simply subtracting free memory, accounting for reclaimable Linux cache and buffers.

### Panel 3: Root Disk Utilization (%)

Displays the percentage of space used on the root filesystem.

PromQL query:

```promql
100 * (1 - (
  node_filesystem_avail_bytes{mountpoint="/", fstype!="tmpfs"}
  /
  node_filesystem_size_bytes{mountpoint="/", fstype!="tmpfs"}
))
```

### Panel 4: Network Traffic (bps)

Monitors incoming and outgoing network traffic using Node Exporter interface metrics.

**Incoming traffic:**

```promql
rate(node_network_receive_bytes_total{device!="lo"}[5m]) * 8
```

**Outgoing traffic:**

```promql
rate(node_network_transmit_bytes_total{device!="lo"}[5m]) * 8
```

The `rate()` function calculates the average per-second traffic rate over a five-minute window.

The results are converted from bytes per second to bits per second.

Configured separate legend labels:

- Incoming
- Outgoing

The visualization uses SI bits-per-second units.

## 3. Dashboard Organization

The dashboard was arranged into a two-column layout:

| Position | Monitoring Panel |
|---|---|
| Row 1 — Left | CPU Utilization (%) |
| Row 1 — Right | RAM Utilization (%) |
| Row 2 — Left | Root Disk Utilization (%) |
| Row 2 — Right | Network Traffic (bps) |

This layout provides a centralized view of the EC2 instance's resource utilization and network activity.

## 4. Verification and Testing

Successfully verified:

- Grafana container started successfully.
- Grafana interface was accessible through the configured access method.
- Prometheus was successfully connected as a Grafana data source.
- Dashboard was created and saved.
- CPU utilization panel was working.
- RAM utilization panel was working.
- Root disk utilization panel was working.
- Network traffic panel displayed incoming and outgoing metrics.
- Dashboard layout and panel legends were finalized.

## 5. Security Considerations

- Grafana communicates with Prometheus through the internal Docker Compose network.
- Prometheus continues to use its existing localhost-bound host port configuration.
- No public inbound security-group rule was added for Prometheus.
- Existing SSH-based access configuration was preserved.
- Existing persistent Prometheus storage was preserved.

## 6. Outcome

Successfully integrated Grafana into the existing multi-tier monitoring infrastructure.

The project now has a centralized monitoring dashboard providing visibility into:

- CPU utilization
- RAM utilization
- Root filesystem utilization
- Incoming and outgoing network traffic

This establishes a basic infrastructure observability layer using Prometheus, Node Exporter, and Grafana.

## 7. Technologies Used

- Docker Compose
- Prometheus
- Node Exporter
- Grafana
- PromQL
