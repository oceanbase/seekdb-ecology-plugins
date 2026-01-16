#!/usr/bin/env python3
"""
Data utilities for importing files to seekdb.
"""

import pandas as pd
from pathlib import Path
from typing import Optional


def read_file(file_path: str) -> pd.DataFrame:
    """
    Read CSV or Excel file into DataFrame.
    
    Args:
        file_path: Path to CSV or Excel file
        
    Returns:
        pandas DataFrame
        
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file format is not supported
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    suffix = path.suffix.lower()
    
    if suffix == '.csv':
        return pd.read_csv(file_path)
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .xlsx")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean DataFrame for import to seekdb.
    
    Handles:
    - Converting numpy types to Python types
    - Filling NaN values
    
    Args:
        df: Input DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    
    for col in df.columns:
        # Convert numpy int64 to Python int
        if df[col].dtype == 'int64':
            df[col] = df[col].astype(object).where(df[col].notna(), None)
        # Convert numpy float64 to Python float
        elif df[col].dtype == 'float64':
            df[col] = df[col].astype(object).where(df[col].notna(), None)
    
    # Fill NaN with empty string for string columns
    df = df.fillna('')
    
    return df


def prepare_import_data(
    df: pd.DataFrame,
    vectorize_column: Optional[str] = None
) -> tuple:
    """
    Prepare data for import to seekdb.
    
    Args:
        df: Input DataFrame
        vectorize_column: Column to use for vectorization (optional)
        
    Returns:
        Tuple of (ids, documents, metadatas)
        - documents is None if vectorize_column is not specified
    """
    import uuid
    
    # Generate unique IDs
    ids = [str(uuid.uuid4()) for _ in range(len(df))]
    
    if vectorize_column:
        if vectorize_column not in df.columns:
            raise ValueError(
                f"Column '{vectorize_column}' not found. "
                f"Available columns: {df.columns.tolist()}"
            )
        
        # Extract documents for vectorization
        documents = df[vectorize_column].astype(str).tolist()
        
        # Remaining columns as metadata
        metadata_columns = [col for col in df.columns if col != vectorize_column]
        metadatas = df[metadata_columns].to_dict('records')
    else:
        documents = None
        metadatas = df.to_dict('records')
    
    return ids, documents, metadatas


def batch_generator(items: list, batch_size: int = 100):
    """
    Generate batches from a list.
    
    Args:
        items: List of items to batch
        batch_size: Size of each batch
        
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
