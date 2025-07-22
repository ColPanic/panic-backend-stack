# AI Backend Services Stack

[![Docker](https://img.shields.io/badge/Docker-containerized-blue.svg)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%20with%20pgvector-blue.svg)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-green.svg)](https://www.trychroma.com)
[![MinIO](https://img.shields.io/badge/MinIO-S3%20compatible-orange.svg)](https://min.io)

> **Complete backend infrastructure for AI applications in a single Docker Compose stack**

A production-ready, open-source backend services stack designed specifically for AI applications. Provides PostgreSQL with vector extensions, Redis caching, ChromaDB for embeddings, and MinIO object storage - everything you need to build scalable AI applications.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd ai-backend-stack

# Setup environment
make setup

# Start all services
make up

# Check service health
make health
```

**That's it!** Your AI backend services are now running and ready to use.

## 📋 What's Included

| Service | Purpose | Port | Description |
|---------|---------|------|-------------|
| **PostgreSQL** | Primary Database | 5432 | PostgreSQL 15 with pgvector extension for vector operations |
| **Redis** | Cache & Sessions | 6379 | In-memory data store for caching and session management |
| **ChromaDB** | Vector Database | 8000 | Specialized vector database for embeddings and similarity search |
| **MinIO** | Object Storage | 9000/9001 | S3-compatible object storage for files and documents |
| **Nginx** | Reverse Proxy | 80/443 | Optional reverse proxy for service routing |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                AI Backend Services                      │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ PostgreSQL  │  │    Redis    │  │  ChromaDB   │    │
│  │   +Vector   │  │   Cache     │  │  Embeddings │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐                     │
│  │    MinIO    │  │    Nginx    │                     │
│  │  S3 Storage │  │   Proxy     │                     │
│  └─────────────┘  └─────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

## ⚡ Usage Examples

### Python Application Integration

```python
import asyncpg
import redis
import chromadb
from minio import Minio

# PostgreSQL with vector support
conn = await asyncpg.connect(
    "postgresql://ai_user:ai_secure_password@localhost:5432/ai_app"
)

# Redis for caching
redis_client = redis.Redis(
    host='localhost', port=6379, 
    password='ai_redis_password'
)

# ChromaDB for embeddings
chroma_client = chromadb.HttpClient(host="localhost", port=8000)

# MinIO for file storage
minio_client = Minio(
    "localhost:9000",
    access_key="ai_admin",
    secret_key="ai_minio_password",
    secure=False
)
```

### Node.js Application Integration

```javascript
import { Client } from 'pg';
import Redis from 'redis';
import { ChromaApi } from 'chromadb';
import * as Minio from 'minio';

// PostgreSQL connection
const pgClient = new Client({
  connectionString: 'postgresql://ai_user:ai_secure_password@localhost:5432/ai_app'
});

// Redis connection
const redisClient = Redis.createClient({
  url: 'redis://:ai_redis_password@localhost:6379'
});

// ChromaDB connection
const chromaClient = new ChromaApi({
  path: "http://localhost:8000"
});

// MinIO connection
const minioClient = new Minio.Client({
  endPoint: 'localhost',
  port: 9000,
  useSSL: false,
  accessKey: 'ai_admin',
  secretKey: 'ai_minio_password'
});
```

## 🔧 Commands

### Basic Operations
```bash
make help           # Show all available commands
make setup          # First-time setup
make up             # Start all services
make down           # Stop all services
make restart        # Restart all services
make status         # Show service status
make health         # Check service health
```

### Monitoring & Logs
```bash
make logs           # View all logs
make logs-postgres  # PostgreSQL logs only
make logs-redis     # Redis logs only
make logs-chromadb  # ChromaDB logs only
make logs-minio     # MinIO logs only
```

### Database Operations
```bash
make shell-db       # Open PostgreSQL shell
make shell-redis    # Open Redis CLI
make backup         # Create database backup
make restore BACKUP=file.sql  # Restore from backup
```

### Maintenance
```bash
make clean          # Clean containers and volumes
make reset-minio    # Reset MinIO credentials
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# PostgreSQL Configuration
POSTGRES_DB=ai_app
POSTGRES_USER=ai_user
POSTGRES_PASSWORD=ai_secure_password
POSTGRES_PORT=5432

# Redis Configuration  
REDIS_PASSWORD=ai_redis_password
REDIS_PORT=6379

# ChromaDB Configuration
CHROMA_PORT=8000

# MinIO Configuration
MINIO_ROOT_USER=ai_admin
MINIO_ROOT_PASSWORD=ai_minio_password
MINIO_API_PORT=9000
MINIO_CONSOLE_PORT=9001
```

### Performance Tuning

Adjust resource limits in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
    reservations:
      memory: 512M
      cpus: '0.5'
```

## 🔒 Security

### Production Deployment

1. **Change Default Passwords**: Update all passwords in `.env`
2. **Enable Authentication**: Uncomment ChromaDB auth in `auth/credentials`
3. **Use SSL**: Configure SSL certificates for Nginx
4. **Network Security**: Place services behind firewall
5. **Backup Strategy**: Implement regular backups

### Network Security
```bash
# Restrict external access (production)
POSTGRES_PORT=127.0.0.1:5432
REDIS_PORT=127.0.0.1:6379
CHROMA_PORT=127.0.0.1:8000
```

## 📊 Monitoring

### Health Checks

All services include health checks:
- **PostgreSQL**: `pg_isready` command
- **Redis**: `ping` command
- **ChromaDB**: HTTP heartbeat endpoint
- **MinIO**: Health endpoint

### Resource Monitoring

```bash
# View resource usage
make status

# Monitor specific service
docker stats ai-postgres
```

## 🔧 Troubleshooting

### Common Issues

**MinIO Login Failed?**
```bash
make reset-minio
```

**Database Connection Issues?**
```bash
make health
make logs-postgres
```

**Out of Memory?**
```bash
# Adjust memory limits in docker-compose.yml
# Check resource usage
make status
```

### Port Conflicts

If default ports are in use, update `.env`:
```bash
POSTGRES_PORT=5433
REDIS_PORT=6380
CHROMA_PORT=8001
```

## 🚀 Production Deployment

### Docker Swarm
```bash
docker stack deploy -c docker-compose.yml ai-backend
```

### Kubernetes
Use the provided manifests in `k8s/` directory:
```bash
kubectl apply -f k8s/
```

### Cloud Deployment

- **AWS**: Use ECS/Fargate with provided task definitions
- **GCP**: Deploy to Cloud Run or GKE
- **Azure**: Use Container Instances or AKS

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone <repository-url>
cd ai-backend-stack
make setup
make up
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/ai-backend-stack/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ai-backend-stack/discussions)
- **Documentation**: [Full Documentation](docs/)

## ⭐ Acknowledgments

- [PostgreSQL](https://postgresql.org) - The world's most advanced open source relational database
- [pgvector](https://github.com/pgvector/pgvector) - Open-source vector similarity search for Postgres
- [Redis](https://redis.io) - The open source, in-memory data store
- [ChromaDB](https://www.trychroma.com) - The open-source embedding database
- [MinIO](https://min.io) - High Performance Object Storage

---

**Made with ❤️ for the AI community**