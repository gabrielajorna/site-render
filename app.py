import os
import requests
import bs4
from flask import Flask, request
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()
import scraping
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN= os.environ['BOT_TOKEN']

#INTEGRAÇÃO COM WEBHOOK
url = "https://site-render-3c9r.onrender.com/telegram"
dados = {"url": url,'description':'teste'}
resposta = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook", data=dados)
print(resposta.json())

#INTEGRAÇÃO COM GOOGLE SHEETS
conteudo_credenciais = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
arquivo_credenciais = "credenciais-google.json"
  
conta = ServiceAccountCredentials.from_json_keyfile_name(arquivo_credenciais)#nome do json 
api = gspread.authorize(conta)
planilha = api.open_by_key("1-JGRKA-HX_vFHZB3aQJJq9cGnaOdfZbMMA8eg1qR7NY")
sheet = planilha.worksheet("Página2")

app= Flask(__name__)

#FORMATANDO AS NOTÍCIAS RASPADAS PARA HTML 
def formata_noticias(titulo, noticias):
    html = f"<b>Que tal incluir essas notícias na sua editoria de {titulo}? </b>\n\n"
    for noticia in noticias:
        # Certifique-se de que noticia é um dicionário
        if isinstance(noticia, dict) and "titulo" in noticia and "url" in noticia:
            html += f'- <a href="{noticia["url"]}">{noticia["titulo"]}</a>\n'
    return html

#INICIANDO AS PÁGINAS DO SITE
@app.route("/")
def index():
  return "Olá <b>Tudo bem?</b>"

@app.route('/telegram', methods=['POST'])

def telegram_update():
    # Definindo todos os headers e urls das funções que serão chamadas nesta página
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url_insper = "https://www.insper.edu.br/imprensa/"
    url_peninsula = "https://www.institutopeninsula.org.br/noticias/"
    url_igarape = "https://igarape.org.br/press-releases/"
    url_dara = "https://dara.org.br/informe-se/noticias/"
    url_ee = "https://esporteeducacao.org.br/noticias/"
    url_neymarjr = "https://institutoneymarjr.org.br/noticias/"

    ultimo_id_processado = int(sheet.get("A1")[0][0])
    print(f"Começando a partir do update_id = {ultimo_id_processado}")

    # Definindo uma resposta padrão
    resposta = None

    # Verificando se há dados JSON na solicitação
    if request.is_json:
        update = request.json
        url_envio_mensagem = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        chat_id = update['message']['chat']['id']
        first_name = update["message"]["from"]["first_name"]
        texto = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        print(f"Mensagem de {first_name}: {texto}")

        if texto == "/start":
            resposta = "Olá, eu sou o Notifiquei.bot e vou te mostrar que notícias do Terceiro Setor cabem em qualquer pauta jornalística. Sou programado para enviar pautas semanalmente, basta você escolher uma das editorias a seguir que te mandarei imediatamente algumas opções de organizações e seus trabalhos sociais. Toda terça-feira tem conteúdo fresquinho por aqui, volte sempre! Vamos começar? Escolha uma das editorias que gostaria de acompanhar: /educacao, /economia, /esporte."
        elif texto == '/educacao':
            materias_insper = scraping.raspar_insper(headers, url_insper)
            materias_peninsula = scraping.raspar_peninsula(headers, url_peninsula)
            materias_educacao = materias_insper + materias_peninsula
            print("Materias Educação:", materias_educacao)  # Adicionado para depuração
            resposta = formata_noticias("Educação", materias_educacao)
            print(resposta)
        elif texto == '/economia':
            materias_dara = scraping.raspar_dara(headers, url_dara)
            materias_igarape = scraping.raspar_igarape(headers, url_igarape)
            materias_economia = materias_dara + materias_igarape
            print("Materias Economia:", materias_economia)  # Adicionado para depuração
            resposta = formata_noticias("Economia", materias_economia)
            print(texto)
        elif texto == '/esporte':
            materias_ee = scraping.raspar_ee(headers, url_ee)
            materias_neymarjr = scraping.raspar_neymarjr(headers, url_neymarjr)
            materias_esporte = materias_ee + materias_neymarjr
            print("Materias Esporte:", materias_esporte)  # Adicionado para depuração
            resposta = formata_noticias("Esportes", materias_esporte)
            print(texto)
        
        mensagem={"chat_id": chat_id, "text": resposta, 'parse_mode': 'HTML'}
        #requests.post(url_envio_mensagem, data=mensagem)

    else:
        # Caso a solicitação não seja JSON
        resposta = "A solicitação não contém dados JSON ou não corresponde a nenhum caso esperado."
        return jsonify({"mensagem": resposta}), 400  # Retorna uma resposta de erro com status 400

    # Retornar a resposta, independentemente do texto recebido
    return requests.post(url_envio_mensagem, data=mensagem)

def adicionar_na_planilha(chat_id, texto):
    planilha.append_row([chat_id, texto])
    print('Mensagem armazenada com sucesso!')
    