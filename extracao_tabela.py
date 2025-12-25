import pdfplumber

caminho_pdf = "Anexo/Anexo_I_Rol_2021RN_465.2021_RN654.2025.pdf"

with pdfplumber.open(caminho_pdf) as pdf:
    print(f"O PDF tem {len(pdf.pages)} paginas.")
    