import requests
import bs4

#INICIANDO AS RASPAGENS DE EDUCAÇÃO
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
url_insper = "https://www.insper.edu.br/imprensa/"

def raspar_insper(headers, url_insper):
  result_insper = requests.get(url_insper,  headers = headers)
  soup_insper = bs4.BeautifulSoup(result_insper.text, 'html.parser')
  links_insper = soup_insper.find_all('div', { 'class': '_thumbnail__descricao no-paddingM' })
  noticias_insper = []
  for link in links_insper:
    link_insper = link.find('a').get('href')
    titulo = link.find('a').text.strip()
    noticias_insper.append([titulo,link_insper])
  return noticias_insper

raspar_insper(headers, url_insper)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
url_peninsula = "https://www.institutopeninsula.org.br/noticias/"

def raspar_peninsula(headers, url_peninsula):
  result_peninsula = requests.get(url_peninsula,  headers = headers)
  soup_peninsula = bs4.BeautifulSoup(result_peninsula.text, 'html.parser')
  links_peninsula = soup_peninsula.find_all('div', { 'class': 'item' })
  noticias_peninsula = []
  for link in links_peninsula:
    link_peninsula = link.find('a').get('href')
    titulo = link.find('a', {'class':'item__link'}).text.strip()
    noticias_peninsula.append([titulo,link_peninsula])
  return noticias_peninsula

raspar_peninsula(headers, url_peninsula)

#INICIANDO AS RASPAGENS DE ECONOMIA
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
url_igarape = "https://igarape.org.br/press-releases/"

def raspar_igarape(headers, url_igarape):
    noticias_igarape = []
    response = requests.get(url_igarape, headers=headers)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    conteudo = soup.find_all('div', {'class': 'uc_post_grid_style_one_item ue_post_grid_item ue-item'})

    for item in conteudo:
        titulo_link = item.find('a', {'class': 'uc_post_grid_style_one_image'})
        if titulo_link:
            # Ajuste aqui: Buscar diretamente o 'div' com classe 'uc_post_title' dentro de 'item', não de 'titulo_link'
            div_titulo = item.find('div', class_='uc_post_title')
            if div_titulo:
                titulo = div_titulo.text.strip()
                link = titulo_link['href']
                # Verifica se o link já existe na lista para evitar duplicatas
                if not any(noticia[1] == link for noticia in noticias_igarape):
                    noticias_igarape.append([titulo, link])
    return noticias_igarape

raspar_igarape(headers, url_igarape)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

url_dara = "https://dara.org.br/informe-se/noticias/"

def raspar_dara(headers,url_dara):
  result_dara = requests.get(url_dara,  headers = headers)
  soup_dara = bs4.BeautifulSoup(result_dara.text, 'html.parser')
  links_dara = soup_dara.find_all('div', { 'class': 'category-post-conteudo' })
  noticias_dara = []
  for link in links_dara:
    link_dara = link.find('a').get('href')
    titulo = link.find('a').text.strip()
    noticias_dara.append([titulo,link_dara])
  return noticias_dara

raspar_dara(headers,url_dara)

#INICIANDO AS RASPAGENS DE ESPORTES
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
url_ee = "https://esporteeducacao.org.br/noticias/"

def raspar_ee(headers,url_ee):
  result_ee = requests.get(url_ee,  headers = headers)
  soup_ee = bs4.BeautifulSoup(result_ee.text, 'html.parser')
  links_ee = soup_ee.find_all('div', { 'class': 'uc_post_title' })
  noticias_ee = []
  for link in links_ee:
    link_ee = link.find('a').get('href')
    titulo = link.find('div', { 'class': 'ue_p_title' }).text.strip()
    noticias_ee.append([titulo,link_ee])
  return noticias_ee

raspar_ee(headers,url_ee)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
url_neymarjr = "https://institutoneymarjr.org.br/noticias/"

def raspar_neymarjr(headers, url_neymarjr):
    result_neymarjr = requests.get(url_neymarjr, headers=headers)
    soup_neymarjr = bs4.BeautifulSoup(result_neymarjr.text, 'html.parser')
    news_neymarjr = soup_neymarjr.find_all('div', {'data-elementor-type': 'jet-listing-items'})

    noticias = []
    for n in news_neymarjr:
        texto_noticia = n.text.strip()
        link = get_link(n)
        if link:
            titulo = get_title(n)
            noticias.append({"titulo": titulo, "link": link})
    return noticias

def get_title(div):
    title_element = div.find('h4', class_='elementor-post__title')
    if title_element:
        return title_element.text.strip()
    else:
        return None

def get_link(div):
    if div.get('data-url'):
        return div.get('data-url')
    
raspar_neymarjr(headers, url_neymarjr)    