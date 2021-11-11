import random
import os
from enum import Enum, auto
import redis
from telethon.sessions import StringSession
from time import sleep
import asyncio
from telethon import TelegramClient, events
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
token = os.getenv("TOKEN")
phone =  os.getenv("NUMERO")
r = redis.Redis(host='localhost',password='SUASENHA', port=6379, db=0)

bot = TelegramClient('Bot', api_id, api_hash)

# We use a Python Enum for the state because it's a clean and easy way to do it
class State(Enum):
    WAIT_EMAIL = auto()
    WAIT_TOKEN = auto()

# The state in which different users are, {user_id: state}
conversation_state = {}
@bot.on(events.NewMessage(pattern='(?i)hi|hello|start|login'))
async def starthandle(event):
    await bot.send_message(event.chat, 'Olá. Bem vindo ao sistema de login da api ja cheguei mae.')
    await bot.send_message(event.chat, 'Esse é um ambiente de testes. Não use sua conta original.')
@bot.on(events.NewMessage)
async def handler(event):
    email = ''
    code = ''
    who = event.sender_id
    state = conversation_state.get(who)
    client = TelegramClient(StringSession(), api_id, api_hash)
    if state is None:
        await bot.send_message(event.chat, 'Olá. Bem vindo ao sistema de login da api ja cheguei mae.')
        await bot.send_message(event.chat, 'Esse é um ambiente de testes. Não use sua conta original.')
        await event.respond('Olá! Qual é seu email?')
        conversation_state[who] = State.WAIT_EMAIL
    
    elif state == State.WAIT_EMAIL:
        conversation_state[email] = event.text  
        await event.respond('Qual é a chave enviada pelo telegram?')  
        await client.connect()
        await client.send_code_request(phone)
        conversation_state[who] = State.WAIT_TOKEN
        
    elif state == State.WAIT_TOKEN:
        conversation_state[code] = event.text  
        await event.respond(f'Obrigado, adicionei sua chave no banco de dados. {code}')
        try:
            await client.sign_in(phone, conversation_state[code]) 
        except Exception:
            await event.respond(f'Código informado inválido. {code}')
        r.set(conversation_state[email],client.session.save())
        sleep(900)
        await client.disconnect()
        del conversation_state[who]




async def parseurls():
    while True:
        ts = abs(int(random.random()*10))
        print(f'parseurls({ts})')
        await sendmsg(ts)
        await asyncio.sleep(ts)


async def sendmsg(msg):
    print(f'sendmsg({msg}) - start')
    channel = await bot.get_entity('https://t.me/bobertobot')
    await bot.send_message(channel, f'ответ из другого потока {msg}')
    print(f'sendmsg({msg}) - done')


def main():
    bot.start(bot_token=token)
    loop = asyncio.get_event_loop()
    tasks = [
        #loop.create_task(parseurls()),
        loop.create_task(bot.run_until_disconnected()),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == '__main__':
    main()