# AI Backend Services Stack

[![Docker](https://img.shields.io/badge/Docker-containerized-blue.svg)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%20with%20pgvector-blue.svg)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-green.svg)](https://www.trychroma.com)
[![MinIO](https://img.shields.io/badge/MinIO-S3%20compatible-orange.svg)](https://min.io)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3%20management-orange.svg)](https://rabbitmq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Complete backend infrastructure for AI applications in a single Docker Compose stack**

A production-ready, open-source backend services stack designed specifically for AI applications. Provides PostgreSQL with vector extensions, Redis caching, ChromaDB for embeddings, MinIO object storage, RabbitMQ message queue, and Nginx reverse proxy - everything you need to build scalable AI applications.

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
| **RabbitMQ** | Message Queue | 5672/15672 | AMQP message broker for async processing and notifications |
| **Nginx** | Reverse Proxy | 80/443 | HTTP reverse proxy for service routing and load balancing |

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────────────────────────────┐
│  Your AI App    │────│            Nginx Proxy                 │
│                 │    │          (Port 80/443)                 │
└─────────────────┘    └─────────────┬───────────────────────────┘
                                     │
                       ┌─────────────┼───────────────────────────┐
                       │             │                           │
                       ▼             ▼                           ▼
              ┌─────────────┐ ┌─────────────┐          ┌─────────────┐
              │ PostgreSQL  │ │    Redis    │          │  ChromaDB   │
              │ + pgvector  │ │   Cache     │          │ Embeddings  │
              │ (Port 5432) │ │ (Port 6379) │          │ (Port 8000) │
              └─────────────┘ └─────────────┘          └─────────────┘
                      │               │                        │
                      ▼               ▼                        ▼
              ┌─────────────┐ ┌─────────────┐          ┌─────────────┐
              │Vector & SQL │ │Cache & Keys │          │   Vector    │
              │   Storage   │ │   Storage   │          │Collections  │
              └─────────────┘ └─────────────┘          └─────────────┘

                       ┌─────────────┐          ┌─────────────┐
                       │    MinIO    │          │  RabbitMQ   │
                       │   Object    │          │  Message    │
                       │   Storage   │          │    Queue    │
                       │(Port 9000)  │          │(Port 5672)  │
                       └─────────────┘          └─────────────┘
                               │                        │
                               ▼                        ▼
                       ┌─────────────┐          ┌─────────────┐
                       │Files & Docs │          │   Async     │
                       │   Storage   │          │ Processing  │
                       └─────────────┘          └─────────────┘
```

<details>
<summary>🎨 Interactive Diagram (for Mermaid-compatible viewers)</summary>

```mermaid
graph TB
    Client[Your Application] --> Nginx[Nginx Reverse Proxy]
    Nginx --> PG[PostgreSQL + pgvector]
    Nginx --> Redis[Redis Cache]
    Nginx --> Chroma[ChromaDB]
    Nginx --> MinIO[MinIO Object Storage]
    Nginx --> Rabbit[RabbitMQ]
    
    PG --> VectorData[(Vector Data)]
    Redis --> CacheData[(Cache)]
    Chroma --> Embeddings[(Embeddings)]
    MinIO --> Files[(Files & Objects)]
    Rabbit --> Queue[(Message Queue)]
    
    classDef service fill:#e1f5fe
    classDef storage fill:#f3e5f5
    class PG,Redis,Chroma,MinIO,Rabbit service
    class VectorData,CacheData,Embeddings,Files,Queue storage
```

</details>

## ⚡ Key Features

### 🔧 Easy Setup & Management
- **One-Command Deploy**: `make setup && make up` gets everything running
- **20+ Make Commands**: Complete operational toolkit included
- **Health Monitoring**: Built-in health checks for all services
- **Auto-Recovery**: Restart policies and failure handling

### 🏗️ Production Ready
- **Resource Limits**: Pre-configured memory and CPU limits
- **Data Persistence**: All data persisted with Docker volumes
- **Security**: Configurable authentication and network isolation
- **Scalability**: Resource optimization and scaling guidelines

### 🔍 AI-Optimized
- **Vector Operations**: PostgreSQL with pgvector for similarity search
- **Embeddings Storage**: ChromaDB for AI embedding workflows
- **File Processing**: MinIO for document and media storage
- **Async Processing**: RabbitMQ for AI model queues and notifications

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

# RabbitMQ Configuration
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_AMQP_PORT=5672
RABBITMQ_MANAGEMENT_PORT=15672

# Nginx Configuration
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
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

## 💻 Usage Examples

### Python Application Integration

```python
import asyncpg
import redis
import chromadb
from minio import Minio
import pika

# PostgreSQL with vector support
conn = await asyncpg.connect(
    "postgresql://ai_user:ai_secure_password@localhost:5432/ai_app"
)

# Execute vector similarity search
result = await conn.fetch("""
    SELECT filename, content_type, 
           embedding <-> $1 AS distance
    FROM ai_data.documents 
    ORDER BY embedding <-> $1 
    LIMIT 10
""", your_query_vector)

# Redis for caching
redis_client = redis.Redis(
    host='localhost', port=6379, 
    password='ai_redis_password'
)

# ChromaDB for embeddings
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection("my_collection")

# MinIO for file storage
minio_client = Minio(
    "localhost:9000",
    access_key="ai_admin",
    secret_key="ai_minio_password",
    secure=False
)

# RabbitMQ for message queuing
rabbitmq_connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/', 
                             pika.PlainCredentials('guest', 'guest'))
)
```

### Node.js Application Integration

```javascript
import { Client } from 'pg';
import Redis from 'redis';
import { ChromaApi } from 'chromadb';
import * as Minio from 'minio';
import amqp from 'amqplib';

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

// RabbitMQ connection
const rabbitmqConnection = await amqp.connect('amqp://guest:guest@localhost:5672');
```

## 🔧 Commands

### Basic Operations
```bash
make help           # Show all available commands
make setup          # First-time setup
make up             # Start all services
make down           # Stop all services
make restart        # Restart all services
make status         # Show service status and resource usage
make health         # Check service health
```

### Monitoring & Logs
```bash
make logs           # View all logs
make logs-postgres  # PostgreSQL logs only
make logs-redis     # Redis logs only
make logs-chromadb  # ChromaDB logs only
make logs-minio     # MinIO logs only
make logs-rabbitmq  # RabbitMQ logs only
```

### Database Operations
```bash
make shell-db       # Open PostgreSQL shell
make shell-redis    # Open Redis CLI
```

### Data Management
```bash
make backup         # Create PostgreSQL database backup
make restore BACKUP=file.sql  # Restore from backup
make reset-data     # Reset all data while preserving credentials
```

**Reset Data Command**: Safely removes all data from PostgreSQL, Redis, ChromaDB, MinIO, and RabbitMQ while preserving:
- All passwords and credentials from `.env` file
- ChromaDB authentication configuration in `./auth/`
- Docker container and network configurations

### Maintenance
```bash
make clean          # Clean containers and volumes
make reset-minio    # Reset MinIO credentials
```

## 🗄️ Database Schema

### Pre-configured AI Schema

The stack includes a pre-configured PostgreSQL schema optimized for AI applications:

```sql
-- Vector-enabled document storage
CREATE TABLE ai_data.documents (
    id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    content_type VARCHAR(100),
    file_size BIGINT,
    embedding vector(1536), -- OpenAI embedding compatible
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Conversation/chat history
CREATE TABLE ai_data.conversations (
    id UUID PRIMARY KEY,
    session_id VARCHAR(255),
    message_text TEXT,
    user_id VARCHAR(255),
    is_bot_response BOOLEAN,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE
);
```

### Vector Operations

```sql
-- Find similar documents using cosine similarity
SELECT filename, embedding <-> $1 AS distance
FROM ai_data.documents 
ORDER BY embedding <-> $1 
LIMIT 10;

-- Find documents within similarity threshold
SELECT * FROM ai_data.documents 
WHERE embedding <-> $1 < 0.5;
```

## 🔒 Security

### Production Deployment

1. **Change Default Passwords**: Update all passwords in `.env`
2. **Enable Authentication**: 
   ```bash
   # Edit auth/credentials for ChromaDB
   admin:your_secure_password
   ```
3. **Configure SSL**: Update nginx.conf with SSL certificates
4. **Network Security**: Restrict external access in production
5. **Backup Strategy**: Implement regular automated backups

### Network Security
```bash
# Restrict external access (production)
POSTGRES_PORT=127.0.0.1:5432
REDIS_PORT=127.0.0.1:6379
CHROMA_PORT=127.0.0.1:8000
```

## 📊 Monitoring

### Service URLs (After Starting)

- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379` 
- **ChromaDB**: `http://localhost:8000`
- **MinIO Console**: `http://localhost:9001` (Login: ai_admin/ai_minio_password)
- **RabbitMQ Management**: `http://localhost:15672` (Login: guest/guest)
- **Health Check**: `http://localhost/health`

### Health Checks

All services include automated health checks:
- **PostgreSQL**: `pg_isready` command
- **Redis**: `ping` command  
- **ChromaDB**: HTTP heartbeat endpoint
- **MinIO**: Health endpoint
- **RabbitMQ**: `rabbitmq-diagnostics ping`
- **Nginx**: Health endpoint

### Resource Monitoring

```bash
# View resource usage
make status

# Monitor specific service
docker stats ai-postgres
```

## 🔧 Troubleshooting

### Common Issues

**Services not starting?**
```bash
make health
make logs
```

**MinIO login failed?**
```bash
make reset-minio
```

**Database connection issues?**
```bash
make logs-postgres
# Check if PostgreSQL is ready
make shell-db
```

**Out of memory?**
```bash
# Check resource usage
make status
# Adjust memory limits in docker-compose.yml
```

### Port Conflicts

If default ports are in use, update `.env`:
```bash
POSTGRES_PORT=5433
REDIS_PORT=6380  
CHROMA_PORT=8001
MINIO_API_PORT=9002
MINIO_CONSOLE_PORT=9003
RABBITMQ_AMQP_PORT=5673
RABBITMQ_MANAGEMENT_PORT=15673
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

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guides.

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)**: Get running in 2 minutes
- **[Connection Guide](CONNECT_README.md)**: Service connection examples
- **[Deployment Guide](DEPLOYMENT.md)**: Production deployment scenarios
- **[Contributing Guide](CONTRIBUTING.md)**: Development and contribution guidelines
- **[Changelog](CHANGELOG.md)**: Version history and updates

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/your-org/ai-backend-stack.git
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
- [RabbitMQ](https://rabbitmq.com) - Open source multi-protocol messaging broker

---

**Made with ❤️ for the AI community**