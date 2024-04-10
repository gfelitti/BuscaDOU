import datetime
import json
import requests
import pandas as pd
import time

from bs4 import BeautifulSoup
from datetime import datetime

# Objetivo
# Criar um scrapper que raspe todas as vezes que uma palavra x apareceu no dou


# adicionar no futuro
# 1. limite de data para a coleta do raspador pra não ficar num looping eterno / coletar por ano
# 2. fazer try/except para ConnectionError
# 3. fazer random de time.sleep
# 4. fazer looping para todas as páginas
# 5. identificar parte do texto que diz sobre o termo




def raspador_termo_dou(url):

    raspagem = []

    # raspar a url usando requests e BeautifulSoup
    raspagem_dou = BeautifulSoup((requests.get(url)).content)
    time.sleep(3)



    # Descobrir o número de página que tem aquele termo no DOU
    # Ver quantas páginas tem

    # Ver como a URL muda quando passa para a página seguinte

    # Começar com a url original e ir no looping adicionando as páginas



    # Encontre o script com o objeto JSON e extrai o conteúdo do script (.string)
    decreto_string = raspagem_dou.find('script', {'id':'_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_params'}).string

    # Analisa o objeto JSON em um array de objetos Python
    json_obj = json.loads(decreto_string)
    objeto_dou = json_obj['jsonArray']

    # Looping para cada um dos decretos dessa página
    for decreto in objeto_dou:
        secao = decreto['pubName']
        organizacao_principal = decreto['hierarchyStr']
        data = decreto['pubDate']
        mes = data[3:5]
        ano = data[6:]
        referencia = 'Edição Nº' + decreto['editionNumber'] + ' de ' + decreto['pubDate'] + ' - Pág. ' + decreto['numberPage']
        titulo = decreto['title']
        emenda = decreto['content'].replace("<span class='highlight' style='background:#FFA;'>", "").replace("</span>", "")
        url_decreto = 'https://www.in.gov.br/web/dou/-/' + decreto['urlTitle']


        # Entrar na URL do decreto para saber o que tem nele
        # raspar a url usando requests e BeautifulSoup
        raspagem_decreto = BeautifulSoup((requests.get(url_decreto)).content)
        time.sleep(2)

        # coletar assinaturas
        lista_assinaturas = []

        # Assinatura Lula
        assina_lula = raspagem_decreto.findAll('p', {'class' : "assinaPr"})
        if assina_lula:
            lula = assina_lula[0].text.capitalize()
            lista_assinaturas.append(lula)

        # Assinatura ministros
        assina_min = raspagem_decreto.findAll('p', {'class' : "assina"})
        
        for i, valor in enumerate(assina_min):
            ministro = assina_min[i].text
            lista_assinaturas.append(ministro)

        # salvar o conteúdo na lista raspagem para depois converterem df
        raspagem.append([secao, organizacao_principal, data, mes, ano, referencia, titulo, emenda, url_decreto, ', '.join(lista_assinaturas)])

    df = pd.DataFrame(raspagem, columns=['secao', 'organizacao_principal', 'data', 'mes', 'ano', 'referencia', 'titulo', 'emenda', 'url_decreto', 'assinaturas'])
    
    # Baixar um arquivo com as aparições do termo no DOU
    df.to_csv('df_termo')