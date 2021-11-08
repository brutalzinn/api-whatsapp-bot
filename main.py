from flask import Flask, request,Response
import asyncio

from telegramService import TelegramEnviarMensagem
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
@app.route('/EnviarMensagem', methods=['POST'])
def EnviarMensagem():
    data = request.json  
    asyncio.run(TelegramEnviarMensagem(data['numero'], data['mensagem']))
    return Response(status=200)

if __name__ == '__main__':
    app.run()

