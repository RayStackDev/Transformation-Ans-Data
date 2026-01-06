import pdfplumber
import pandas as pd
import zipfile
import os
import re
import unicodedata


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

MAPEAMENTO_LEGENDA = {
    'OD': 'Seg. Odontológica',
    'AMB': 'Seg. Ambulatorial'
}


def corrigir_mojibake(texto: str) -> str:
    try:
        return texto.encode('latin1').decode('utf-8')
    except Exception:
        return texto


def limpar_texto(texto):
    if texto is None:
        return ""
    
    texto = str(texto)
    texto = re.sub(r"\(cid:\d+\)", "", texto)
    texto = corrigir_mojibake(texto)
    texto = unicodedata.normalize("NFC", texto)
    texto = texto.replace("\n", " ")
    texto = " ".join(texto.split())

    return texto


def extrair_tabela(caminho_path):
    tabelas = []

    with pdfplumber.open(caminho_path) as pdf:
        for pagina in pdf.pages:
            tabelas_pagina = pagina.extract_tables()
            if tabelas_pagina:
                for tabela in tabelas_pagina:
                    cabecalhos = [limpar_texto(c) for c in tabela[0]]
                    dados = tabela[1:]
                    df = pd.DataFrame(dados, columns=cabecalhos)
                    tabelas.append(df)

    return tabelas


def organizar_dados(tabelas):

    df = pd.concat(tabelas, ignore_index=True)
    df= df.dropna(how="all")

    for coluna in df.columns:
        df[coluna] = df[coluna].apply(limpar_texto)
        if coluna in MAPEAMENTO_LEGENDA:
            df[coluna] = df[coluna].replace(MAPEAMENTO_LEGENDA)

    for coluna, tipo in DADOS:
        if coluna not in df.columns:
            df[coluna] = ""

    df = df[DADOS]
    df['DUT'] = pd.to_numeric(df['DUT'], errors='coerce').astype('Int64')

    return df.reset_index(drop=True)


def salvar_csv(df, nome_arquivo):

    os.makedirs("output", exist_ok=True)

    caminho_csv = os.path.join("output", nome_arquivo)

    df.to_csv(
        caminho_csv,
        index=False,
        encoding="utf-8-sig",
        sep=";"
    )

    return caminho_csv


def compactar_csv(caminho_csv, nome_zip):

    caminho_zip = os.path.join("output", nome_zip)

    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(caminho_csv, arcname=os.path.basename(caminho_csv))

    
    return caminho_zip


def main():
    caminho_pdf = "Anexo/Anexo_I_Rol_2021RN_465.2021_RN654.2025.pdf"

    tabelas = extrair_tabela(caminho_pdf)
    df_final = organizar_dados(tabelas)

    
    caminho_csv = salvar_csv(df_final, "rol_procedimentos.csv")

    nome_zip = "Teste_Raymond.zip"
    compactar_csv(caminho_csv, nome_zip)

    print("Processo finalizado com sucesso :D")

if __name__ == "__main__":
    main()