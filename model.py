import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import os
import platform
import subprocess


def abrir_arquivo_no_sistema(caminho_arquivo):
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(caminho_arquivo)
        elif sistema == "Darwin":  # macOS
            subprocess.call(["open", caminho_arquivo])
        else:  # Linux e outros
            subprocess.call(["xdg-open", caminho_arquivo])
    except Exception as e:
        print(f"Não foi possível abrir o arquivo automaticamente: {e}")


def scraper_ml(busca, paginas=1):
    produtos = []
    precos = []
    notas = []
    fretes = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/134.0.0.0 Safari/537.36"
        )
    }

    for pagina in range(1, paginas + 1):
        url = (
            f"https://lista.mercadolivre.com.br/"
            f"{busca}_Desde_{(pagina - 1) * 50 + 1}"
        )

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        itens = soup.find_all('li', class_='ui-search-layout__item')

        for item in itens:
            titulo_tag = item.find('a', class_='poly-component__title')
            preco_tag = item.find(
                'span', class_='andes-money-amount__fraction')

            nota_tag = item.find('span', class_='poly-reviews__rating')
            frete_tag = item.find('div', class_='poly-component__shipping')

            if titulo_tag and preco_tag:
                produtos.append(titulo_tag.text.strip())
                precos.append("R$ " + preco_tag.text.strip())
                notas.append(nota_tag.text.strip() if nota_tag else "-")
                fretes.append(
                    "✔️" if frete_tag and
                    "frete grátis" in frete_tag.text.lower() else "❌")

    # Criar DataFrame
    df = pd.DataFrame({
        'Produto': produtos,
        'Preço (R$)': precos,
        'Nota': notas,
        'Frete Grátis': fretes
    })

    arquivo = f"produtos_{busca}.xlsx"
    df.to_excel(arquivo, index=False)

    # Estilizar Excel
    wb = load_workbook(arquivo)
    ws = wb.active

    # Estilos
    header_font = Font(bold=True, color="000000", name="Calibri")
    header_fill = PatternFill("solid", fgColor="DDEBF7")
    cell_font = Font(name="Calibri", size=11)
    align_left = Alignment(
        horizontal="left", vertical="center", wrap_text=False)

    border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD'),
    )

    # Estilizar cabeçalho
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_left
        cell.border = border

    # Estilizar dados
    for row in ws.iter_rows(min_row=2,
                            max_row=ws.max_row, min_col=1, max_col=4):

        for cell in row:
            cell.font = cell_font
            cell.alignment = align_left
            cell.border = border

        # Frete Grátis (coluna D)
        frete_cell = row[3]
        if frete_cell.value == '✔️':
            frete_cell.font = Font(color="008000", name="Calibri")  # Verde
        elif frete_cell.value == '❌':
            frete_cell.font = Font(color="FF0000", name="Calibri")  # Vermelho

    # Altura padrão das linhas
    for row_idx in range(2, ws.max_row + 1):
        ws.row_dimensions[row_idx].height = 18

    # Ajustar larguras das colunas
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_length = max(
            (len(str(cell.value)) if cell.value else 0) for cell in col)

        ws.column_dimensions[col_letter].width = max_length + 2

    wb.save(arquivo)

    # Abrir arquivo automaticamente
    abrir_arquivo_no_sistema(arquivo)

    return arquivo
