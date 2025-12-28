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


def processar_tabelas(lista_tabelas):

    if not lista_tabelas:
        raise ValueError("Nenhuma tabela foi extraída do PDF.")
    
    df_final = pd.concat(lista_tabelas, ignore_index=True)

    df_final = df_final.dropna(how="all")

    for coluna in df_final.columns:
        df_final[coluna] = df_final[coluna].apply(limpar_texto)

        if coluna in Mapeamento_legenda:
            df_final[coluna] = df_final[coluna].replace(Mapeamento_legenda)

    for coluna, tipo in DADOS.items():
        if coluna in df_final.columns:
            if tipo == "Int64":
                df_final[coluna] = pd.to_numeric(
                    df_final[coluna], errors="coerce"
                ).astype("Int64")
            else:
                df_final[coluna] = df_final[coluna].fillna("").astype(tipo)


    return df_final.reset_index(drop=True)