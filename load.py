from dados import *
from transform import *
from datetime import date

data = date.today()
pasta = fr'C:\Users\eduardosilva-aeg\OneDrive - AMBAR ENERGIA LTDA\Documentos\Materiais\Apresentações\01. Janeiro 2026\Relatório de Inteligencia - diário\Deck {data.strftime("%d.%m.%Y")}'

def load_content():

    #1
    cmo_barra = df_cmo_barra()
    #2
    pld = tabela_pld()
    #3
    cmo_arg = pd.read_csv(rf'{pasta}\CMO_arg.csv', delimiter=',')
    #4 bbce
    bbce = pd.read_csv(rf'{pasta}\marcacao_bbce.csv', delimiter=';')
    #5 precos_gas
    pg_usinas = pd.read_csv(rf'{pasta}\pg_usinas.csv', delimiter=';')
    #6 despacho_ambar
    #7
    despacho_br = rf'{pasta}\despacho_termico_brasil.png'
    #8 maiores_cvus
    m_cvus = pd.read_csv(rf'{pasta}\maiores_cvus.csv', delimiter=';')
    #9
    ena = rf'{pasta}\ENA.png'
    #10 intercambios
    intercambios = rf'{pasta}\intercambios.png'
    inicio_imp_preco, fim_imp_preco, preco_ar, preco_ur = precos_importacao()
    data_blocos, bloco_ar, bloco_ur = importacao_blocos()
    #11 variacoes
    variacoes = load_texto(rf'{pasta}\variacao_programacao.txt')
    

    return [{'type': 'table',
             'title': 'CMO na barra por usina (R$/MWh)',
             'data': cmo_barra},

            {'type': 'two_tables',
             'title': 'PLD (R$/MWh)',
             'data': pld},

             #{'type': 'table',
             #'title': 'CMO Semanal Argentina (US$/MWh)',
             #'data': cmo_arg},

             #{'type': 'table',
             #'title': 'Marcação de Preços BBCE por sumercado (R$/MWh)',
             #'data': bbce},

             {'type': 'table',
             'title': 'Preços de gás postos nas usinas (R$/m³)',
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

             {'type': 'image', 'title': 'Intercâmbios de energia internacionais', 'data': intercambios},

             {'type': 'text',
             'title': 'Variações na programação IPDO',
             'data': variacoes}
             ]


'''

             {'type': 'two_tables',
             'title': f'Preços de importação por bloco {inicio_imp_preco.strftime("%d.%m.%Y")} a {fim_imp_preco.strftime("%d.%m.%Y")} (R$/MWh)',
             'data': [preco_ar, preco_ur]},

             {'type': 'two_tables',
             'title': f'Importação por bloco {data_blocos.strftime("%d.%m.%Y")} (MW)',
             'data': [bloco_ar, bloco_ur]},

'''