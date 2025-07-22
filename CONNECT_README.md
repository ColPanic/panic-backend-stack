# AI Backend Stack - Service Connection Guide

This document provides complete connection details for all services in the AI Backend Stack infrastructure. Use this guide to connect your applications to the pre-configured backend services.

## 🏗️ Available Services

| Service | Port | Purpose | Authentication |
|---------|------|---------|----------------|
| **PostgreSQL** | 5432 | Primary database with vector extensions | Username/Password |
| **Redis** | 6379 | Cache and session storage | Password |
| **ChromaDB** | 8000 | Vector database for embeddings | None (HTTP API) |
| **MinIO** | 9000/9001 | S3-compatible object storage | Access Key/Secret |
| **Nginx** | 80 | Reverse proxy and load balancer | None |

## 🔑 Default Credentials

### PostgreSQL Database
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `ai_app`
- **Username:** `ai_user`
- **Password:** `ai_secure_password`
- **Connection String:** `postgresql://ai_user:ai_secure_password@localhost:5432/ai_app`

### Redis Cache
- **Host:** `localhost`
- **Port:** `6379`
- **Password:** `ai_redis_password`
- **Connection String:** `redis://:ai_redis_password@localhost:6379`

### ChromaDB Vector Database
- **Host:** `localhost`
- **Port:** `8000`
- **Base URL:** `http://localhost:8000`
- **API Endpoint:** `http://localhost:8000/api/v1`
- **Authentication:** None required

### MinIO Object Storage
- **S3 Endpoint:** `localhost:9000`
- **Console:** `http://localhost:9001`
- **Access Key:** `ai_admin`
- **Secret Key:** `ai_minio_password`
- **SSL:** Disabled (local development)

## 🐍 Python Connection Examples

### PostgreSQL with asyncpg
```python
import asyncpg

async def connect_postgres():
    conn = await asyncpg.connect(
        "postgresql://ai_user:ai_secure_password@localhost:5432/ai_app"
    )
    return conn

# Usage
conn = await connect_postgres()
result = await conn.fetch("SELECT version();")
await conn.close()
```

### PostgreSQL with psycopg2
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="ai_app",
    user="ai_user",
    password="ai_secure_password"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
conn.close()
```

### Redis
```python
import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    password='ai_redis_password',
    decode_responses=True
)

# Test connection
redis_client.ping()
redis_client.set('test_key', 'test_value')
print(redis_client.get('test_key'))
```

### ChromaDB
```python
import chromadb

# HTTP Client
chroma_client = chromadb.HttpClient(
    host="localhost",
    port=8000
)

# Create/get collection
collection = chroma_client.get_or_create_collection("my_collection")

# Add documents
collection.add(
    documents=["This is a document"],
    ids=["doc1"]
)

# Query
results = collection.query(
    query_texts=["search query"],
    n_results=10
)
```

### MinIO
```python
from minio import Minio

minio_client = Minio(
    "localhost:9000",
    access_key="ai_admin",
    secret_key="ai_minio_password",
    secure=False  # HTTP for local development
)

# List buckets
buckets = minio_client.list_buckets()

# Upload file
minio_client.fput_object(
    "my-bucket",
    "my-object",
    "local-file.txt"
)
```

## 🟢 Node.js Connection Examples

### PostgreSQL with pg
```javascript
import { Client } from 'pg';

const client = new Client({
    host: 'localhost',
    port: 5432,
    database: 'ai_app',
    user: 'ai_user',
    password: 'ai_secure_password'
});

await client.connect();
const result = await client.query('SELECT version();');
console.log(result.rows);
await client.end();
```

### Redis with redis
```javascript
import Redis from 'redis';

const redis = Redis.createClient({
    url: 'redis://:ai_redis_password@localhost:6379'
});

await redis.connect();
await redis.ping();
await redis.set('test_key', 'test_value');
const value = await redis.get('test_key');
console.log(value);
```

### ChromaDB
```javascript
import { ChromaApi } from 'chromadb';

const chroma = new ChromaApi({
    path: "http://localhost:8000"
});

const collection = await chroma.getOrCreateCollection({
    name: "my_collection"
});

await collection.add({
    documents: ["This is a document"],
    ids: ["doc1"]
});
```

### MinIO
```javascript
import * as Minio from 'minio';

const minioClient = new Minio.Client({
    endPoint: 'localhost',
    port: 9000,
    useSSL: false,
    accessKey: 'ai_admin',
    secretKey: 'ai_minio_password'
});

// List buckets
const buckets = await minioClient.listBuckets();
console.log(buckets);
```

## 🦀 Rust Connection Examples

### PostgreSQL with tokio-postgres
```rust
use tokio_postgres::{NoTls, Error};

#[tokio::main]
async fn main() -> Result<(), Error> {
    let (client, connection) = tokio_postgres::connect(
        "postgresql://ai_user:ai_secure_password@localhost:5432/ai_app",
        NoTls,
    ).await?;

    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("Connection error: {}", e);
        }
    });

    let rows = client.query("SELECT version()", &[]).await?;
    for row in rows {
        let version: &str = row.get(0);
        println!("Version: {}", version);
    }

    Ok(())
}
```

### Redis with redis-rs
```rust
use redis::Commands;

