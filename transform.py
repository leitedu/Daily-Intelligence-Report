import pandas as pd
from datetime import date

data = date.today()
pasta = fr'C:\Users\eduardosilva-aeg\OneDrive - AMBAR ENERGIA LTDA\Documentos\Materiais\Apresentações\01. Janeiro 2026\Relatório de Inteligencia - diário\Deck {data.strftime("%d.%m.%Y")}'


def tabela_pld():
    df_pld = pd.read_csv(rf'{pasta}\PLD_relat_d.csv', delimiter=';')
    df_pld1, df_pld2 = df_pld[df_pld['Data'] == df_pld['Data'].iloc[0]], df_pld[df_pld['Data'] == df_pld['Data'].iloc[-1]]
    return df_pld1, df_pld2

def precos_importacao():
    #Lê arquivo de preços
    pasta = fr'C:\Users\eduardosilva-aeg\OneDrive - AMBAR ENERGIA LTDA\Documentos\Materiais\Apresentações\01. Janeiro 2026'
    df_precos = pd.read_csv(rf'{pasta}\precos.csv', delimiter=';')
    
    #Filtra última semana disponível
    df_precos['dat_iniciovalidade'] = pd.to_datetime(df_precos['dat_iniciovalidade'], format='%Y-%m-%d')
    hj_preco = df_precos['dat_iniciovalidade'].max()
    filtro_preco = df_precos[df_precos['dat_iniciovalidade'] == hj_preco]
    
    #Separa datas de início e fim e remove colunas do df
    data_inicio, data_fim = hj_preco, hj_preco + pd.Timedelta(days=6)
    filtro_preco.drop(columns=['dat_iniciovalidade', 'dat_fimvalidade'], inplace=True)
    
    #Separa df Argentina e Uruguai
    preco_ar = filtro_preco[filtro_preco['nom_pais'] == 'ARGENTINA']
    preco_ur = filtro_preco[filtro_preco['nom_pais'] == 'URUGUAI']

    return data_inicio, data_fim, preco_ar, preco_ur

def importacao_blocos():
    #Lê blocos
    pasta = fr'C:\Users\eduardosilva-aeg\OneDrive - AMBAR ENERGIA LTDA\Documentos\Materiais\Apresentações\01. Janeiro 2026'
    df_bloco = pd.read_csv(rf'{pasta}\blocos.csv', delimiter=';')
    df_bloco[['data', 'hora']] = df_bloco['din_instante'].str.split(' ', expand=True)
    df_bloco = df_bloco.drop(columns=['din_instante'])

    #Filtra última data disponível
    df_bloco['data'] = pd.to_datetime(df_bloco['data'], format='%Y-%m-%d')
    ultima = df_bloco['data'].max()
    filtro_bloco = df_bloco[df_bloco['data'] == ultima].drop(columns=['data'])
    bloco_group = (
                    filtro_bloco
                   .groupby(['nom_pais', 'nom_agente', 'nom_bloco'], as_index=False)
                   .agg({'val_importacaoprogramada':'mean',
                         'val_importacaodespachada':'mean',
                         'val_importacaoverificada':'mean',
                         'val_preco':'mean'})
                         )
    
    #Separa df Argentina e Uruguai
    bloco_ar = bloco_group[bloco_group['nom_pais'] == 'ARGENTINA']
    bloco_ur = bloco_group[bloco_group['nom_pais'] == 'URUGUAI']

    return ultima, bloco_ar, bloco_ur
