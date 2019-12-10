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

logged_in = False
getting_who = False

#for passing messages from mud -> discord
message_queue = asyncio.Queue()

client = discord.Client()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def telnet(client):
    pool = concurrent.futures.ThreadPoolExecutor()
    channel = None
    global getting_who, logged_in
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
        who_text = ""
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('Connection closed')
                    sys.exit()
                else:
                    data = data.decode('utf-8', 'backslashreplace')
                    #print(data.strip())
                    if getting_who:
                        print("Getting who in loop")
                        print(data.strip())
                        who_text = data.strip()
                        if "displayed." in data:
                            message_queue.put_nowait("```" + who_text + "```")
                            who_text = ""
                            getting_who = False
                            continue
                    if "(OOC)" in data:
                        data = data.strip()
                        user = data[1:].split(']')[0]
                        if user.lower() != mud_username.lower():
                            send_text = "**" + user + "**: " + data[data.find('"')+1:-1]
                            print("sending to discord: " + send_text)
                            message_queue.put_nowait(send_text)
                    # [CONNLOG: [60500] Radiotower [ip72-199-36-114.sd.sd.cox.net] has connected.]
                    elif "CONNLOG" in data and "has connected" in data:
                        data = data.strip()
                        user = data.split(']')[1].split('[')[0][1:-1]
                        send_text = "**" + user + "** has connected"
                        print("Connection: " + send_text)
                        message_queue.put_nowait(send_text)
                    elif not logged_in and "your handle" in data:
                        print("your handle")
                        s.send((mud_username + "\n").encode())
                    elif not logged_in and "Welcome back. Enter your password" in data:
                        s.send((mud_password + "\n").encode())
                        logged_in = True
                    elif "PRESS RETURN" in data:
                        s.send("\n".encode())
                    elif "Enter the game" in data:
                        s.send("1\n".encode())
            else :
                msg = sys.stdin.readline()
                s.send(msg.encode())

@client.event
async def on_message(message):
    global getting_who
    if message.author == client.user:
        return
    if message.channel.id != discord_channel:
        return
    if "!who" in message.content:
        getting_who = True
        print("Getting who list")
        s.send("who\n".encode())
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

