# ChromaDB Statistics & Analysis Tool

A comprehensive Python script that analyzes ChromaDB vector databases to provide detailed insights about collections, vectors, documents, metadata, and overall health metrics.

## 🚀 Features

- **Health Monitoring**: Check ChromaDB service health and response times
- **Collection Analysis**: Detailed statistics for each collection
- **Vector Analysis**: Embedding dimensions, statistics, and sample data
- **Document Analysis**: Text content statistics and samples
- **Metadata Analysis**: Metadata key frequency and value distribution
- **Search Testing**: Test similarity search and metadata filtering functionality
- **Export Options**: Save detailed reports in JSON format
- **Connection Testing**: Verify ChromaDB connectivity and API endpoints

## 📋 Requirements

Install the required dependencies:

```bash
pip install -r requirements_chromadb_stats.txt
```

Dependencies:
- `chromadb>=0.4.0` - ChromaDB client library
- `numpy>=1.20.0` - Numerical analysis of embeddings
- `requests>=2.25.0` - HTTP health checks

## 🔧 Usage

### Basic Usage

Analyze ChromaDB with default settings (localhost:8000):

```bash
python chromadb_stats.py
```

### Custom Host/Port

Connect to a different ChromaDB instance:

```bash
python chromadb_stats.py --host 192.168.1.100 --port 8000
```

### Export to JSON

Save detailed analysis to a JSON file:

```bash
python chromadb_stats.py --output chromadb_analysis.json
```

### Quiet Mode

Run without detailed console output:

```bash
python chromadb_stats.py --quiet --output report.json
```

### Command Line Options

```
usage: chromadb_stats.py [-h] [--host HOST] [--port PORT] [--output OUTPUT] [--quiet]

ChromaDB Statistics and Analysis Tool

options:
  -h, --help       show this help message and exit
  --host HOST      ChromaDB host (default: localhost)
  --port PORT      ChromaDB port (default: 8000)
  --output OUTPUT  Output JSON file path (optional)
  --quiet          Suppress detailed output
```

## 📊 Sample Output

### Console Report

```
================================================================================
🗄️  CHROMADB ANALYSIS REPORT
================================================================================

📡 CONNECTION: ✅ CONNECTED
   🌐 URL: http://localhost:8000

💓 HEALTH: ✅ Heartbeat OK
   ⏱️  Response time: 15.23ms
   📋 Version: {'version': '0.4.15'}

📊 OVERVIEW:
   📚 Total Collections: 3
   📄 Total Documents: 1,247
   🔢 Total Vectors: 1,247

📂 COLLECTIONS:
   📁 company_profiles: 856 documents 🔍🏷️
      🎯 Vector dimensions: 1536
      🏷️  Metadata keys: company_id, industry, size
   📁 portfolio_research: 234 documents 🔍🏷️
      🎯 Vector dimensions: 1536
      🏷️  Metadata keys: fund_id, investment_stage, sector
   📁 user_documents: 157 documents 🔍
      🎯 Vector dimensions: 384

🔬 DETAILED ANALYSIS:

📁 Collection: company_profiles
   📊 Documents: 856
   📝 Avg document length: 1,247.3 chars
   🎯 Vector stats: μ=0.003, σ=0.124
   🔍 Similarity search: ✅
   🏷️  Metadata filtering: ✅

📁 Collection: portfolio_research
   📊 Documents: 234
   📝 Avg document length: 2,891.7 chars
   🎯 Vector stats: μ=-0.001, σ=0.098
   🔍 Similarity search: ✅
   🏷️  Metadata filtering: ✅

⏰ Analysis completed at: 2025-07-23T14:57:42.388134
================================================================================
```

### JSON Report Structure

The JSON report contains detailed metrics organized in these sections:

```json
{
  "timestamp": "2025-07-23T14:57:42.388134",
  "connection": {
    "status": "connected",
    "host": "localhost",
    "port": 8000,
    "url": "http://localhost:8000"
  },
  "health": {
    "heartbeat": {
      "status_code": 200,
      "response_time_ms": 15.23,
      "success": true
    },
    "version": {
      "version": "0.4.15"
    }
  },
  "overview": {
    "total_collections": 3,
    "collection_names": ["company_profiles", "portfolio_research", "user_documents"],
    "total_documents": 1247,
    "total_vectors": 1247,
    "collections_details": [...]
  },
  "collections": {
    "company_profiles": {
      "name": "company_profiles",
      "document_count": 856,
      "documents": {
        "total_analyzed": 856,
        "avg_document_length": 1247.3,
        "samples": ["Sample document text..."],
        "empty_documents": 0
      },
      "embeddings": {
        "total_vectors": 856,
        "vector_dimensions": 1536,
        "statistics": {
          "mean": 0.003,
          "std": 0.124,
          "min": -0.892,
          "max": 0.745
        },
        "sample_vector": [0.123, -0.456, 0.789, ...]
      },
      "metadata_analysis": {
        "total_with_metadata": 856,
        "common_keys": {"company_id": 856, "industry": 834, "size": 712},
        "metadata_summary": {...}
      },
      "search_tests": {
        "similarity_search": {"success": true, "results_count": 5},
        "metadata_filtering": {"success": true, "results_count": 23}
      }
    }
  }
}
```

