# Meu site no ar
Neste repositório você pode conferir o conteúdo do Trabalho Final do Master em Jornalismo de Dados, Automação e Data Storytelling do Insper que contém:

- Site em Flask
- Chat bot do Telegram;

## Objetivo do projeto: 

Criar um chatbot que suprisse uma necessidade do Terceiro Setor em ter mais pautas jornalísticas sobre o tema. 

O bot executa algumas funções:

- Web Scraping de 2 instituições para cada editoria escolhida (Educação, Economia e Esporte) 
- Transforma o título e link em um conteúdo HTML e devolve em forma de mensagem ao usuário

## Tecnologias utilizadas
- Flask: Utilizado para construir o servidor web que se comunica com a API do Telegram.
- API do Telegram: Utilizada para receber e enviar mensagens para os usuários.
- API Google Sheets: Utilizada para armazenar os chat_id de usuários bem como as respostas enviadas.

## Próximos passos
- Melhoria do chatbot com inclusão de novas editorias jornalísitcas;
- Abertura de canal para instituições que quiserem fazer parte da lista, incluirem seus sites. 
