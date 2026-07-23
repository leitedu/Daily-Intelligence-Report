from dados import *
from transform import *
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import os

#Load environment variables from .env file
load_dotenv()
root = Path(os.getenv('PASTA'))

dia = date.today()
folder = root /  f'Deck {dia.strftime("%d.%m.%Y")}'

def load_content():

    #1 Marginal System Cost (CMO) in Brazil
    cmo_barra = df_cmo_barra()
    #2 Electricity Spot Price (PLD) in Brazil
    pld = tabela_pld()
    #3 Marginal System Cost (CMO) in Argentina
    cmo_arg = pd.read_csv(folder / f'CMO_arg.csv', delimiter=',')
    #4 Exchange Electricity Prices by Submarket in Brazil 
    bbce = pd.read_csv(folder / f'marcacao_bbce.csv', delimiter=';')
    #5 Natural gas Prices
    pg_usinas = pd.read_csv(folder / f'pg_usinas.csv', delimiter=';')
    #6 Thermal dispatch in the day - Brazil
    despacho_br = folder / f'despacho_termico_brasil.png'
    #7 Biggest Variable Unitary Costs of thermal plants in Brazil, by submarket 
    m_cvus = pd.read_csv(folder / f'maiores_cvus.csv', delimiter=';')
    #8 Stored energy in hidric reservoirs
    ena = folder / f'ENA.png'
    #9 Electricity exchanges between Brazil, Argentina and Uruguay (Volume, Prices and Offers)
    intercambios = folder / f'intercambios.png'
    inicio_imp_preco, fim_imp_preco, preco_ar, preco_ur = precos_importacao()
    data_blocos, bloco_ar, bloco_ur = importacao_blocos()
    

    return [{'type': 'table',
             'title': 'CMO na barra por usina (R$/MWh)',
             'data': cmo_barra},

            {'type': 'two_tables',
             'title': 'PLD (R$/MWh)',
             'data': pld},

             {'type': 'table',
             'title': 'CMO Semanal Argentina (US$/MWh)',
             'data': cmo_arg},

             {'type': 'table',
             'title': 'Marcação de Preços BBCE por submercado (R$/MWh)',
             'data': bbce},

             {'type': 'table',
             'title': 'Preços de gás (R$/m³)',
             'data': pg_usinas},
             
             {'type': 'table',
             'title': 'Maiores CVUs despachados (R$/MWh)',
             'data': m_cvus},

             {'type': 'image',
             'title': 'Despacho térmico Brasil',
             'data': despacho_br},

             {'type': 'image',
             'title': 'ENA',
             'data': ena},
            
             {'type': 'two_tables',
             'title': f'Preços de importação por bloco {inicio_imp_preco.strftime("%d.%m.%Y")} a {fim_imp_preco.strftime("%d.%m.%Y")} (R$/MWh)',
             'data': [preco_ar, preco_ur]},

             {'type': 'two_tables',
             'title': f'Importação por bloco {data_blocos.strftime("%d.%m.%Y")} (MW)',
             'data': [bloco_ar, bloco_ur]},
            
             {'type': 'image', 'title': 'Intercâmbios de energia internacionais', 'data': intercambios},

             ]
