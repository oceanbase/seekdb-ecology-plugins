#!/usr/bin/env python3
"""
Query data from seekdb vector database and optionally export to CSV/Excel.

Usage:
    python query_in_seekdb.py <collection_name> --query-text <text> [--n-results <n>]
    python query_in_seekdb.py <collection_name> --get-all [--limit <n>]
    python query_in_seekdb.py <collection_name> --get-ids <id1,id2,...>
    python query_in_seekdb.py <collection_name> --query-text <text> --output results.csv

Examples:
    # Semantic search with text query
    python query_in_seekdb.py mobiles --query-text "phone with good battery"
    
    # Get all records from collection
    python query_in_seekdb.py mobiles --get-all --limit 10
    
    # Get specific records by IDs
    python query_in_seekdb.py mobiles --get-ids "id1,id2,id3"
    
    # Search with metadata filter
    python query_in_seekdb.py mobiles --query-text "budget phone" --where '{"Brand": {"$eq": "SAMSUNG"}}'
    
    # Hybrid search (full-text + vector)
    python query_in_seekdb.py mobiles --hybrid --query-text "gaming phone" --contains "64 GB"
    
    # Export query results to CSV
    python query_in_seekdb.py mobiles --query-text "phone with good battery" --output results.csv
    
    # Export all records to Excel
    python query_in_seekdb.py mobiles --get-all --limit 1000 --output mobiles.xlsx
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional, will use environment variables directly

try:
    import pyseekdb
except ImportError:
    print("Error: pyseekdb is required. Install with: pip install pyseekdb")
    sys.exit(1)

# pandas is optional, only required for export
pandas_available = False
try:
    import pandas as pd
    pandas_available = True
except ImportError:
    pass


# Initialize client based on environment
host = os.getenv("SEEKDB_HOST")
if host:
    # Server mode
    client = pyseekdb.Client(
        host=host,
        port=int(os.getenv("SEEKDB_PORT", "2881")),
        database=os.getenv("SEEKDB_DATABASE", "test"),
        user=os.getenv("SEEKDB_USER", "root"),
        password=os.getenv("SEEKDB_PASSWORD", "")
    )
else:
    # Embedded mode
    client = pyseekdb.Client()


def get_collection(collection_name: str):
    """Get a collection from seekdb."""
    if not client.has_collection(collection_name):
        raise ValueError(f"Collection '{collection_name}' not found. Available collections: {client.list_collections()}")
    return client.get_collection(name=collection_name)


def query_by_text(
    collection_name: str,
    query_text: str,
    n_results: int = 5,
    where: Optional[dict] = None,
    where_document: Optional[dict] = None,
    include: Optional[list] = None
) -> dict:
    """
    Perform semantic similarity search using text query.
    
    Args:
        collection_name: Name of the collection to query
        query_text: Text to search for (will be embedded automatically)
        n_results: Number of results to return
        where: Metadata filter conditions
        where_document: Document filter conditions
        include: List of fields to include in results
    
    Returns:
        Query results dictionary with ids, documents, metadatas, distances
    """
    collection = get_collection(collection_name)
    
    query_params = {
        "query_texts": query_text,
        "n_results": n_results
    }
    
    if where:
        query_params["where"] = where
    if where_document:
        query_params["where_document"] = where_document
    if include:
        query_params["include"] = include
    else:
        query_params["include"] = ["documents", "metadatas"]
    
    return collection.query(**query_params)


def get_by_ids(
    collection_name: str,
    ids: list,
    include: Optional[list] = None
) -> dict:
    """
    Retrieve specific records by their IDs.
    
    Args:
        collection_name: Name of the collection
        ids: List of IDs to retrieve
        include: List of fields to include
    
    Returns:
        Get results dictionary
    """
    collection = get_collection(collection_name)
    
    get_params: dict = {"ids": ids}
    if include:
        get_params["include"] = include
    else:
        get_params["include"] = ["documents", "metadatas"]
    
    return collection.get(**get_params)


def get_all(
    collection_name: str,
    limit: int = 10,
    offset: int = 0,
    where: Optional[dict] = None,
    include: Optional[list] = None
) -> dict:
    """
    Retrieve all records from collection with optional filtering.
    
    Args:
        collection_name: Name of the collection
        limit: Maximum number of records to return
        offset: Number of records to skip (for pagination)
        where: Metadata filter conditions
        include: List of fields to include
    
    Returns:
        Get results dictionary
    """
    collection = get_collection(collection_name)
    
    get_params: dict = {
        "limit": limit,
        "offset": offset
    }
    
    if where:
        get_params["where"] = where
    if include:
        get_params["include"] = include
    else:
        get_params["include"] = ["documents", "metadatas"]
    
    return collection.get(**get_params)


def hybrid_search(
    collection_name: str,
    query_text: str,
    contains: Optional[str] = None,
    n_results: int = 5,
    where: Optional[dict] = None,
    include: Optional[list] = None
) -> dict:
    """
    Perform hybrid search combining full-text and vector similarity search.
    
    Args:
        collection_name: Name of the collection
        query_text: Text to search for (will be embedded for vector search)
        contains: Text substring for full-text search
        n_results: Number of results to return
        where: Metadata filter conditions
        include: List of fields to include
    
    Returns:
        Hybrid search results dictionary
    """
    collection = get_collection(collection_name)
    
    # Build query (full-text search) configuration
    query_config: dict = {"n_results": n_results * 2}  # Get more for ranking
    if contains:
        query_config["where_document"] = {"$contains": contains}
    if where:
        query_config["where"] = where
    
    # Build knn (vector search) configuration
    knn_config = {
        "query_texts": [query_text],
        "n_results": n_results * 2
    }
    if where:
        knn_config["where"] = where
    
    search_params = {
        "query": query_config,
        "knn": knn_config,
        "rank": {"rrf": {}},  # Reciprocal Rank Fusion
        "n_results": n_results
    }
    
    if include:
        search_params["include"] = include
    else:
        search_params["include"] = ["documents", "metadatas"]
    
    return collection.hybrid_search(**search_params)


def results_to_dataframe(results: dict, result_type: str = "query") -> "pd.DataFrame":
    """
    Convert query/get results to pandas DataFrame.
    
    Args:
        results: Query or get results dictionary
        result_type: "query" for query/hybrid_search results (nested lists),
                    "get" for get results (flat lists)
    
    Returns:
        DataFrame with all data flattened
    """
    if not pandas_available:
        raise ImportError("pandas is required for export. Install with: pip install pandas openpyxl")
    
    import pandas as pd  # Import here since we've confirmed it's available
    
    rows = []
    
    if result_type == "query":
        # Query results have nested lists
        if not results.get("ids") or not results["ids"][0]:
            return pd.DataFrame()
        
        ids = results["ids"][0]
        distances = results.get("distances", [[]])[0]
        documents = results.get("documents", [[]])[0] if results.get("documents") else []
        metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
        
        for i, id_ in enumerate(ids):
            row = {"id": id_}
            
            if distances and i < len(distances):
                row["distance"] = distances[i]
            
            if documents and i < len(documents) and documents[i]:
                row["document"] = documents[i]
            
            if metadatas and i < len(metadatas) and metadatas[i]:
                for key, value in metadatas[i].items():
                    row[key] = value
            
            rows.append(row)
    else:
        # Get results have flat lists
        if not results.get("ids"):
            return pd.DataFrame()
        
        ids = results["ids"]
        documents = results.get("documents", []) if results.get("documents") else []
        metadatas = results.get("metadatas", []) if results.get("metadatas") else []
        
        for i, id_ in enumerate(ids):
            row = {"id": id_}
            
            if documents and i < len(documents) and documents[i]:
                row["document"] = documents[i]
            
            if metadatas and i < len(metadatas) and metadatas[i]:
                for key, value in metadatas[i].items():
                    row[key] = value
            
            rows.append(row)
    
    return pd.DataFrame(rows)


def export_to_file(df, output_path: str, sheet_name: str = "Data") -> str:
    """
    Export DataFrame to CSV or Excel file.
    
    Args:
        df: DataFrame to export
        output_path: Output file path (.csv or .xlsx)
        sheet_name: Sheet name for Excel export
    
    Returns:
        Absolute path to the exported file
    """
    if not pandas_available:
        raise ImportError("pandas is required for export. Install with: pip install pandas openpyxl")
    
    path = Path(output_path)
    suffix = path.suffix.lower()
    
    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if suffix == '.csv':
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
    elif suffix in ['.xlsx', '.xls']:
        df.to_excel(output_path, index=False, sheet_name=sheet_name, engine='openpyxl')
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .xlsx")
    
    return str(path.absolute())


def print_results(results: dict, result_type: str = "query"):
    """Pretty print query results."""
    if result_type == "query":
        # Query results have nested lists
        if not results.get("ids") or not results["ids"][0]:
            print("No results found.")
            return
        
        ids = results["ids"][0]
        distances = results.get("distances", [[]])[0]
        documents = results.get("documents", [[]])[0] if results.get("documents") else []
        metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
        
        print(f"\nFound {len(ids)} results:\n")
        print("=" * 80)
        
        for i, id_ in enumerate(ids):
            print(f"\n[Result {i + 1}]")
            print(f"  ID: {id_}")
            if distances and i < len(distances):
                print(f"  Distance: {distances[i]:.4f}")
            if documents and i < len(documents) and documents[i]:
                doc = documents[i]
                if len(doc) > 200:
                    doc = doc[:200] + "..."
                print(f"  Document: {doc}")
            if metadatas and i < len(metadatas) and metadatas[i]:
                print(f"  Metadata:")
                for key, value in metadatas[i].items():
                    val_str = str(value)
                    if len(val_str) > 100:
                        val_str = val_str[:100] + "..."
                    print(f"    - {key}: {val_str}")
    else:
        # Get results have flat lists
        if not results.get("ids"):
            print("No results found.")
            return
        
        ids = results["ids"]
        documents = results.get("documents", []) if results.get("documents") else []
        metadatas = results.get("metadatas", []) if results.get("metadatas") else []
        
        print(f"\nFound {len(ids)} records:\n")
        print("=" * 80)
        
        for i, id_ in enumerate(ids):
            print(f"\n[Record {i + 1}]")
            print(f"  ID: {id_}")
            if documents and i < len(documents) and documents[i]:
                doc = documents[i]
                if len(doc) > 200:
                    doc = doc[:200] + "..."
                print(f"  Document: {doc}")
            if metadatas and i < len(metadatas) and metadatas[i]:
                print(f"  Metadata:")
                for key, value in metadatas[i].items():
                    val_str = str(value)
                    if len(val_str) > 100:
                        val_str = val_str[:100] + "..."
                    print(f"    - {key}: {val_str}")


def list_collections():
    """List all available collections."""
    collections = client.list_collections()
    if not collections:
        print("No collections found.")
        return
    
    print("\nAvailable collections:")
    for col in collections:
        if hasattr(col, 'name'):
            print(f"  - {col.name}")
        else:
            print(f"  - {col}")


def collection_info(collection_name: str):
    """Get information about a collection."""
    collection = get_collection(collection_name)
    count = collection.count()
    
    print(f"\nCollection: {collection_name}")
    print(f"  Total records: {count}")
    
    # Preview some data
    if count > 0:
        preview = collection.peek(limit=3)
        print(f"\nPreview (first 3 records):")
        for i in range(len(preview['ids'])):
            print(f"  ID: {preview['ids'][i][:20]}...")
            if preview.get('documents') and preview['documents'][i]:
                doc = preview['documents'][i][:50] + "..." if len(preview['documents'][i]) > 50 else preview['documents'][i]
                print(f"    Document: {doc}")
            if preview.get('metadatas') and preview['metadatas'][i]:
                print(f"    Metadata keys: {list(preview['metadatas'][i].keys())}")


def output_results(results: dict, result_type: str, output_path: Optional[str], 
                   as_json: bool, sheet_name: str = "Data"):
    """
    Output results to terminal, JSON, or file.
    
    Args:
        results: Query or get results dictionary
        result_type: "query" or "get"
        output_path: Optional file path for export (.csv or .xlsx)
        as_json: Output as JSON to terminal
        sheet_name: Sheet name for Excel export
    """
    if output_path:
        # Export to file
        df = results_to_dataframe(results, result_type=result_type)
        if df.empty:
            print("No results found to export.")
            return
        
        abs_path = export_to_file(df, output_path, sheet_name=sheet_name)
        print(f"Exported {len(df)} records to: {abs_path}")
    elif as_json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print_results(results, result_type=result_type)


def main():
    parser = argparse.ArgumentParser(
        description="Query data from seekdb vector database and optionally export to CSV/Excel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Positional argument (optional for --list-collections)
    parser.add_argument("collection_name", nargs="?", help="Name of the collection to query")
    
    # Query modes
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--query-text", "-q", 
                           help="Text query for semantic similarity search")
    mode_group.add_argument("--get-all", "-a", action="store_true",
                           help="Get all records from collection")
    mode_group.add_argument("--get-ids", "-i",
                           help="Comma-separated list of IDs to retrieve")
    mode_group.add_argument("--hybrid", action="store_true",
                           help="Perform hybrid search (requires --query-text)")
    mode_group.add_argument("--list-collections", "-l", action="store_true",
                           help="List all available collections")
    mode_group.add_argument("--info", action="store_true",
                           help="Show collection info and preview")
    
    # Common options
    parser.add_argument("--n-results", "-n", type=int, default=5,
                       help="Number of results to return (default: 5)")
    parser.add_argument("--limit", type=int, default=10,
                       help="Limit for get-all (default: 10)")
    parser.add_argument("--offset", type=int, default=0,
                       help="Offset for pagination (default: 0)")
    parser.add_argument("--where", "-w",
                       help="Metadata filter as JSON string, e.g., '{\"Brand\": {\"$eq\": \"SAMSUNG\"}}'")
    parser.add_argument("--contains", "-c",
                       help="Text substring for document filter or hybrid search")
    parser.add_argument("--include", 
                       help="Comma-separated fields to include: documents,metadatas,embeddings")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output results as JSON")
    
    # Export options
    parser.add_argument("--output", "-o",
                       help="Export results to file (.csv or .xlsx)")
    parser.add_argument("--sheet-name", "-s", default="Data",
                       help="Sheet name for Excel export (default: Data)")
    
    # Special case: hybrid requires query-text to be passed separately
    parser.add_argument("--hybrid-query",
                       help="Query text for hybrid search (use with --hybrid)")
    
    args = parser.parse_args()
    
    # Handle list-collections (no collection_name required)
    if args.list_collections:
        list_collections()
        return
    
    # All other modes require collection_name
    if not args.collection_name:
        parser.error("collection_name is required (except for --list-collections)")
    
    # Parse where filter
    where_filter = None
    if args.where:
        try:
            where_filter = json.loads(args.where)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in --where: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Parse include list
    include_list = None
    if args.include:
        include_list = [f.strip() for f in args.include.split(",")]
    
    # Handle hybrid search query text
    query_text = args.query_text or args.hybrid_query
    
    try:
        if args.info:
            collection_info(args.collection_name)
        
        elif args.get_all:
            results = get_all(
                collection_name=args.collection_name,
                limit=args.limit,
                offset=args.offset,
                where=where_filter,
                include=include_list
            )
            output_results(results, "get", args.output, args.json, args.sheet_name)
        
        elif args.get_ids:
            ids = [id_.strip() for id_ in args.get_ids.split(",")]
            results = get_by_ids(
                collection_name=args.collection_name,
                ids=ids,
                include=include_list
            )
            output_results(results, "get", args.output, args.json, args.sheet_name)
        
        elif args.hybrid:
            if not query_text:
                parser.error("--hybrid requires --query-text or --hybrid-query")
            results = hybrid_search(
                collection_name=args.collection_name,
                query_text=query_text,
                contains=args.contains,
                n_results=args.n_results,
                where=where_filter,
                include=include_list
            )
            output_results(results, "query", args.output, args.json, args.sheet_name)
        
        elif args.query_text:
            where_document = None
            if args.contains:
                where_document = {"$contains": args.contains}
            
            results = query_by_text(
                collection_name=args.collection_name,
                query_text=args.query_text,
                n_results=args.n_results,
                where=where_filter,
                where_document=where_document,
                include=include_list
            )
            output_results(results, "query", args.output, args.json, args.sheet_name)
        
        else:
            # Default: show collection info
            collection_info(args.collection_name)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
