from playwright.sync_api import sync_playwright
from datetime import date
from bs4 import BeautifulSoup
from time import sleep, strftime
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import os

#Load environment variables from .env file
load_dotenv()
root = Path(os.getenv('PASTA'))

dia = date.today()
folder = foot /  f'Deck {dia.strftime("%d.%m.%Y")}'

def dados():

    p, browser, context, page = get_browser()
    cmo_cammesa(page)
    repdoe(page)
    close_browser(p, browser)


def get_browser():
    p = sync_playwright().start()
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    return p, browser, context, page

def close_browser(p, browser):
    browser.close()
    p.stop()


def cmo_cammesa(page):

    #Precios CAMMESA ARS
    try:
        page.goto(f'https://microfe.cammesa.com/static-content/CammesaWeb/download-manager-files/Revistas/ProSem/preciosmercado.html', wait_until='load')
    except:
        sleep(2)
        page.goto(f'https://microfe.cammesa.com/static-content/CammesaWeb/download-manager-files/Revistas/ProSem/preciosmercado.html', wait_until='load')
    sleep(5)

    soup = BeautifulSoup(page.content(), 'lxml')
    precios_ars = pd.read_html(str(soup.select('table')).replace(',', '.'))[1]

    #Scraping cambio
    page.goto(f'https://www.bcb.gov.br/rex/sml/3-1-taxa.asp?frame=1')
    sleep(5)

    soup = BeautifulSoup(page.content(), 'lxml')
    usd_ars = pd.read_html(str(soup.select('table')), header=0)[0]
    cambio = float(usd_ars.iloc[0, 1].replace('.', '').replace(',', '.'))

    #DF Precios USD
    precios_usd = precios_ars.copy()
    for i in range(7):
        precios_usd[f'Dia{i+1}'] = precios_ars[f'Dia{i+1}']/cambio
        precios_usd[f'Dia{i+1}'].round(2)

    precios_usd = precios_usd.round(2).applymap(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x).iloc[:,2:]
    precios_ars = precios_ars.round(2).applymap(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x).iloc[:,2:]
    precios_ars.to_csv(f'{folder}\\CMO_arg_peso.csv', index=False)
    precios_usd.to_csv(f'{folder}\\CMO_arg.csv', index=False)


def repdoe(page):

    login = 'eduardo.leite@ambarenergia.com.br'
    senha = 'Ambar-energia@2025'
    dia = date.today()

    local = rf'{folder}\REPDOE-{dia.strftime("%Y%m%d")}.pdf'

    result = False
    tentativas = 0
    while not result and tentativas < 20:
        try:
            
            with page.expect_download() as download_info:

                page.goto(f'https://sintegre.ons.org.br/sites/9/51/_layouts/download.aspx?SourceUrl=/sites/9/51/Produtos/282/REPDOE-{dia.strftime("%Y%m%d")}.pdf')

                page.locator('xpath=//*[@id="username"]').fill(login)
                page.locator('xpath=//*[@id="password"]').fill(senha)
                page.locator('xpath=//*[@id="kc-login"]').click()

            download = download_info.value
            sleep(2)
            download.save_as(local)

            result = True
        except:
            tentativas += 1
            sleep(300)  


def df_cmo_barra():
    df = pd.read_csv(f'{folder}\\CMO_barra.csv', delimiter=';')
    return df


def load_texto(path):
    with open(path, 'r', encoding='utf-8') as file:
        conteudo = file.read()
    return conteudo

dados()
