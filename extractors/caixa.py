"""Functions to extract transactions from Caixa statements."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd
import pdfplumber

from utils.file_utils import normalize_text


@dataclass
class Transaction:
    date: str
    description: str
    amount: float
    installments: str
    card: str
    type: str


_DATE_RE = re.compile(r"^(\d{2}/\d{2})")
_AMOUNT_RE = re.compile(r"([\d,.]+)$")


def parse_pdf(path: Path) -> pd.DataFrame:
    """Parse Caixa PDF and return a DataFrame of transactions."""
    rows: List[Transaction] = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text = normalize_text(page.extract_text() or "")
            lines = text.split('\n')
            for line in lines:
                if not _DATE_RE.match(line):
                    continue
                parts = line.split()
                date = parts[0]
                amount_match = _AMOUNT_RE.search(line)
                if not amount_match:
                    continue
                amount_str = amount_match.group(1).replace('.', '').replace(',', '.')
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue
                description = ' '.join(parts[1:-1])
                transaction = Transaction(
                    date=date,
                    description=description,
                    amount=amount,
                    installments="",
                    card="Caixa",
                    type="debit",
                )
                rows.append(transaction)

    df = pd.DataFrame([t.__dict__ for t in rows])
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'], format='%d/%m')
        df.sort_values('date', inplace=True)
    return df



def matches(path: Path) -> bool:
    """Return True if the PDF appears to be a Caixa statement."""
    with pdfplumber.open(str(path)) as pdf:
        first_page = pdf.pages[0]
        text = normalize_text(first_page.extract_text() or "")
    return "CAIXA" in text.upper()
