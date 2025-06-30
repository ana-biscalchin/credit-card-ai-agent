"""Main entry point with graphical interface to extract credit card statements."""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import pandas as pd

from extractors import nubank, caixa
from utils.file_utils import save_to_csv


class App:
    """Simple Tkinter GUI to select PDF and export transactions."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Extrator de Faturas")

        btn_select = tk.Button(root, text="Selecionar PDF", command=self.select_pdf)
        btn_select.pack(pady=10)

        self.lbl_file = tk.Label(root, text="Nenhum arquivo selecionado")
        self.lbl_file.pack(pady=5)

        btn_export = tk.Button(root, text="Gerar CSV", command=self.export_csv)
        btn_export.pack(pady=10)

        self.pdf_path: Path | None = None

    def select_pdf(self) -> None:
        """Open a file dialog to choose a PDF file."""
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.pdf_path = Path(filename)
            self.lbl_file.config(text=str(self.pdf_path))

    def export_csv(self) -> None:
        """Process the selected PDF and generate a CSV file."""
        if not self.pdf_path:
            messagebox.showwarning("Atenção", "Selecione um arquivo PDF primeiro")
            return

        parser = self.detect_parser(self.pdf_path)
        if not parser:
            messagebox.showerror(
                "Erro", "Não foi possível identificar o emissor da fatura"
            )
            return

        df = parser(self.pdf_path)
        if df.empty:
            messagebox.showerror(
                "Erro", "Nenhuma transação encontrada no PDF"
            )
            return

        csv_path = save_to_csv(df, self.pdf_path)
        messagebox.showinfo("Sucesso", f"CSV gerado em {csv_path}")

    @staticmethod
    def detect_parser(path: Path):
        """Return the correct parser based on PDF contents."""
        if nubank.matches(path):
            return nubank.parse_pdf
        if caixa.matches(path):
            return caixa.parse_pdf
        return None


def main() -> None:
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
