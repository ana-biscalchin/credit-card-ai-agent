"""Functions to extract transactions from Nubank statements."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd
import fitz  # PyMuPDF
import logging

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
    """Parse Nubank PDF and return a DataFrame of transactions."""
    rows: List[Transaction] = []
    doc = fitz.open(str(path))
    in_section = False
    for page in doc:
        raw = page.get_text()
        logging.debug("Pagina %d texto bruto: %s", page.number + 1, raw)
        for line in raw.splitlines():
            clean = normalize_text(line)
            if "TRANSAÇÕES DE" in clean.upper():
                in_section = True
                continue
            if "PAGAMENTOS" in clean.upper():
                in_section = False
            if not in_section:
                continue
            if not _DATE_RE.match(clean):
                continue
            parts = clean.split()
            date = parts[0]
            amount_match = _AMOUNT_RE.search(clean)
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
                card="Nubank",
                type="debit",
            )
            rows.append(transaction)
    doc.close()

    df = pd.DataFrame([t.__dict__ for t in rows])
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'], format='%d/%m')
        df.sort_values('date', inplace=True)
    return df



def matches(path: Path) -> bool:
    """Return True if the PDF appears to be a Nubank statement."""
    doc = fitz.open(str(path))
    first_page = doc.load_page(0)
    text = normalize_text(first_page.get_text() or "")
    doc.close()
    return "NUBANK" in text.upper()
