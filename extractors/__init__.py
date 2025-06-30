"""Parsers for different credit card statements."""

from .nubank import parse_pdf as parse_nubank, matches as is_nubank
from .caixa import parse_pdf as parse_caixa, matches as is_caixa

__all__ = [
    "parse_nubank",
    "is_nubank",
    "parse_caixa",
    "is_caixa",
]
