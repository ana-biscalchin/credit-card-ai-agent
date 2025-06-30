# Credit Card Statement Extractor

Este projeto extrai transações de faturas de cartão de crédito do Nubank em PDF e exporta para CSV. Possui uma interface gráfica simples usando `tkinter`.

## Como usar

1. Crie o ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o agente:
   ```bash
   python main.py
   ```

4. Selecione o PDF desejado e clique em **Gerar CSV**. O arquivo será criado na mesma pasta do PDF.

## Estrutura do Projeto

```
.
├── main.py
├── extractors/
│   ├── __init__.py
│   ├── nubank.py
├── utils/
│   ├── __init__.py
│   └── file_utils.py
├── requirements.txt
└── README.md
```
