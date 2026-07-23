import pandas as pd
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import os

#Load environment variables from .env file
load_dotenv()
root = Path(os.getenv('PASTA'))

day = date.today()
# Sets path of deck, which is the folder where the files used in the report are taken
folder = foot /  f'Deck {day.strftime("%d.%m.%Y")}'

def pld_table():
    df_pld = pd.read_csv(folder / f'PLD_relat_d.csv', delimiter=';')
    df_pld1, df_pld2 = df_pld[df_pld['Data'] == df_pld['Data'].iloc[0]], df_pld[df_pld['Data'] == df_pld['Data'].iloc[-1]]
    return df_pld1, df_pld2

def import_prices():
    #Reads prices file 
    df_prices = pd.read_csv(folder / 'prices.csv', delimiter=';')
    
    #Gets last available data
    df_prices['dat_iniciovalidade'] = pd.to_datetime(df_prices['dat_iniciovalidade'], format='%Y-%m-%d')
    hj_price = df_prices['dat_iniciovalidade'].max()
    filter_price = df_prices[df_prices['dat_iniciovalidade'] == hj_price]
    
    #Filters start and end dates
    start_date, end_date = hj_price, hj_price + pd.Timedelta(days=6)
    filter_price.drop(columns=['dat_iniciovalidade', 'dat_fimvalidade'], inplace=True)
    
    #Creates distinct dfs to Argentina and Uruguay
    price_ar = filter_price[filter_price['nom_pais'] == 'ARGENTINA']
    price_ur = filter_price[filter_price['nom_pais'] == 'URUGUAI']

    return start_date, end_date, price_ar, price_ur

def import_blocks():
    #Reads file
    df_block = pd.read_csv(folder / 'blocks.csv', delimiter=';')
    df_block[['data', 'hora']] = df_block['din_instante'].str.split(' ', expand=True)
    df_block = df_block.drop(columns=['din_instante'])

    #Gets last available data
    df_block['data'] = pd.to_datetime(df_block['data'], format='%Y-%m-%d')
    last = df_block['data'].max()
    filter_block = df_block[df_block['data'] == last].drop(columns=['data'])
    block_group = (
                    filter_block
                   .groupby(['nom_pais', 'nom_agente', 'nom_block'], as_index=False)
                   .agg({'val_importacaoprogramada':'mean',
                         'val_importacaodespachada':'mean',
                         'val_importacaoverificada':'mean',
                         'val_price':'mean'})
                         )
    
    #Separates Uruguay and Argentina
    block_ar = block_group[block_group['nom_pais'] == 'ARGENTINA']
    block_ur = block_group[block_group['nom_pais'] == 'URUGUAI']

    return last, block_ar, block_ur
