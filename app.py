from flask import Flask

app= Flask(__name__)

@app.route("/")
def index():
  return "Olá <b>Tudo bem?</b>"
  
@app.route("/teste")
def teste():
  return 'Olá essa página é um <b>teste</b>!'

