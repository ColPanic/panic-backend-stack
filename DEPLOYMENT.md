# Deployment Guide

This guide covers deploying the AI Backend Services Stack in various environments.

## Local Development

### Quick Start
```bash
# Setup and start
make setup
make up

# Verify everything is working
make health
```

### Custom Configuration
```bash
# Copy and edit environment file
cp .env.example .env
# Edit .env with your settings
make up
```

## Production Deployment

### Docker Compose (Single Server)

1. **Prepare the server:**
   ```bash
   # Install Docker and Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

2. **Deploy the stack:**
   ```bash
   git clone <repository-url>
   cd ai-backend-stack
   cp .env.example .env
   # Edit .env with production settings
   make up
   ```

3. **Configure SSL (recommended):**
   ```bash
   # Update nginx.conf for SSL
   # Add SSL certificates to volumes
   # Restart nginx service
   ```

### Docker Swarm (Multi-Server)

1. **Initialize Swarm:**
   ```bash
   docker swarm init
   ```

2. **Deploy as stack:**
   ```bash
   docker stack deploy -c docker-compose.yml ai-backend
   ```

3. **Scale services:**
   ```bash
   docker service scale ai-backend_postgres=1
   docker service scale ai-backend_redis=1
   docker service scale ai-backend_chromadb=2
   ```

### Kubernetes

#### Using Helm (Recommended)

1. **Add Helm repository:**
   ```bash
   helm repo add ai-backend-stack https://your-org.github.io/ai-backend-stack
   helm repo update
   ```

2. **Install with Helm:**
   ```bash
   helm install ai-backend ai-backend-stack/ai-backend-stack \
     --set postgres.password=secure_password \
     --set redis.password=secure_password \
     --set minio.rootPassword=secure_password
   ```

#### Manual Kubernetes Deployment

1. **Create namespace:**
   ```bash
   kubectl create namespace ai-backend
   ```

2. **Apply manifests:**
   ```bash
   kubectl apply -f k8s/ -n ai-backend
   ```

3. **Configure ingress:**
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: ai-backend-ingress
   spec:
     rules:
     - host: ai-backend.example.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: nginx
               port:
                 number: 80
   ```

## Cloud Platform Deployments

### AWS

#### ECS Fargate

1. **Create task definition:**
   ```json
   {
     "family": "ai-backend-stack",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "1024",
     "memory": "2048",
     "containerDefinitions": [...]
   }
   ```

2. **Create ECS service:**
   ```bash
   aws ecs create-service \
     --cluster ai-backend-cluster \
     --service-name ai-backend-service \
     --task-definition ai-backend-stack \
     --desired-count 1
   ```

#### Using AWS CDK

```typescript
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

const cluster = new ecs.Cluster(this, 'AIBackendCluster', {
  vpc: vpc
});

const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef');

// Add containers for each service
taskDefinition.addContainer('postgres', {
  image: ecs.ContainerImage.fromRegistry('pgvector/pgvector:pg15'),
  memoryLimitMiB: 512,
  environment: {
    POSTGRES_DB: 'ai_app',
    POSTGRES_USER: 'ai_user',
    POSTGRES_PASSWORD: 'secure_password'
  }
});
```

### Google Cloud Platform

#### Cloud Run
```bash
# Deploy each service separately
gcloud run deploy ai-postgres \
  --image pgvector/pgvector:pg15 \
  --platform managed \
  --region us-central1

gcloud run deploy ai-redis \
  --image redis:7-alpine \
  --platform managed \
  --region us-central1
```

#### GKE
```bash
# Create GKE cluster
gcloud container clusters create ai-backend-cluster \
  --num-nodes=3 \
  --machine-type=e2-standard-4

# Deploy using kubectl
kubectl apply -f k8s/
```

### Azure

#### Container Instances
```bash
# Create resource group
az group create --name ai-backend-rg --location eastus

# Deploy container group
az container create \
  --resource-group ai-backend-rg \
  --name ai-backend-stack \
  --file docker-compose.yml
```

#### AKS (Azure Kubernetes Service)
```bash
# Create AKS cluster
az aks create \
  --resource-group ai-backend-rg \
  --name ai-backend-aks \
  --node-count 3

# Get credentials
az aks get-credentials \
  --resource-group ai-backend-rg \
  --name ai-backend-aks

# Deploy
kubectl apply -f k8s/
```

## High Availability Setup

### Database Clustering

#### PostgreSQL Primary-Replica
```yaml
# Add to docker-compose.yml
postgres-replica:
  image: pgvector/pgvector:pg15
  environment:
    PGUSER: replicator
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    POSTGRES_MASTER_SERVICE: postgres
  command: |
    bash -c '
    until pg_basebackup --pgdata=/var/lib/postgresql/data -R --slot=replication_slot --host=postgres --port=5432
    do
    echo "Waiting for master to connect..."
    sleep 1s
    done
    echo "Backup done, starting replica..."
    postgres
    '
```

#### Redis Clustering
```yaml
# Redis cluster setup
redis-cluster:
  image: redis:7-alpine
  command: redis-cli --cluster create 
    redis1:6379 redis2:6379 redis3:6379 
    --cluster-replicas 1 --cluster-yes
```

