import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio
import aiohttp
from aiohttp import web
from threading import Thread
from discord.utils import get
import os
import random

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

SOUNDS = 'trim'

debug = 1
TOKEN = open("credentials.env","r").readline()

clientList = []

soundList = []
soundList = os.listdir(SOUNDS)

print('noise list = ', soundList)

soundMap = {}

client = commands.Bot(command_prefix='$derp', intents=intents)
#824575380006502400 robot wars
async def hello(request):
    #channel = client.get_channel(824575380006502400)
    #channels = client.get_all_channels()
    #for channel in channels:
    #    print(channel.name+"= ",  channel.id)
    #
    sessionId = request.rel_url.query['id']
    #typedName = request.rel_url.query['name']
    #TODO: Add the typed name as a parameter, check for null values
    print('param='+sessionId)
    if (sessionId not in clientList):
        clientList.append(sessionId)
        index = random.randint(0, len(soundList)-1)
        playfile = SOUNDS+"/"+soundList[index]        
        soundMap.update({sessionId:playfile})
        soundList.pop(index)

    playfile=soundMap.get(sessionId)

    #print('soundMap=',soundMap)
    
    print(sessionId+' = ' + playfile)
    #print('session list = ', clientList)
    
    print(' unused noises:',len(soundList))




    #check if already connected to voice channel
    
    #await channel.connect()
    voice = get(client.voice_clients)
    
    if (voice is not None):
        #TODO: mute all other users in voice channel
        voice.play(discord.FFmpegPCMAudio(playfile))
        while voice.is_playing():
            print('playing')
            await asyncio.sleep(1)
        #await voice.disconnect()
        #print('done playing, disconnected voice')
        return web.Response(text=playfile)
    else:
        return web.Response(text='bot not connected to voice channel')

app = web.Application()

app.add_routes([web.get('/', hello)])

channels = client.get_all_channels()
@client.event
async def on_ready():
    print('connected')
    #channels = client.get_all_channels()
    #for channel in channels:
    #    print (channel.name+" " ,channel.id)

"""
@client.event
async def on_voice_state_update(member, before, after):
    if debug == 1:
        if member.name != 'shoutybot' and isinstance(after, discord.VoiceState):
            print(member.name + ' either joined or left')
            if isinstance(after.channel, discord.VoiceChannel) and after.channel.id == 824575380006502400: 
                #need to add check if bot is already in this channel                 
                await client.get_channel(824575380006502400).connect()     
                voice = get(client.voice_clients)
                voice.play(discord.FFmpegPCMAudio("/home/iain/git/shoutybot/shout.mp3"), after=print('done'))
                while voice.is_playing():
                    print('playing')
                    await asyncio.sleep(1)
                await voice.disconnect()
"""
    
    
            
@client.command(name='paxman', help='Paxman?')
async def join_voice(ctx):
    #print('joining voice channel I hope')
    #channel = ctx.author.voice.channel    
    #print('author is in voice channel = ', ctx.author.voice.channel)
    #channels = ctx.author.voice
    if (ctx.author.voice is not None):
        await ctx.author.voice.channel.connect()

@client.event
async def on_message(message):
    chat_message = message.content.lower()
    await client.process_commands(message)




async def start_discord(app):
    print('start disco')
    


loop = asyncio.get_event_loop()
loop.create_task(client.start(TOKEN))
Thread(target=loop.run_forever)
web.run_app(app)





