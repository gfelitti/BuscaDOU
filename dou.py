import argparse
import datetime
import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from tqdm import tqdm
from utils import obter_conteudo_dou, raspar_caderno, filtrar_dados

# Configurando o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Argumentos de linha de comando
parser = argparse.ArgumentParser(description='Extrai dados do DOU com base em um termo de busca e uma data específica.')
parser.add_argument('-t', '--termo', required=True, type=str, help='Palavra-chave para busca no DOU.')
parser.add_argument('-d', '--data', type=str, help='Data para raspar o DOU no formato dd-mm-aaa. O padrão é hoje.', default=datetime.date.today().strftime('%d-%m-%Y'))
args = parser.parse_args()

if __name__ == '__main__':
    termo_usuario = args.termo.lower()
    data_usuario = args.data
    cadernos = ['do1', 'do2']
    
    logging.info(f"Pegando os cadernos {', '.join(cadernos)} do dia {data_usuario} do DOU")
    conteudos = obter_conteudo_dou(data_usuario, cadernos)
    
    dou_final = []
    for conteudo in conteudos:
        dou_final.extend(raspar_caderno(conteudo))
    
    if dou_final:
        df_bruto = pd.DataFrame(dou_final, columns=['Seção', 'Organização Principal', 'Data', 'Referência', 'Título', 'Emenda', 'URL', 'Assinaturas'])
        filepath_bruto = os.path.join(os.getcwd(), f'DOU_bruto_{data_usuario}.csv')
        df_bruto.to_csv(filepath_bruto)
        logging.info(f"Arquivo bruto salvo em {filepath_bruto}")

        df_filtrado = filtrar_dados(dou_final, termo_usuario)
        if not df_filtrado.empty:
            filepath_filtrado = os.path.join(os.getcwd(), f'DOU_filtrado_{data_usuario}.csv')
            df_filtrado.to_csv(filepath_filtrado)
            logging.info(f"Arquivo filtrado salvo em {filepath_filtrado}")
        else:
            logging.warning(f'Nenhum resultado foi encontrado para o termo {termo_usuario}. Nenhum arquivo CSV filtrado foi criado.')
    else:
        logging.warning(f'Não foram encontrados registros no DOU para data {data_usuario}.')