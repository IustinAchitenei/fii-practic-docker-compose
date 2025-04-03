# Observability Demo: NGINX + Prometheus + Grafana + Elasticsearch + Locust

This project demonstrates a full observability pipeline using Docker. It includes:
- NGINX with Lua delay for traffic simulation
- Prometheus for metrics
- Grafana for visualization
- cAdvisor for container monitoring
- Locust for load testing
- Elasticsearch + Filebeat for centralized logging

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/IustinAchitenei/fii-practic-docker-compose.git
cd fii_practic_grafana
```

### 2. Start all services
```bash
docker-compose up --build
```
This will spin up:
- NGINX (web server with simulated latency)
- Prometheus (scraping metrics)
- Grafana (for dashboards)
- cAdvisor (container monitoring)
- Locust (load testing UI)
- Filebeat (log shipper)
- Elasticsearch (log storage)

---

## Verify Services Are Running

### NGINX
Visit: [http://EC2-public-ip:8080](http://EC2-public-ip:8080)  
You should see: `Hello! Simulated delay: XXXms`

### Prometheus
Visit: [http://EC2-public-ip:9090](http://EC2-public-ip:9090)  
Try queries like:
- `up`
- `nginx_http_requests_total`
- `nginx_connections_active`

### Grafana
Visit: [http://EC2-public-ip:3000](http://EC2-public-ip:3000)  
Login: `admin / admin`  
Add these data sources:
- **Prometheus** → `http://prometheus:9090`
- **Elasticsearch** → `http://elasticsearch:9200`
  - Index: `docker-logs-*`
  - Timestamp field: `@timestamp`

### Locust
Visit: [http://EC2-public-ip:8089](http://EC2-public-ip:8089)

- Users: `1000`
- Spawn rate: `10`
- Host: `http://nginx`

Click **Start** to generate traffic.

---

## Grafana Dashboards

### 🔹 Dashboard 1: NGINX Metrics

- **Active connections**: `nginx_connections_active`
- **Request rate (RPS)**: `rate(nginx_http_requests_total[1m])`
- **4xx / 5xx errors**: `rate(nginx_http_requests_total{code=~"4.."}[1m])`
- **Accepted connections**: `nginx_connections_accepted`
- **Connection states**: `nginx_connections_reading`, `writing`, `waiting`

### 🔹 Dashboard 2: Container Metrics (via cAdvisor)

- **CPU Usage % per Container**:
```promql
rate(container_cpu_usage_seconds_total[1m]) * 100
```
- **Memory Usage % per Container**:
```promql
(container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100
```
- **Network I/O**:
```promql
rate(container_network_receive_bytes_total[1m])
rate(container_network_transmit_bytes_total[1m])
```

### 🔹 Dashboard 3: Logs from Elasticsearch

Create:
- **Logs panel** → Query type: Logs, Lucene query: `*`
- **Bar chart** of log volume by container: group by `container.name`
- **Line chart** of log rate: metric = Count, group by `@timestamp`

**Example queries:**
- All logs: `*`
- Only NGINX: `container.name: nginx`
- Errors: `message: 404 OR message: 500`

---

## Tear Down

```bash
docker-compose down -v
```

---

## Repo Structure

```
project-root/
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   └── delay.lua
├── prometheus/
│   └── prometheus.yml
├── filebeat/
│   └── filebeat.yml
├── locust/
│   └── locustfile.py
```