### Load Balancing

#### Nginx Load Balancer
```nginx
upstream chromadb_backend {
    server chromadb1:8000;
    server chromadb2:8000;
    server chromadb3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://chromadb_backend;
    }
}
```

## Monitoring and Observability

### Prometheus + Grafana

1. **Add monitoring stack:**
   ```yaml
   # monitoring/docker-compose.yml
   prometheus:
     image: prom/prometheus
     ports:
       - "9090:9090"
   
   grafana:
     image: grafana/grafana
     ports:
       - "3000:3000"
   ```

2. **Configure exporters:**
   ```yaml
   postgres-exporter:
     image: prometheuscommunity/postgres-exporter
     environment:
       DATA_SOURCE_NAME: "postgresql://ai_user:password@postgres:5432/ai_app?sslmode=disable"
   
   redis-exporter:
     image: oliver006/redis_exporter
     environment:
       REDIS_ADDR: "redis:6379"
   ```

### Health Monitoring

```bash
# Automated health checks
#!/bin/bash
services=("postgres" "redis" "chromadb" "minio")
for service in "${services[@]}"; do
  if ! make health | grep -q "$service.*Ready"; then
    echo "Service $service is down!"
    # Send alert (email, slack, etc.)
  fi
done
```

## Backup and Recovery

### Automated Backups

```bash
#!/bin/bash
# backup.sh - Daily backup script

# PostgreSQL backup
make backup

# Redis backup
docker exec ai-redis redis-cli --rdb /data/dump.rdb

# MinIO backup (sync to S3)
mc mirror minio/data s3/backup-bucket/$(date +%Y%m%d)

# ChromaDB backup
docker exec ai-chromadb tar czf /chroma/backup_$(date +%Y%m%d).tar.gz /chroma/chroma
```

### Disaster Recovery

1. **Backup verification:**
   ```bash
   # Test backup integrity
   pg_restore --list backup.sql
   ```

2. **Recovery procedure:**
   ```bash
   # Stop services
   make down
   
   # Restore data
   make restore BACKUP=backup.sql
   
   # Start services
   make up
   
   # Verify recovery
   make health
   ```

## Security Hardening

### Network Security

1. **Firewall rules:**
   ```bash
   # Only allow necessary ports
   ufw allow 22    # SSH
   ufw allow 80    # HTTP
   ufw allow 443   # HTTPS
   ufw deny 5432   # Block direct PostgreSQL access
   ufw deny 6379   # Block direct Redis access
   ```

2. **Internal networking:**
   ```yaml
   # Use internal network for service communication
   networks:
     ai-backend:
       driver: bridge
       internal: true
   ```

### Authentication and Authorization

1. **Enable ChromaDB auth:**
   ```bash
   # Edit auth/credentials
   echo "admin:secure_password" > auth/credentials
   ```

2. **PostgreSQL security:**
   ```sql
   -- Create specific users with limited permissions
   CREATE USER app_user WITH PASSWORD 'app_password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON ai_data.* TO app_user;
   ```

3. **Redis security:**
   ```bash
   # Configure Redis ACL
   redis-cli ACL SETUSER app_user on >app_password ~* +@read +@write
   ```

## Performance Optimization

### Resource Allocation

```yaml
# Optimize resource limits based on workload
deploy:
  resources:
    limits:
      memory: 4G      # Increase for large datasets
      cpus: '2.0'     # Increase for high concurrency
    reservations:
      memory: 2G
      cpus: '1.0'
```

### Database Tuning

```sql
-- PostgreSQL optimization
ALTER SYSTEM SET shared_buffers = '25% of RAM';
ALTER SYSTEM SET effective_cache_size = '75% of RAM';
ALTER SYSTEM SET random_page_cost = 1.1;
SELECT pg_reload_conf();
```

### Caching Strategy

```python
# Implement proper caching layers
import redis

cache = redis.Redis(host='localhost', port=6379)

def get_cached_embeddings(text_hash):
    cached = cache.get(f"embedding:{text_hash}")
    if cached:
        return json.loads(cached)
    
    # Generate embedding
    embedding = generate_embedding(text)
    
    # Cache for 1 hour
    cache.setex(f"embedding:{text_hash}", 3600, json.dumps(embedding))
    return embedding
```

## Troubleshooting

### Common Issues

1. **Out of memory:**
   ```bash
   # Check memory usage
   docker stats
   
   # Increase memory limits
   # Edit docker-compose.yml resource limits
   ```

2. **Disk space:**
   ```bash
   # Clean old logs
   docker system prune -f
   
   # Check volume usage
   docker system df
   ```

3. **Network connectivity:**
   ```bash
   # Test service connectivity
   docker exec ai-nginx curl chromadb:8000/api/v1/heartbeat
   ```

### Debug Mode

```bash
# Enable debug logging
LOG_LEVEL=DEBUG make up

# View detailed logs
make logs
```

This deployment guide should cover most scenarios. For specific use cases or issues, please refer to the individual service documentation or open an issue in the repository.