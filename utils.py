from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import requests

def raspar_caderno(json_caderno):
    raspagem = []
    objeto_dou=json_caderno['jsonArray']
    desc_tqdm = f"Raspando {json_caderno['jsonArray'][0]['pubName']}"

    for decreto in tqdm(objeto_dou, desc=desc_tqdm):
        secao = decreto['pubName']
        organizacao_principal = decreto['hierarchyStr']
        data = decreto['pubDate']
        referencia = 'Edição Nº' + decreto['editionNumber'] + ' de ' + decreto['pubDate'] + ' - Pág. ' + decreto['numberPage']
        titulo = decreto['title']
        emenda = decreto['content'].replace("<span class='highlight' style='background:#FFA;'>", "").replace("</span>", "")
        url_decreto = 'https://www.in.gov.br/web/dou/-/' + decreto['urlTitle']
        raspagem_decreto = BeautifulSoup((requests.get(url_decreto)).content, 'html.parser')
        time.sleep(0.3)
        lista_assinaturas = []

        assina_lula = raspagem_decreto.findAll('p', {'class' : "assinaPr"})
        if assina_lula:
            lula = assina_lula[0].text.capitalize()
            lista_assinaturas.append(lula)

        assina_min = raspagem_decreto.findAll('p', {'class' : "assina"})

        for i,_ in enumerate(assina_min):
            ministro = assina_min[i].text
            lista_assinaturas.append(ministro)

    
        raspagem.append([secao, organizacao_principal, data, referencia, titulo, emenda, url_decreto, ', '.join(lista_assinaturas)])

    return raspagem