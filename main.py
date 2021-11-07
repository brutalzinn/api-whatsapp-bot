from flask import Flask, request, jsonify
from whatsappService import EnviarMensagemWhatsapp
app = Flask(__name__)
@app.route('/EnviarMensagem', methods=['POST'])
#string mensagem
#int numerodecelular
def EnviarMensagem():
    data = request.json
    EnviarMensagemWhatsapp(data["numero"],data["mensagem"])
    return 200

if __name__ == '__main__':
    app.run()

