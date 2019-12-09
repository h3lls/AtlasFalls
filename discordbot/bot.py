# bot.py
import socket, select, string, sys
import os
import threading
import time
import re
import asyncio, concurrent.futures

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
discord_channel = int(os.getenv('DISCORD_CHANNEL'))
mud_username = os.getenv('MUD_USERNAME')
mud_password = os.getenv('MUD_PASSWORD')
mud_host = os.getenv('MUD_HOST')
mud_port = int(os.getenv('MUD_PORT'))

#for passing messages from mud -> discord
message_queue = asyncio.Queue()

client = discord.Client()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def telnet(client):
    pool = concurrent.futures.ThreadPoolExecutor()
    channel = None
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((mud_host, mud_port))
    except :
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host')

    while 1:
        time.sleep(1)
        socket_list = [sys.stdin, s]
        
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('Connection closed')
                    sys.exit()
                else:
                    data = data.decode('utf-8', 'backslashreplace')
                    # This is clearly unsafe.. I know this... it's fine... just fine
                    if "your handle" in data:
                        print("your handle")
                        s.send((mud_username + "\n").encode())
                    elif "Welcome back. Enter your password" in data:
                        s.send((mud_password + "\n").encode())
                    elif "PRESS RETURN" in data:
                        s.send("\n".encode())
                    elif "Enter the game" in data:
                        s.send("1\n".encode())
                    elif "(OOC)" in data:
                        data = data.strip()
                        user = data[1:].split(']')[0]
                        if user.lower() != mud_username.lower():
                            send_text = "**" + user + "**: " + data[data.find('"')+1:-1]
                            print("sending to discord: " + send_text)
                            message_queue.put_nowait(send_text)
            else :
                msg = sys.stdin.readline()
                s.send(msg.encode())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id != discord_channel:
        return
    send_text = "ooc Discord: " + message.author.display_name + " says " + message.content + "\n"
    print("sending to mud: " + send_text)
    s.send(send_text.encode())
    # message.content
    # message.author.display_name

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(discord_channel)
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
    while True:
        time.sleep(1)
        message = await message_queue.get()
        try:
            await channel.send(message)
        except:
            print("error")

x = threading.Thread(target=telnet, args=(client,))
x.start()

client.run(token)