fn main() -> redis::RedisResult<()> {
    let client = redis::Client::open("redis://:ai_redis_password@localhost:6379/")?;
    let mut con = client.get_connection()?;

    con.set("test_key", "test_value")?;
    let value: String = con.get("test_key")?;
    println!("Value: {}", value);

    Ok(())
}
```

## 🔧 Configuration Details

### PostgreSQL Extensions
The PostgreSQL instance includes these extensions:
- `vector` - for vector similarity search
- `uuid-ossp` - for UUID generation
- `pg_trgm` - for text similarity search
- Standard extensions (hstore, ltree, etc.)

### Redis Configuration
- Persistence enabled (RDB + AOF)
- Memory policy: `allkeys-lru`
- Max memory: 256MB (configurable)

### ChromaDB Features
- HTTP API enabled
- Persistent storage
- Collection management
- Vector similarity search
- Metadata filtering

### MinIO Buckets
Default buckets created:
- `documents` - for document storage
- `images` - for image assets
- `models` - for ML model files
- `backups` - for backup files

## 🔍 Health Check Endpoints

Verify services are running:

```bash
# PostgreSQL
psql "postgresql://ai_user:ai_secure_password@localhost:5432/ai_app" -c "SELECT 1;"

# Redis
redis-cli -h localhost -p 6379 -a ai_redis_password ping

# ChromaDB
curl http://localhost:8000/api/v1/heartbeat

# MinIO
curl http://localhost:9000/minio/health/live
```

## 🌐 Environment Variables

For easy configuration in your applications:

```bash
# Database
DATABASE_URL=postgresql://ai_user:ai_secure_password@localhost:5432/ai_app
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_app
DB_USER=ai_user
DB_PASSWORD=ai_secure_password

# Redis
REDIS_URL=redis://:ai_redis_password@localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=ai_redis_password

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_URL=http://localhost:8000

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=ai_admin
MINIO_SECRET_KEY=ai_minio_password
MINIO_SECURE=false
```

## 🔒 Security Notes

**⚠️ IMPORTANT:** These are default development credentials. For production:

1. **Change all passwords** before deployment
2. **Enable SSL/TLS** for all services
3. **Use environment variables** for credentials
4. **Implement proper authentication** for ChromaDB
5. **Configure firewall rules** to restrict access
6. **Enable Redis AUTH** and SSL
7. **Use IAM roles** for MinIO in cloud deployments

## 🚀 Quick Test Scripts

### Test All Services (Python)
```python
import asyncio
import asyncpg
import redis
import chromadb
from minio import Minio
import requests

async def test_all_services():
    # Test PostgreSQL
    try:
        conn = await asyncpg.connect("postgresql://ai_user:ai_secure_password@localhost:5432/ai_app")
        await conn.execute("SELECT 1")
        await conn.close()
        print("✅ PostgreSQL: Connected")
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")

    # Test Redis
    try:
        r = redis.Redis(host='localhost', port=6379, password='ai_redis_password')
        r.ping()
        print("✅ Redis: Connected")
    except Exception as e:
        print(f"❌ Redis: {e}")

    # Test ChromaDB
    try:
        response = requests.get("http://localhost:8000/api/v1/heartbeat")
        if response.status_code == 200:
            print("✅ ChromaDB: Connected")
        else:
            print(f"❌ ChromaDB: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ ChromaDB: {e}")

    # Test MinIO
    try:
        minio = Minio("localhost:9000", access_key="ai_admin", secret_key="ai_minio_password", secure=False)
        minio.list_buckets()
        print("✅ MinIO: Connected")
    except Exception as e:
        print(f"❌ MinIO: {e}")

if __name__ == "__main__":
    asyncio.run(test_all_services())
```

## 📚 Additional Resources

- **PostgreSQL Vector Extension:** [pgvector documentation](https://github.com/pgvector/pgvector)
- **ChromaDB Documentation:** [ChromaDB docs](https://docs.trychroma.com/)
- **MinIO SDK Documentation:** [MinIO client SDKs](https://min.io/docs/minio/linux/developers/minio-drivers.html)
- **Redis Documentation:** [Redis commands](https://redis.io/commands/)

## 🆘 Troubleshooting

### Common Issues

1. **Connection Refused:** Check if services are running
2. **Authentication Failed:** Verify credentials match defaults
3. **Port Conflicts:** Ensure ports 5432, 6379, 8000, 9000, 9001, 80 are available
4. **Memory Issues:** Ensure at least 4GB RAM available

### Service Status Commands
```bash
# Check if ports are open
netstat -tlnp | grep -E ':(5432|6379|8000|9000|9001|80)\s'

# Check service logs
docker logs ai-backend-postgres
docker logs ai-backend-redis
docker logs ai-backend-chromadb
docker logs ai-backend-minio
```

---

**Need help?** Check service logs or verify the infrastructure is running correctly. 