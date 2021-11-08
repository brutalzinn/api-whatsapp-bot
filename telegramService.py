import os
from telethon import TelegramClient

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
token = os.getenv("TOKEN")
phone =  os.getenv("NUMERO")
async def TelegramEnviarMensagem(numero: str, mensagem: str):
    client = TelegramClient('session', api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: ')) 
    try:
        await client.send_message(numero, mensagem, parse_mode='html')
    except Exception as e:
        print(e)
    await client.disconnect()