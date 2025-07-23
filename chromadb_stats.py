#!/usr/bin/env python3
"""
ChromaDB Statistics and Health Check Script

This script provides comprehensive insights into the ChromaDB vector database,
including collection statistics, vector analysis, and overall health metrics.
"""

import json
import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime
import chromadb
import requests
import numpy as np
from collections import Counter


class ChromaDBAnalyzer:
    """Comprehensive ChromaDB analysis and statistics generator."""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        """Initialize the ChromaDB analyzer.
        
        Args:
            host: ChromaDB host (default: localhost)
            port: ChromaDB port (default: 8000)
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.client = None
        self.stats = {
            "timestamp": datetime.now().isoformat(),
            "connection": {},
            "overview": {},
            "collections": {},
            "health": {}
        }
    
    def connect(self) -> bool:
        """Connect to ChromaDB and test the connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = chromadb.HttpClient(host=self.host, port=self.port)
            
            # Test basic connectivity
            self.client.heartbeat()
            
            self.stats["connection"] = {
                "status": "connected",
                "host": self.host,
                "port": self.port,
                "url": self.base_url
            }
            print(f"✅ Connected to ChromaDB at {self.base_url}")
            return True
            
        except Exception as e:
            self.stats["connection"] = {
                "status": "failed",
                "error": str(e),
                "host": self.host,
                "port": self.port
            }
            print(f"❌ Failed to connect to ChromaDB: {e}")
            return False
    
    def check_health(self) -> Dict[str, Any]:
        """Check ChromaDB health and API endpoints.
        
        Returns:
            Dict containing health check results
        """
        health_data = {}
        
        try:
            # Check heartbeat endpoint
            response = requests.get(f"{self.base_url}/api/v1/heartbeat", timeout=5)
            health_data["heartbeat"] = {
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "success": response.status_code == 200
            }
        except Exception as e:
            health_data["heartbeat"] = {
                "success": False,
                "error": str(e)
            }
        
        try:
            # Check version endpoint
            response = requests.get(f"{self.base_url}/api/v1/version", timeout=5)
            if response.status_code == 200:
                health_data["version"] = response.json()
            else:
                health_data["version"] = {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            health_data["version"] = {"error": str(e)}
        
        return health_data
    
    def get_collections_overview(self) -> Dict[str, Any]:
        """Get overview of all collections.
        
        Returns:
            Dict containing collections overview
        """
        try:
            collections = self.client.list_collections()
            
            overview = {
                "total_collections": len(collections),
                "collection_names": [col.name for col in collections],
                "collections_details": []
            }
            
            total_documents = 0
            total_vectors = 0
            
            for collection in collections:
                try:
                    count = collection.count()
                    total_documents += count
                    total_vectors += count  # In ChromaDB, each document typically has one vector
                    
                    overview["collections_details"].append({
                        "name": collection.name,
                        "id": collection.id,
                        "document_count": count,
                        "metadata": collection.metadata or {}
                    })
                except Exception as e:
                    overview["collections_details"].append({
                        "name": collection.name,
                        "error": str(e)
                    })
            
            overview["total_documents"] = total_documents
            overview["total_vectors"] = total_vectors
            
            return overview
            
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_collection(self, collection) -> Dict[str, Any]:
        """Analyze a specific collection in detail.
        
        Args:
            collection: ChromaDB collection object
            
        Returns:
            Dict containing detailed collection analysis
        """
        try:
            analysis = {
                "name": collection.name,
                "id": collection.id,
                "metadata": collection.metadata or {},
                "document_count": 0,
                "documents": {},
                "embeddings": {},
                "metadata_analysis": {}
            }
            
            # Get count
            count = collection.count()
            analysis["document_count"] = count
            
            if count == 0:
                analysis["status"] = "empty"
                return analysis
            
            # Get all documents (limit to reasonable number for analysis)
            limit = min(count, 1000)  # Analyze up to 1000 documents
            
            try:
                results = collection.get(limit=limit, include=["documents", "metadatas", "embeddings"])
                
                # Analyze documents
                if results.get("documents"):
                    documents = results["documents"]
                    analysis["documents"] = {
                        "total_analyzed": len(documents),
                        "sample_count": min(5, len(documents)),
                        "samples": documents[:5] if documents else [],
                        "document_lengths": [len(doc) if doc else 0 for doc in documents],
                        "avg_document_length": statistics.mean([len(doc) if doc else 0 for doc in documents]) if documents else 0,
                        "empty_documents": sum(1 for doc in documents if not doc)
                    }
                
                # Analyze embeddings
                if results.get("embeddings"):
                    embeddings = results["embeddings"]
                    if embeddings and len(embeddings) > 0:
                        # Convert to numpy array for analysis
                        embeddings_array = np.array(embeddings)
                        
                        analysis["embeddings"] = {
                            "total_vectors": len(embeddings),
                            "vector_dimensions": embeddings_array.shape[1] if len(embeddings_array.shape) > 1 else 0,
                            "statistics": {
                                "mean": float(np.mean(embeddings_array)) if embeddings_array.size > 0 else 0,
                                "std": float(np.std(embeddings_array)) if embeddings_array.size > 0 else 0,
                                "min": float(np.min(embeddings_array)) if embeddings_array.size > 0 else 0,
                                "max": float(np.max(embeddings_array)) if embeddings_array.size > 0 else 0
                            },
                            "sample_vector": embeddings[0][:10] if embeddings and embeddings[0] else []  # First 10 dimensions of first vector
                        }
                
                # Analyze metadata
                if results.get("metadatas"):
                    metadatas = [meta for meta in results["metadatas"] if meta]
                    if metadatas:
                        # Count metadata keys
                        all_keys = []
                        for meta in metadatas:
                            if isinstance(meta, dict):
                                all_keys.extend(meta.keys())
                        
                        key_counts = Counter(all_keys)
                        
                        # Analyze metadata values
                        metadata_summary = {}
                        for key in key_counts.keys():
                            values = []
                            for meta in metadatas:
                                if isinstance(meta, dict) and key in meta:
                                    values.append(meta[key])
                            
                            value_types = Counter([type(v).__name__ for v in values])
                            unique_values = len(set(str(v) for v in values))
                            
                            metadata_summary[key] = {
                                "frequency": key_counts[key],
                                "unique_values": unique_values,
                                "value_types": dict(value_types),
                                "sample_values": list(set(str(v) for v in values))[:5]
                            }
                        
                        analysis["metadata_analysis"] = {
                            "total_with_metadata": len(metadatas),
                            "common_keys": dict(key_counts.most_common(10)),
                            "metadata_summary": metadata_summary,
                            "sample_metadata": metadatas[:3]
                        }
                
            except Exception as e:
                analysis["data_retrieval_error"] = str(e)
            
            return analysis
            
        except Exception as e:
            return {
                "name": collection.name if hasattr(collection, 'name') else "unknown",
                "error": str(e)
            }
    
    def test_search_functionality(self, collection) -> Dict[str, Any]:
        """Test search functionality on a collection.
        
        Args:
            collection: ChromaDB collection object
            
        Returns:
            Dict containing search test results
        """
        try:
            count = collection.count()
            if count == 0:
                return {"status": "skipped", "reason": "empty collection"}
            
            # Try a simple query
            test_results = {}
            
            try:
                # Get a sample document to use for similarity search
                sample = collection.get(limit=1, include=["documents"])
                if sample.get("documents") and sample["documents"][0]:
                    sample_text = sample["documents"][0][:100]  # First 100 chars
                    
                    # Perform similarity search
                    search_results = collection.query(
                        query_texts=[sample_text],
                        n_results=min(5, count)
                    )
                    
                    test_results["similarity_search"] = {
                        "success": True,
                        "query_text": sample_text,
                        "results_count": len(search_results.get("ids", [[]])[0]),
                        "has_distances": bool(search_results.get("distances"))
                    }
                else:
                    test_results["similarity_search"] = {
                        "success": False,
                        "reason": "no sample document available"
                    }
                    
            except Exception as e:
                test_results["similarity_search"] = {
                    "success": False,
                    "error": str(e)
                }
            
            # Test metadata filtering if metadata exists
            try:
                sample_with_meta = collection.get(limit=1, include=["metadatas"])
                if sample_with_meta.get("metadatas") and sample_with_meta["metadatas"][0]:
                    metadata = sample_with_meta["metadatas"][0]
                    if isinstance(metadata, dict) and metadata:
                        # Try filtering by first metadata key
                        first_key = list(metadata.keys())[0]
                        first_value = metadata[first_key]
                        
                        filtered_results = collection.get(
                            where={first_key: first_value},
                            limit=5
                        )
                        
                        test_results["metadata_filtering"] = {
                            "success": True,
                            "filter_used": {first_key: first_value},
                            "results_count": len(filtered_results.get("ids", []))
                        }
                    else:
                        test_results["metadata_filtering"] = {
                            "success": False,
                            "reason": "no metadata available"
                        }
                else:
                    test_results["metadata_filtering"] = {
                        "success": False,
                        "reason": "no metadata found"
                    }
                    
            except Exception as e:
                test_results["metadata_filtering"] = {
                    "success": False,
                    "error": str(e)
                }
            
            return test_results
            
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive ChromaDB analysis report.
        
        Returns:
            Dict containing complete analysis report
        """
        print("🔍 Analyzing ChromaDB...")
        
        # Check connection
        if not self.connect():
            return self.stats
        
        # Check health
        print("📊 Checking health...")
        self.stats["health"] = self.check_health()
        
        # Get collections overview
        print("📋 Getting collections overview...")
        self.stats["overview"] = self.get_collections_overview()
        
        # Analyze each collection in detail
        if self.stats["overview"].get("total_collections", 0) > 0:
            print(f"🔬 Analyzing {self.stats['overview']['total_collections']} collections...")
            
            collections = self.client.list_collections()
            for i, collection in enumerate(collections, 1):
                print(f"  📂 Analyzing collection {i}/{len(collections)}: {collection.name}")
                
                collection_analysis = self.analyze_collection(collection)
                
                # Test search functionality
                search_tests = self.test_search_functionality(collection)
                collection_analysis["search_tests"] = search_tests
                
                self.stats["collections"][collection.name] = collection_analysis
        
        return self.stats
    
    def print_summary(self):
        """Print a formatted summary of the analysis."""
        stats = self.stats
        
        print("\n" + "="*80)
        print("🗄️  CHROMADB ANALYSIS REPORT")
        print("="*80)
        
        # Connection status
        conn = stats.get("connection", {})
        status_icon = "✅" if conn.get("status") == "connected" else "❌"
        print(f"\n📡 CONNECTION: {status_icon} {conn.get('status', 'unknown').upper()}")
        if conn.get("status") == "connected":
            print(f"   🌐 URL: {conn.get('url')}")
        elif conn.get("error"):
            print(f"   ❌ Error: {conn.get('error')}")
        
        # Health status
        health = stats.get("health", {})
        if health.get("heartbeat"):
            hb = health["heartbeat"]
            hb_icon = "✅" if hb.get("success") else "❌"
            print(f"\n💓 HEALTH: {hb_icon} Heartbeat {'OK' if hb.get('success') else 'FAILED'}")
            if hb.get("response_time_ms"):
                print(f"   ⏱️  Response time: {hb['response_time_ms']:.2f}ms")
        
        if health.get("version"):
            version = health["version"]
            if not version.get("error"):
                print(f"   📋 Version: {version}")
        
        # Overview
        overview = stats.get("overview", {})
        print(f"\n📊 OVERVIEW:")
        print(f"   📚 Total Collections: {overview.get('total_collections', 0)}")
        print(f"   📄 Total Documents: {overview.get('total_documents', 0):,}")
        print(f"   🔢 Total Vectors: {overview.get('total_vectors', 0):,}")
        
        # Collections details
        if overview.get("collection_names"):
            print(f"\n📂 COLLECTIONS:")
            for name in overview["collection_names"]:
                collection_stats = stats.get("collections", {}).get(name, {})
                doc_count = collection_stats.get("document_count", 0)
                
                search_status = ""
                search_tests = collection_stats.get("search_tests", {})
                if search_tests.get("similarity_search", {}).get("success"):
                    search_status += "🔍"
                if search_tests.get("metadata_filtering", {}).get("success"):
                    search_status += "🏷️"
                
                print(f"   📁 {name}: {doc_count:,} documents {search_status}")
                
                # Show embedding info if available
                embeddings = collection_stats.get("embeddings", {})
                if embeddings.get("vector_dimensions"):
                    dims = embeddings["vector_dimensions"]
                    print(f"      🎯 Vector dimensions: {dims}")
                
                # Show metadata info if available
                meta_analysis = collection_stats.get("metadata_analysis", {})
                if meta_analysis.get("common_keys"):
                    keys = list(meta_analysis["common_keys"].keys())[:3]
                    print(f"      🏷️  Metadata keys: {', '.join(keys)}")
        
        # Detailed collection analysis
        collections_data = stats.get("collections", {})
        if collections_data:
            print(f"\n🔬 DETAILED ANALYSIS:")
            for name, data in collections_data.items():
                print(f"\n📁 Collection: {name}")
                print(f"   📊 Documents: {data.get('document_count', 0):,}")
                
                # Document analysis
                docs = data.get("documents", {})
                if docs.get("avg_document_length"):
                    print(f"   📝 Avg document length: {docs['avg_document_length']:.1f} chars")
                
                # Embedding analysis
                embeddings = data.get("embeddings", {})
                if embeddings.get("statistics"):
                    stats_data = embeddings["statistics"]
                    print(f"   🎯 Vector stats: μ={stats_data.get('mean', 0):.3f}, σ={stats_data.get('std', 0):.3f}")
                
                # Search functionality
                search_tests = data.get("search_tests", {})
                if search_tests:
                    sim_search = search_tests.get("similarity_search", {})
                    meta_filter = search_tests.get("metadata_filtering", {})
                    
                    sim_status = "✅" if sim_search.get("success") else "❌"
                    meta_status = "✅" if meta_filter.get("success") else "❌"
                    
                    print(f"   🔍 Similarity search: {sim_status}")
                    print(f"   🏷️  Metadata filtering: {meta_status}")
        
        print(f"\n⏰ Analysis completed at: {stats.get('timestamp')}")
        print("="*80)


def main():
    """Main function to run ChromaDB analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ChromaDB Statistics and Analysis Tool")
    parser.add_argument("--host", default="localhost", help="ChromaDB host (default: localhost)")
    parser.add_argument("--port", type=int, default=8000, help="ChromaDB port (default: 8000)")
    parser.add_argument("--output", help="Output JSON file path (optional)")
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed output")
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = ChromaDBAnalyzer(host=args.host, port=args.port)
    
    # Generate report
    report = analyzer.generate_report()
    
    # Print summary unless quiet mode
    if not args.quiet:
        analyzer.print_summary()
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n💾 Report saved to: {args.output}")
    
    # Exit with appropriate code
    if report.get("connection", {}).get("status") != "connected":
        exit(1)


if __name__ == "__main__":
    main() 