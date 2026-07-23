from dados import *
from transform import *
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import os

#Load environment variables from .env file
load_dotenv()
root = Path(os.getenv('PASTA'))

# Sets path of deck, where the files used in the report are taken
day = date.today()
folder = root /  f'Deck {day.strftime("%d.%m.%Y")}'

def load_content():

    #1 Marginal System Cost (CMO) in Brazil
    cmo = df_cmo()
    #2 Electricity Spot Price (PLD) in Brazil
    pld = pld_table()
    #3 Marginal System Cost (CMO) in Argentina
    cmo_arg = pd.read_csv(folder / f'CMO_arg.csv', delimiter=',')
    #4 Exchange Electricity Prices by Submarket in Brazil 
    bbce = pd.read_csv(folder / f'marcacao_bbce.csv', delimiter=';')
    #5 Natural gas Prices
    gas_prices = pd.read_csv(folder / f'gas_prices.csv', delimiter=';')
    #6 Thermal dispatch in the day - Brazil
    br_dispatch = folder / f'despacho_termico_brasil.png'
    #7 Highest Variable Unitary Costs of thermal plants in Brazil, by submarket 
    m_cvus = pd.read_csv(folder / f'maiores_cvus.csv', delimiter=';')
    #8 Stored energy in hidric reservoirs
    ena = folder / f'ENA.png'
    #9 Electricity exchanges between Brazil, Argentina and Uruguay (Volume, Prices and Offers)
    exchanges = folder / f'exchanges.png'
    start_imp_price, end_imp_price, price_ar, price_ur = import_prices()
    data_blocks, block_ar, block_ur = import_blocks()
    

    return [{'type': 'table',
             'title': 'CMO (R$/MWh)',
             'data': cmo},

            {'type': 'two_tables',
             'title': 'PLD (R$/MWh)',
             'data': pld},

             {'type': 'table',
             'title': 'Weekly Argentine CMO (US$/MWh)',
             'data': cmo_arg},

             {'type': 'table',
             'title': 'BBCE prices (R$/MWh)',
             'data': bbce},

             {'type': 'table',
             'title': 'Natural gas prices (R$/m³)',
             'data': gas_prices},
             
             {'type': 'table',
             'title': 'Highest dispatched CVUs (R$/MWh)',
             'data': m_cvus},

             {'type': 'image',
             'title': 'Thermal dispatch Brazil',
             'data': br_dispatch},

             {'type': 'image',
             'title': 'ENA',
             'data': ena},
            
             {'type': 'two_tables',
             'title': f'Import prices by Block {start_imp_price.strftime("%d.%m.%Y")} to {end_imp_price.strftime("%d.%m.%Y")} (R$/MWh)',
             'data': [price_ar, price_ur]},

             {'type': 'two_tables',
             'title': f'Imported volume by Block {data_blocks.strftime("%d.%m.%Y")} (MW)',
             'data': [block_ar, block_ur]},
            
             {'type': 'image', 'title': 'Iinternational energy exchanges', 'data': exchanges},

             ]
