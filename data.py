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

# Sets path of deck, where the files used in the report are saved
day = date.today()
folder = foot /  f'Deck {day.strftime("%d.%m.%Y")}'

#Orchestrator
def dados():

    p, browser, context, page = get_browser()
    cmo_cammesa(page)
    repdoe(page)
    close_browser(p, browser)

#Handles browser
def get_browser():
    p = sync_playwright().start()
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    return p, browser, context, page

def close_browser(p, browser):
    browser.close()
    p.stop()

#Scrapes Marginal Costs in Argentina
def cmo_cammesa(page):

    #CAMMESA ARS Prices
    try:
        page.goto(f'https://microfe.cammesa.com/static-content/CammesaWeb/download-manager-files/Revistas/ProSem/pricesmercado.html', wait_until='load')
    except:
        sleep(2)
        page.goto(f'https://microfe.cammesa.com/static-content/CammesaWeb/download-manager-files/Revistas/ProSem/pricesmercado.html', wait_until='load')
    sleep(5)

    soup = BeautifulSoup(page.content(), 'lxml')
    prices_ars = pd.read_html(str(soup.select('table')).replace(',', '.'))[1]

    #Scrapes Exchange rate ARS-USD
    page.goto(f'https://www.bcb.gov.br/rex/sml/3-1-taxa.asp?frame=1')
    sleep(5)

    soup = BeautifulSoup(page.content(), 'lxml')
    usd_ars = pd.read_html(str(soup.select('table')), header=0)[0]
    exchange = float(usd_ars.iloc[0, 1].replace('.', '').replace(',', '.'))

    #Creates dataframe with USD prices
    prices_usd = prices_ars.copy()
    for i in range(7):
        prices_usd[f'Dia{i+1}'] = prices_ars[f'Dia{i+1}']/exchange
        prices_usd[f'Dia{i+1}'].round(2)

    prices_usd = prices_usd.round(2).applymap(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x).iloc[:,2:]
    prices_ars = prices_ars.round(2).applymap(lambda x: f'{x:.2f}' if isinstance(x, (int, float)) else x).iloc[:,2:]
    prices_ars.to_csv(folder / f'CMO_arg_peso.csv', index=False)
    prices_usd.to_csv(folder / f'CMO_arg.csv', index=False)

#Scrapes Executive Report on the Daily Scheduling of Electric Power Operations (REPDOE) from ONS
def repdoe(page):

    login = os.getenv('LOGIN-ONS')
    password = os.getenv('PASSWORD-ONS')

    local = folder / rf'REPDOE-{day.strftime("%Y%m%d")}.pdf'

    result = False
    trials = 0
    while not result and trials < 20:
        try:
            
            with page.expect_download() as download_info:

                page.goto(f'https://sintegre.ons.org.br/sites/9/51/_layouts/download.aspx?SourceUrl=/sites/9/51/Produtos/282/REPDOE-{dia.strftime("%Y%m%d")}.pdf')

                page.locator('xpath=//*[@id="username"]').fill(login)
                page.locator('xpath=//*[@id="password"]').fill(password)
                page.locator('xpath=//*[@id="kc-login"]').click()

            download = download_info.value
            sleep(2)
            download.save_as(local)

            result = True
        except:
            trials += 1
            sleep(10)  

# Scrapes text from pdf
def df_cmo():
    df = pd.read_csv(folder / f'CMO.csv', delimiter=';')
    return df

# Scrapes text from pdf
def load_text(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

dados()
