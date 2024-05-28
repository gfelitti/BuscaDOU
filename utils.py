from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import logging
import randomheaders

def filtrar_dados(dou_final, termo):
    df = pd.DataFrame(dou_final, columns=['Seção', 'Organização Principal', 'Data', 'Referência', 'Título', 'Emenda', 'URL', 'Assinaturas'])
    df[['Emenda', 'Título']] = df[['Emenda', 'Título']].map(str.lower)
    df_filtrado = df[df['Emenda'].str.contains(termo, case=False, na=False) | df['Título'].str.contains(termo, case=False, na=False)]
    return df_filtrado

def obter_conteudo_dou(data_formatada, cadernos):
    url_base = f'http://www.in.gov.br/leiturajornal?data={data_formatada}&secao='

    conteudos = []
    for caderno in cadernos:
        try:
            response = requests.get(url_base + caderno, 
                                    headers=randomheaders.LoadHeader())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            script = soup.find("script", {"id": "params"})
            if script:
                conteudo = json.loads(script.text)
                if 'jsonArray' in conteudo and conteudo['jsonArray']:
                    conteudos.append(conteudo)
                else:
                    logging.warning(f'Nenhuma publicação encontrada no caderno {caderno} para a data {data_formatada}. Conteúdo jsonArray está vazio.')
            else:
                logging.error(f'Não foi possível encontrar o script JSON para {caderno}. Verifique se o ID está correto e a página contém dados.')
        except requests.RequestException as e:
            logging.error(f'Erro ao buscar dados para {caderno}: {e}')
    return conteudos


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