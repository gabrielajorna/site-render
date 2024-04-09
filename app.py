import os
import requests
import bs4
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
import scraping
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN= os.environ['TELEGRAM_BOT_TOKEN']

#INTEGRAÇÃO COM WEBHOOK
url = "https://site-render-3c9r.onrender.com"
dados = {"url": url,'description':'teste'}
resposta = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook", data=dados)
print(resposta.json())

#INTEGRAÇÃO COM GOOGLE SHEETS
conteudo_credenciais = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
arquivo_credenciais = "algoritmo-aula01-822d22859c10.json"
with open(arquivo_credenciais, mode="w") as arquivo:
  arquivo.write(conteudo_credenciais)
  conta = ServiceAccountCredentials.from_json_keyfile_name(arquivo_credenciais)
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1-JGRKA-HX_vFHZB3aQJJq9cGnaOdfZbMMA8eg1qR7NY")
  sheet = planilha.worksheet("Página2")

app= Flask(__name__)

#FORMATANDO AS NOTÍCIAS RASPADAS PARA HTML 
def formata_noticias(editoria, noticias):
  html = f"Que tal incluir essas notícias na sua próxima pauta de {editoria}:\n\n"
  for materia in noticias:
    html += f'- <a href="{materia["url"]}">{materia["titulo"]}</a>\n'
  return html

#INICIANDO AS PÁGINAS DO SITE
@app.route("/")
def index():
  return "Olá <b>Tudo bem?</b>"

@app.route('/telegram', methods=['POST'])
def telegram_update(request):
    # Definindo todos os headers e urls das funções que serão chamadas nesta página
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url_insper = "https://www.insper.edu.br/imprensa/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url_peninsula = "https://www.institutopeninsula.org.br/noticias/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url_igarape = "https://igarape.org.br/press-releases/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url_dara = "https://dara.org.br/informe-se/noticias/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url_ee = "https://esporteeducacao.org.br/noticias/"

    ultimo_id_processado = int(sheet.get("A1")[0][0])
    print(f"Começando a partir do update_id = {ultimo_id_processado}")
    update = request.json
    url_envio_mensagem = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    chat_id = update['message']['chat']['id']
    mensagem = {"chat_id": chat_id, "text": resposta, 'parse_mode': 'HTML'}
    requests.post(url_envio_mensagem, data=mensagem)

    for update in dados["result"]:
        if "message" not in update:  # Não é uma mensagem, pula
            continue
        if update["update_id"] <= ultimo_id_processado:
            print(f"Pulando atualização {update['update_id']} - já processada")
            continue  # Pula para próximo update caso seja igual

        first_name = update["message"]["from"]["first_name"]
        texto = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        print(f"Mensagem de {first_name}: {texto}")

        if texto == "/start":
            resposta = "Bem-vindo(a), eu sou o Notifiquei.bot e vou te mostrar que notícias do Terceiro Setor cabem em qualquer pauta jornalística. Vamos começar? Escolha uma das editorias: /educacao, /economia, /esporte "
        elif texto == '/educacao':
            materias_insper = scraping.raspar_insper(headers, url_insper)
            materias_peninsula = scraping.raspar_peninsula(headers, url_peninsula)
            resposta = formata_noticias("Educação", materias_insper + materias_peninsula)
            print(texto)
        elif texto == '/economia':
            materias_dara = scraping.raspar_dara(headers, url_dara)
            materias_igarape = scraping.raspar_igarape(headers, url_igarape)
            resposta = formata_noticias("Economia", materias_dara + materias_igarape)
            print(texto)
        elif texto == '/esporte':
            materias_ee = scraping.raspar_ee(headers, url_ee)
            resposta = formata_noticias("Esportes", materias_ee)
            print(texto)
        mensagem = {"chat_id": chat_id, "text": resposta, 'parse_mode': 'HTML'}
        requests.post(url_envio_mensagem, data=mensagem)
        return "ok"  # Retornar algo como ok ao final da função

def adicionar_na_planilha(chat_id, texto):
    planilha.append_row([chat_id, texto])
    print('Mensagem armazenada com sucesso!')
    