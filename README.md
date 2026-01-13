# 📄 Transformação de Dados – PDF para CSV (ANS)

Este projeto contém um script em **Python** para **extrair tabelas de um arquivo PDF da ANS**, realizar **tratamento de caracteres especiais**, organizar os dados em formato tabular e gerar um **arquivo CSV**, que também é **compactado em ZIP**.

<br>

## 🎯 Objetivo do Projeto

Demonstrar, na prática:

- Leitura e extração de dados de arquivos **PDF**
- Tratamento e limpeza de dados textuais
- Correção de caracteres especiais (acentos, ç, etc.)
- Organização de dados com **pandas**
- Geração de arquivos **CSV**
- Compactação de arquivos em **ZIP**
- Boas práticas de organização de código e Git/GitHub

<br>

## ⚙️ Requisitos

- Python 3.x  
- pip (gerenciador de pacotes Python)

<br>

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git

cd seu-repositorio
```

2. Instale as dependências utilizando o `requirements.txt`:
```bash
pip install -r requirements.txt
```
<br>

## ▶️ Como usar

Execute o script principal:

```bash
python extracao_tabela.py
```

Ao final da execução:
- O arquivo **CSV** será gerado na pasta `output/`
- O arquivo **ZIP** será criado automaticamente

<br>

## ✨ Funcionalidades

- 📑 Leitura de PDFs com múltiplas páginas  
- 📊 Extração automática de tabelas  
- 🧹 Limpeza de textos:
  - Correção de caracteres especiais
  - Remoção de códigos invisíveis `(cid:xxx)`
  - Normalização Unicode
- 🗂️ Padronização das colunas conforme o rol da ANS  
- 📄 Geração de CSV compatível com Excel  
- 🗜️ Compactação do CSV em ZIP  
- 📁 Criação automática da pasta `output/`

<br>

## 🗂️ Estrutura do Projeto

```
projeto/
├── Anexo/
│   └── Anexo_I_Rol_2021RN_465.2021_RN654.2025.pdf
├── output/
│   ├── rol_procedimentos.csv
│   └── Teste_Raymond.zip
├── extracao_tabela.py
├── requirements.txt
└── README.md
```

<br>

## 🧰 Dependências Principais

- `pdfplumber` – extração de tabelas do PDF  
- `pandas` – tratamento e organização de dados  
- `re` – limpeza de padrões indesejados  
- `unicodedata` – normalização de caracteres  
- `zipfile` – compactação de arquivos  
- `os` – manipulação de diretórios  

<br>

## 🛠️ Tratamento de Erros

O script trata automaticamente:

- ❌ PDFs sem tabelas
- 🔤 Caracteres especiais quebrados
- 📉 Colunas ausentes no PDF
- 🔢 Conversão segura de dados numéricos
- 📁 Pastas inexistentes

<br>

## 📝 Observações

- O CSV é gerado com **separador `;`**, ideal para Excel (PT-BR)
- Codificação **UTF-8 com BOM**
- Projeto desenvolvido com foco em **aprendizado e clareza**

<br>

## 📚 Aprendizados

- Extração de dados estruturados a partir de PDFs  
- Tratamento de problemas de encoding  
- Transformação de dados com pandas  
- Organização de projetos Python para testes técnicos  
