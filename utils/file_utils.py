"""Utility functions for file operations."""
from pathlib import Path
import pandas as pd


def save_to_csv(transactions: pd.DataFrame, pdf_path: Path) -> Path:
    """Save transactions DataFrame to CSV next to the PDF file."""
    csv_path = pdf_path.with_suffix('.csv')
    transactions.to_csv(csv_path, index=False)
    return csv_path


def normalize_text(text: str) -> str:
    """Normalize text by stripping extra spaces and newlines."""
    return ' '.join(text.split())
