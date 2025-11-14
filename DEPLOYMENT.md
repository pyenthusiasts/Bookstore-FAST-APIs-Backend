# Production Deployment Guide

This guide provides comprehensive instructions for deploying the Bookstore API to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Database Setup](#database-setup)
5. [Monitoring](#monitoring)
6. [Backup & Recovery](#backup--recovery)
7. [Security Considerations](#security-considerations)
8. [Performance Tuning](#performance-tuning)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- Kubernetes 1.24+ (for K8s deployment)
- kubectl configured
- PostgreSQL 15+ (for production database)
- Redis 7+ (for caching and rate limiting)
- SSL certificates (for HTTPS)

## Docker Deployment

### 1. Production Configuration

```bash
# Copy production environment file
cp .env.production.example .env.production

# Edit and configure all values
nano .env.production
```

**Important: Update these values:**
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `SQLALCHEMY_DATABASE_URL`: PostgreSQL connection string
- `BACKEND_CORS_ORIGINS`: Your domain(s)
- Database passwords
- Redis password

### 2. Build and Deploy

```bash
# Build production image
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# Seed database (optional)
docker-compose -f docker-compose.prod.yml exec api python scripts/seed_database.py
```

### 3. Verify Deployment

```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f api

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health/ready
```

## Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl create namespace bookstore
kubectl config set-context --current --namespace=bookstore
```

### 2. Configure Secrets

```bash
# Create secrets from file
kubectl create secret generic bookstore-secrets \
  --from-literal=secret-key=$(openssl rand -hex 32) \
  --from-literal=database-url='postgresql://user:pass@host:5432/db'

# Or apply from secrets.yaml
cp k8s/secrets.yaml.example k8s/secrets.yaml
# Edit secrets.yaml with your values
kubectl apply -f k8s/secrets.yaml
```

### 3. Deploy Application

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods
kubectl describe pod <pod-name>

# Check services
kubectl get svc

# Check ingress
kubectl get ingress

# View logs
kubectl logs -f deployment/bookstore-api

# Test health check
kubectl port-forward svc/bookstore-api-service 8000:80
curl http://localhost:8000/api/v1/health/ready
```

## Database Setup

### PostgreSQL Production Setup

```bash
# Create database and user
psql -U postgres
CREATE DATABASE bookstore;
CREATE USER bookstore WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE bookstore TO bookstore;
\q

# Run migrations
alembic upgrade head

# Or in Docker
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# View migration history
alembic history
```

## Monitoring

### Prometheus Metrics

Metrics are exposed at `/metrics` endpoint:

```bash
# Access metrics
curl http://localhost:8000/metrics
```

Available metrics:
- `http_requests_total`: Total HTTP requests
- `http_request_duration_seconds`: Request duration
- `http_requests_in_progress`: In-progress requests
- `database_connections`: Active DB connections

### Health Checks

- `/health`: Basic health check
- `/api/v1/health/live`: Liveness probe
- `/api/v1/health/ready`: Readiness probe
- `/api/v1/health/detailed`: Detailed health information

### Log Aggregation

Logs are structured and output to stdout. Configure your log aggregation:

```yaml
# Example: Fluentd, Logstash, etc.
# All requests include X-Request-ID for tracing
```

## Backup & Recovery

### Automated Backups

```bash
# Setup cron job for daily backups
0 2 * * * /path/to/scripts/backup_database.sh

# Or use K8s CronJob
kubectl apply -f k8s/cronjob-backup.yaml
```

### Manual Backup

```bash
# Run backup script
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=bookstore
export DB_USER=bookstore
export DB_PASSWORD=your-password
./scripts/backup_database.sh
```

### Restore from Backup

```bash
# Restore database
./scripts/restore_database.sh /backups/bookstore_20240101_120000.sql.gz
```

## Security Considerations

### 1. Secret Management

- **Never** commit `.env` files or secrets to version control
- Use secret management tools (Vault, AWS Secrets Manager, etc.)
- Rotate secrets regularly

### 2. SSL/TLS

```bash
# Generate SSL certificate (Let's Encrypt)
certbot certonly --standalone -d api.yourdomain.com

# Or use cert-manager in Kubernetes
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml
```

### 3. Security Headers

All security headers are automatically added:
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security
- Content-Security-Policy

### 4. Rate Limiting

Configured at multiple levels:
- Application middleware (100 requests/minute per IP)
- Nginx (10 requests/second with burst)
- Kubernetes Ingress annotations

### 5. Database Security

- Use strong passwords
- Enable SSL for database connections
- Restrict database network access
- Regular security updates

## Performance Tuning

### Application Level

```python
# config.py
WEB_CONCURRENCY = 4  # Number of worker processes
MAX_WORKERS = 10     # Max concurrent workers
```

### Database Connection Pooling

```python
# Increase pool size for high traffic
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### Redis Caching

```python
# Add caching for frequently accessed data
from redis import Redis
redis_client = Redis.from_url(REDIS_URL)
```

### Nginx Tuning

```nginx
worker_processes auto;
worker_connections 2048;
keepalive_timeout 65;
```

## Troubleshooting

### Common Issues

#### 1. Application Won't Start

```bash
# Check logs
docker-compose logs api
kubectl logs deployment/bookstore-api

# Check environment variables
docker-compose exec api env
kubectl exec deployment/bookstore-api -- env
```

#### 2. Database Connection Errors

```bash
# Test database connectivity
docker-compose exec api python -c "
from app.db.database import engine
try:
    engine.connect()
    print('Connected!')
except Exception as e:
    print(f'Error: {e}')
"
```

#### 3. Memory Issues

```bash
# Check memory usage
docker stats
kubectl top pods

# Increase memory limits
# Edit k8s/deployment.yaml resources section
```

#### 4. High CPU Usage

```bash
# Check CPU usage
docker stats
kubectl top pods

# Scale horizontally
kubectl scale deployment/bookstore-api --replicas=5
```

### Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Access container shell
docker-compose exec api /bin/bash
kubectl exec -it deployment/bookstore-api -- /bin/bash

# Check network connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- sh
```

## Production Checklist

Before going to production:

- [ ] All secrets are properly configured
- [ ] SSL certificates are installed and valid
- [ ] Database backups are automated
- [ ] Monitoring and alerting are configured
- [ ] Rate limiting is enabled
- [ ] CORS is properly configured
- [ ] Health checks are passing
- [ ] Load testing is completed
- [ ] Disaster recovery plan is documented
- [ ] Security audit is performed
- [ ] Log aggregation is configured
- [ ] Metrics are being collected
- [ ] Auto-scaling is configured
- [ ] Documentation is up to date

## Support

For issues and questions:
- GitHub Issues: https://github.com/pyenthusiasts/Bookstore-FAST-APIs-Backend/issues
- Documentation: See README.md
