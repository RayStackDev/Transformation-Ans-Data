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