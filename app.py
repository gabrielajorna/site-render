import os
import requests
from flask import Flask, request
import re
import unicodedata

app= Flask(__name__)
BOT_TOKEN= os.environ['TELEGRAM_BOT_TOKEN']

@app.route("/")
def index():
  return "Olá <b>Tudo bem?</b>"
  
@app.route("/teste")
def teste():
  return 'Olá essa página é um <b>teste</b>!'

#Bot do Telegram
def processa_update():
  url = f"https://api.telegram.org/bot{token}/getUpdates?offset={ultimo_id_processado + 1}"
  resposta = requests.get(url)
  dados = resposta.json()
  for update in dados["result"]:
    if "message" not in update: 
      continue

  first_name = update["message"]["from"]["first_name"]
  text = update["message"]["text"]
  def normaliza(text):
    texto = text.lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", errors="ignore").decode("ascii")
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

  texto = normaliza(text)
  chat_id = update["message"]["chat"]["id"]
  print(f"Mensagem de {first_name}: {text}")

  if texto == "/start":
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resposta = "Bem-vindo(a), eu sou o Notifiquei.bot e vou te mostrar que notícias do Terceiro Setor cabem em qualquer pauta jornalística. Vamos começar? Por favor, digite qual a editoria que você trabalha: Educação, Economia ou Esporte? "
    mensagem = {"chat_id": chat_id, "text": resposta}
    resultado = requests.post(url, data=mensagem)
    print("Resposta enviada", resultado.json())
  elif texto == 'educacao':
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resposta = "Que tal explorar essas notícias e incluir na sua próxima pauta de Educação?"
    mensagem = {"chat_id": chat_id, "text": resposta}
    resultado = requests.post(url, data=mensagem)
    print("Resposta enviada", resultado.json())
  elif texto == "economia":
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resposta = "Que tal explorar essas notícias e incluir na sua próxima pauta de Economia?"
    mensagem = {"chat_id": chat_id, "text": resposta}
    resultado = requests.post(url, data=mensagem)
    print("Resposta enviada", resultado.json())
  elif texto == "esporte":
    raspar_ee(headers,url_ee)
    raspar_gol(headers,url_gol)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resposta = f"Que tal explorar essas notícias e incluir na sua próxima pauta de Esporte?{[noticias_gol,noticias_ee]}"
    mensagem = {"chat_id": chat_id, "text": resposta}
    resultado = requests.post(url, data=mensagem)
    print("Resposta enviada", resultado.json())
  else:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resposta = "Não entendi!"
    mensagem = {"chat_id": chat_id, "text": resposta}
    resultado = requests.post(url, data=mensagem)
    print("Resposta enviada", resultado.json())
  ultimo_id_processado = update["update_id"]
print("Atualizações concluídas")

@app.route('/telegram', methods=['POST'])
def telegram_update():
  update=request.json
  url_envio_mensagem= f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
  chat_id=update['message']['chat']['id']
  mensagem= {'chat_id': chat_id, 'text':'mensagem <b>recebida</b>!', 'parse_mode':'HTML'}
  return 'ok'

