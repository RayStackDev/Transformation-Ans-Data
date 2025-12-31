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

MAPEAMENTO_LEGENDA = {
    'OD': 'Seg. Odontológica',
    'AMB': 'Seg. Ambulatorial'
}

def limpar_texto(texto):

    if pd.isna(texto):
        return pd.NA
    return " ".join(str(texto).strip().replace("\n", " ").split())


def extrair_tabela(pdf_path):

    linhas = []

    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if texto:
                for linha in texto.split("\n"):
                    linhas.append(linha)


    return linhas


def processar_tabelas(lista_tabelas):

    if not lista_tabelas:
        raise ValueError("Nenhuma tabela foi extraída do PDF.")
    
    df_final = pd.concat(lista_tabelas, ignore_index=True)

    df_final = df_final.dropna(how="all")

    for coluna in df_final.columns:
        df_final[coluna] = df_final[coluna].apply(limpar_texto)

        if coluna in MAPEAMENTO_LEGENDA:
            df_final[coluna] = df_final[coluna].replace(MAPEAMENTO_LEGENDA)

    for coluna, tipo in DADOS.items():
        if coluna in df_final.columns:
            if tipo == "Int64":
                df_final[coluna] = pd.to_numeric(
                    df_final[coluna], errors="coerce"
                ).astype("Int64")
            else:
                df_final[coluna] = df_final[coluna].fillna("").astype(tipo)


    return df_final.reset_index(drop=True)


def salvar_csv(df, nome_arquivo):

    os.makedirs("output", exist_ok=True)

    caminho_csv = os.path.join("output", nome_arquivo)

    df.to_csv(
        caminho_csv,
        index=False,
        encoding="utf-8"
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
    df_final = processar_tabelas(tabelas)

    
    caminho_csv = salvar_csv(df_final, "rol_procedimentos.csv")

    nome_zip = "Teste_Raymond.zip"
    compactar_csv(caminho_csv, nome_zip)

    print("Processo finalizado com sucesso :D")

if __name__ == "__main__":
    main()