## 📈 Metrics Provided

### Connection Metrics
- ✅ Connection status and URL
- ⏱️ Response times for health checks
- 🔄 API endpoint availability

### Collection Metrics
- 📊 Document counts per collection
- 📝 Average document lengths
- 🎯 Vector dimensions and statistics
- 🏷️ Metadata key frequencies and distributions
- 🔍 Search functionality testing

### Health Metrics
- 💓 Heartbeat endpoint status
- 📋 ChromaDB version information
- 🚀 Service availability

### Vector Analysis
- 📐 Embedding dimensions
- 📊 Statistical analysis (mean, std, min, max)
- 🎯 Sample vector data
- 🔢 Vector count validation

### Document Analysis
- 📄 Text content statistics
- 📝 Document length distributions
- 🔤 Sample document previews
- ❌ Empty document detection

### Metadata Analysis
- 🏷️ Metadata key frequency
- 🔧 Value type analysis
- 📊 Unique value counts
- 🎯 Sample metadata examples

## 🔍 Use Cases

### Development & Testing
- Verify ChromaDB is working correctly
- Validate vector embeddings are stored properly
- Test search functionality
- Monitor collection growth

### Production Monitoring
- Health check automation
- Performance monitoring
- Data quality validation
- Capacity planning

### Data Analysis
- Understand document distributions
- Analyze metadata patterns
- Validate embedding consistency
- Troubleshoot search issues

## 🛠️ Integration Examples

### Automated Health Checks

```bash
#!/bin/bash
# health_check.sh
python chromadb_stats.py --quiet --output /tmp/chromadb_health.json
if [ $? -eq 0 ]; then
    echo "✅ ChromaDB health check passed"
else
    echo "❌ ChromaDB health check failed"
    exit 1
fi
```

### Monitoring Script

```python
import subprocess
import json
import time

def monitor_chromadb():
    """Monitor ChromaDB and alert on issues."""
    try:
        result = subprocess.run([
            'python', 'chromadb_stats.py', 
            '--quiet', '--output', '/tmp/chromadb_report.json'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            with open('/tmp/chromadb_report.json') as f:
                report = json.load(f)
                
            total_docs = report['overview']['total_documents']
            print(f"ChromaDB healthy: {total_docs:,} documents")
            
        else:
            print("❌ ChromaDB connection failed")
            
    except Exception as e:
        print(f"Monitor error: {e}")

# Run every 5 minutes
while True:
    monitor_chromadb()
    time.sleep(300)
```

### CI/CD Integration

```yaml
# .github/workflows/chromadb-health.yml
name: ChromaDB Health Check
on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements_chromadb_stats.txt
      - name: Run ChromaDB health check
        run: python chromadb_stats.py --host ${{ secrets.CHROMADB_HOST }}
```

## 🔧 Troubleshooting

### Common Issues

**Connection Refused**
```bash
❌ Failed to connect to ChromaDB: Connection refused
```
- Ensure ChromaDB is running on the specified host/port
- Check firewall settings
- Verify the service is healthy

**Import Errors**
```bash
ImportError: cannot import name 'Collection'
```
- Update ChromaDB: `pip install --upgrade chromadb`
- Check Python version compatibility

**Embedding Dimension Mismatch**
```bash
Collection expecting embedding with dimension of 1536, got 384
```
- This indicates inconsistent embedding models
- Review your embedding generation pipeline
- Consider re-embedding documents with consistent models

**Empty Collections**
```bash
📁 Collection: my_collection: 0 documents
```
- Collection exists but contains no data
- Check your data ingestion pipeline
- Verify documents are being added correctly

### Performance Considerations

- **Large Collections**: Analysis is limited to 1,000 documents per collection to prevent memory issues
- **Network Latency**: Use `--host` and `--port` for remote ChromaDB instances
- **API Rate Limits**: The script includes reasonable delays between API calls

## 📋 Exit Codes

- `0`: Success - ChromaDB is healthy and analysis completed
- `1`: Failure - ChromaDB connection failed or critical error

## 🤝 Contributing

To extend this tool:

1. **Add new metrics**: Extend the `ChromaDBAnalyzer` class
2. **Custom output formats**: Add new export methods
3. **Additional health checks**: Extend the `check_health()` method
4. **Performance optimizations**: Improve large dataset handling

## 📚 Related Documentation

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [AI Backend Stack Connection Guide](./CONNECT_README.md)
- [Vector Database Best Practices](https://docs.trychroma.com/guides)

---

**Need help?** Check the ChromaDB logs or verify your connection settings using the examples in the [Connection Guide](./CONNECT_README.md). 