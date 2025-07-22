# Quick Start Guide

Get your AI backend services running in under 2 minutes!

## Prerequisites

- Docker and Docker Compose installed
- 4GB+ RAM available
- Ports 5432, 6379, 8000, 9000, 9001, 80 available

## 1-2-3 Start

```bash
# 1. Setup
make setup

# 2. Start all services  
make up

# 3. Verify everything is working
make health
```

## What You Get

✅ **PostgreSQL** with vector extensions on port 5432  
✅ **Redis** cache on port 6379  
✅ **ChromaDB** vector database on port 8000  
✅ **MinIO** object storage on ports 9000/9001  
✅ **Nginx** reverse proxy on port 80  

## Test Your Services

```bash
# PostgreSQL
psql "postgresql://ai_user:ai_secure_password@localhost:5432/ai_app"

# Redis
redis-cli -h localhost -p 6379 -a ai_redis_password ping

# ChromaDB
curl http://localhost:8000/api/v1/heartbeat

# MinIO Console
open http://localhost:9001
# Login: ai_admin / ai_minio_password
```

## Connect from Your App

### Python
```python
import asyncpg
import redis
import chromadb
from minio import Minio

# PostgreSQL
pg = await asyncpg.connect("postgresql://ai_user:ai_secure_password@localhost:5432/ai_app")

# Redis  
redis_client = redis.Redis(host='localhost', port=6379, password='ai_redis_password')

# ChromaDB
chroma = chromadb.HttpClient(host="localhost", port=8000)

# MinIO
minio = Minio("localhost:9000", access_key="ai_admin", secret_key="ai_minio_password", secure=False)
```

### Node.js
```javascript
import { Client } from 'pg';
import Redis from 'redis';
import { ChromaApi } from 'chromadb';
import * as Minio from 'minio';

const pg = new Client({connectionString: 'postgresql://ai_user:ai_secure_password@localhost:5432/ai_app'});
const redis = Redis.createClient({url: 'redis://:ai_redis_password@localhost:6379'});
const chroma = new ChromaApi({path: "http://localhost:8000"});
const minio = new Minio.Client({endPoint: 'localhost', port: 9000, useSSL: false, accessKey: 'ai_admin', secretKey: 'ai_minio_password'});
```

## Useful Commands

```bash
make help           # Show all commands
make status         # Service status
make logs           # View logs
make shell-db       # PostgreSQL shell
make shell-redis    # Redis CLI
make down           # Stop services
```

## Next Steps

1. **Customize**: Edit `.env` with your preferred passwords
2. **Secure**: Enable authentication in `auth/credentials` 
3. **Scale**: Adjust resource limits in `docker-compose.yml`
4. **Deploy**: See `DEPLOYMENT.md` for production deployment

That's it! You now have a complete AI backend infrastructure running locally. 🚀