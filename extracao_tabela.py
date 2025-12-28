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

Mapeamento_legenda = {
    'OD': 'Seg. Odontológica',
    'AMB': 'Seg. Ambulatorial'
}

def limpar_texto(texto):
    if pd.isna(texto):
        return pd.NA
    return " ". join(str(texto).strip().replace("\n"))


def extrair_tabela(pdf_path):

    tabela_extraida = []

    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:

            tabela_pagina = pagina.extract_tables()
            
            if tabela_pagina:
                for tabela in tabela_pagina:

                    cabecalhos = [limpar_texto(c) for c in tabela[0]]
                    df = pd.DataFrame(tabela[1:], columns=cabecalhos)
                    tabela_extraida.append(df)


    return tabela_extraida