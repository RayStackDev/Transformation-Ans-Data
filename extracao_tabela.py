import pdfplumber
import pandas as pd
import zipfile
import os

DADOS = {
    'PROCEDIMENTO': str,
    'RN (alteração)': str,
    'VIGÊNCIA': str,
    'OD': str,
    'AMB': str,
    'HCO': str,
    'HSO': str,
    'REF': str,
    'PAC': str,
    'DUT': 'Int64',
    'SUBGRUPO': str,
    'GRUPO': str,
    'CAPÍTULO': str
}


caminho_pdf = "Anexo/Anexo_I_Rol_2021RN_465.2021_RN654.2025.pdf"

with pdfplumber.open(caminho_pdf) as pdf:
    print(f"O PDF tem {len(pdf.pages)} paginas.")
    
    todas_linhas = []

    for numero_pagina, pagina in enumerate(pdf.pages, start=1):

        tabelas = pagina.extract_tables()
    

        for tabela in tabelas:
            for linha in tabela[1:]:
                todas_linhas.append(linha)

substituicoes = {
    "OD": "Odontologica",
    "AMD": "Ambulatorial"
}

for linha in todas_linhas:
    if linha[2] in substituicoes:
        linha[2] = substituicoes[linha[2]]

caminho_csv = os.path.join("output", "tabela_rol_procedimentos.csv")

with open(caminho_csv, mode="w", newline="", encoding="utf-8") as arquivo_csv:
    escritor = csv.writer(arquivo_csv)

    escritor.writerow(["Código", "Descrição", "Tipo", "OutraColuna1", "OutraColuna2"])

    escritor.writerows(todas_linhas)

print(f"CSV salvo em {caminho_csv}")