# Observability Stack with Docker Compose

This repository contains a complete observability stack using Docker Compose, including metrics, logs, and traces collection and visualization.

## Components

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation system
- **Promtail**: Log collector for Loki
- **Tempo**: Distributed tracing system
- **Node Exporter**: Host metrics exporter
- **cAdvisor**: Container metrics exporter
- **NGINX with OpenResty**: Demo web server with Lua scripting
- **NGINX Exporter**: NGINX metrics collection
- **Locust**: Load testing tool

---

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of available RAM
- Windows, macOS, or Linux operating system

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/IustinAchitenei/fii-practic-docker-compose.git
cd fii-practic-docker-compose
```

### 2. Start the Stack

```bash
docker-compose up -d
```

This command will start all services defined in the docker-compose.yml file.

---

### 3. Access the Components

- **Grafana**: http://localhost:3000 (default login: admin/admin)
- **Prometheus**: http://localhost:9090
- **Loki**: http://localhost:3100
- **NGINX Demo App**: http://localhost:8080
- **Locust (load testing UI)**: http://localhost:8089
- **Tempo**: http://localhost:3200
- **Node Exporter**: http://localhost:9100
- **cAdvisor**: http://localhost:8081

## Exploring Logs in Grafana

1. Open Grafana at http://localhost:3000
2. Navigate to Explore (compass icon in the left sidebar)
3. Select "Loki" as the data source
4. Use LogQL to query logs, for example:
   - `{container_id=~".+"}` - All logs from all containers
   - `{service="nginx"}` - Only NGINX logs
   - `{http_method="GET"}` - Only GET requests in NGINX logs
   - `{http_path=~"/api.*"}` - Requests to API endpoints

### Sample LogQL Queries:

```
# All NGINX logs
{service="nginx"}

# All 404 responses
{service="nginx", status_code="404"}

# Slow responses (>200ms)
{service="nginx"} |= "time=" | pattern `<_> time=<duration>` | duration > 200ms
```

## Generating Test Traffic with Locust

1. Open Locust at http://localhost:8089
2. Enter the following settings:
   - Number of users: 10
   - Spawn rate: 1
   - Host: http://nginx
3. Click "Start swarming" to begin sending traffic to the NGINX server
4. The Locust file is configured to send various types of requests:
   - Standard GET requests
   - Requests with intentional delays
   - Requests that generate errors
   - Different HTTP methods (GET, POST, PUT, etc.)

---

## Recommended Dashboards to Import

To import dashboards in Grafana:
1. Click on the "+" icon in the left sidebar
2. Select "Import"
3. Enter the dashboard ID
4. Select appropriate data source when prompted

### Recommended Dashboards:

1. **Logs / App Dashboard** - ID: 13639
   - Data source: Loki
   - Provides comprehensive log visualization and filtering

2. **NGINX Exporter Dashboard** - ID: 12708
   - Data source: Prometheus
   - Visualizes NGINX metrics including requests, status codes, and response times

3. **Node Exporter Full Dashboard** - ID: 1860
   - Data source: Prometheus
   - Complete system monitoring with CPU, memory, disk, and network metrics

## Architecture

The system follows a standard observability architecture:

- Metrics: Prometheus scrapes metrics from exporters (NGINX, Node, cAdvisor)
- Logs: Promtail collects container logs and forwards to Loki
- Traces: Applications can send traces to Tempo (sample client not included)
- Visualization: Grafana provides a unified view of all telemetry data

---

### Key Configuration Files:

- `docker-compose.yml`: Main configuration for all services
- `prometheus/prometheus.yml`: Prometheus scrape configuration
- `promtail-config-final.yaml`: Promtail configuration for log collection and processing
- `loki/loki-config.yaml`: Loki server configuration
- `tempo/tempo-config.yaml`: Tempo tracing configuration
- `nginx/nginx.conf`: NGINX configuration

## Troubleshooting

- **Missing logs in Loki**: Check Promtail configuration and container permissions
- **No metrics in Prometheus**: Verify target status in Prometheus UI
- **Dashboard visualization issues**: Ensure metrics naming matches what the dashboard expects
- **Container startup failures**: Check container logs with `docker-compose logs [service-name]`

## Additional Information

- Prometheus metrics are retained for 15 days by default
- Loki logs are retained for 7 days by default
- Tempo traces are retained for 24 hours by default

## Tear Down

```bash
docker-compose down -v
```

