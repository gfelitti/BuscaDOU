import argparse
import json
import datetime
import requests
import pandas as pd
from utils import raspar_caderno
from bs4 import BeautifulSoup
import os
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser( description= 'DOU Online')

# argumentos posicionais / obrigatórios
parser.add_argument('-t', '--termo', type =str, help='Escreva aqui a palavra que você busca no DOU')
# parser.add_argument('data', type='str', help='Digite aqui a data do DOU que você quer raspar. Formato: aaaa-mm-dd')

# armazenar os resultados do conteúdo dado pelo usuário + tratar o conteudo
args = parser.parse_args()
# para acessar um conteúdo escrito pelo usuário, você pode fazer 'args.termo', 'args.data'... 

# para garantir que o código aqui só seja executado quando o script for executado diretamente
if __name__ == '__main__': 
  cadernos=['do1','do2','do3']
  data=datetime.date.today()
  data_formatada=data.strftime('%d-%m-%Y')
  url=f'http://www.in.gov.br/leiturajornal?data={data_formatada}&secao='
  integra=[]

  print(f"Pegando os cadernos {', '.join(cadernos)} do dia {data_formatada} do DOU")

  for caderno in cadernos:
    page = requests.get(url+caderno)
    soup = BeautifulSoup(page.text, 'html.parser')
    conteudo = json.loads(soup.find("script", {"id": "params"}).text)
    integra.append(conteudo)

  dou_final=[]
  for json_caderno in integra:
    raspagem = raspar_caderno(json_caderno)
    for item in raspagem:
      dou_final.append(item)
      
  df=pd.DataFrame(dou_final, columns=['Seção', 'Organização Principal', 'Data', 'Referência', 'Título', 'Emenda', 'URL', 'Assinaturas'])

  # filtro do dou com o termo enviado pelo usuário

  filepath=os.path.join(os.getcwd(), f'DOU_completo_{data_formatada}.csv')
  df.to_csv(filepath)

