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
from gtts import gTTS
import string
import logging

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

SOUNDS = 'trim'
MODE = 'fry'
debug = 0

TOKEN = open("credentials.env","r").readline()
#TODO: exit on token load fail

if (TOKEN is None or len(TOKEN)==0):
    print('cloud not load discord token')
    exit

#Set up array to store list of connected clients on the Button website
clientList = []
#Load array of buzz in noise sounds
soundList = os.listdir(SOUNDS)

print('noise list = ', soundList)

prefix = '$shout '

modes = ['fry','paxman']

soundMap = {}

mp3List = []

client = commands.Bot(command_prefix=prefix, intents=intents)
#824575380006502400 robot wars
async def hello(request):    
    sessionId = request.rel_url.query['id']

    disconnected = request.rel_url.query['disconnect']
    if (disconnected=='true'):
        print('received disconnection event for ' + sessionId)
        if (sessionId in clientList):
            clientList.remove(sessionId)
            soundList.append(soundMap.get(sessionId))
            print(' added ' + soundMap.get(sessionId)+' back to sound list')
            del soundMap[sessionId]
            print(' unused noises:',len(soundList))
            return web.Response(body='removed client from list',status=200)
    else:
        typedName = request.rel_url.query['name']
        #Anti-Mikey feature
        typedName = typedName.translate(str.maketrans('', '', string.punctuation))
        #another anti-Mikey feature
        if (len(typedName) > 30):
            typedName=typedName[0:30]
        if (len(typedName)==0):
            typedName='Clint Eastwood'
        if(typedName.lower()=='acres greg'):
            typedName='CURIOUS GEORGE'
        
        if (sessionId not in clientList):
            clientList.append(sessionId)
            #get random sound from list
            index = random.randint(0, len(soundList)-1)
            playfile = soundList[index]        
            soundMap.update({sessionId:playfile})
            soundList.pop(index)

        playfile=soundMap.get(sessionId)    
        print(sessionId+' = '+ 'is pretending to be \'' + typedName+'\' is getting file ' + playfile)    
        print(' unused noises:',len(soundList))

        voice = get(client.voice_clients)
        
        if (voice is not None):
            #TODO: mute all other users in voice channel
            print(' MODE:'+MODE)
            if (MODE == 'paxman'):
                mp3FileName = typedName+'.mp3'
                if (not os.path.isfile(mp3FileName)):
                    tts = gTTS(typedName)                
                    tts.save(mp3FileName)

                mp3List.append(mp3FileName)
                if (not voice.is_playing()):
                    voice.play(discord.FFmpegPCMAudio(mp3FileName))
            else:
                if (not voice.is_playing()):
                    voice.play(discord.FFmpegPCMAudio(SOUNDS+"/"+playfile))                          
            playSeconds = 0
            while voice.is_playing():
                print('playing ', playSeconds)
                playSeconds = playSeconds+1
                await asyncio.sleep(1)
            return web.Response(text=playfile,status=200)
        else:
            helpString = 'Bot active, but connected to a voice channel. Type  \'$shout help\' in discord'
            return web.Response(body=helpString,status=500)       

app = web.Application()

app.add_routes([web.get('/', hello)])

channels = client.get_all_channels()
@client.event
async def on_ready():
    print('discord connection established, voice channel list=')
    channels = client.get_all_channels()
    for channel in channels:
        if (isinstance(channel, discord.VoiceChannel)):            
            print (channel.name+" " ,channel.id)
            
    
    #TODO: reconnect to a voice channel if I'm already there
    #await get(client.voice_clients).channel.connect()


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
    
@client.event
async def on_voice_state_update(member, before, after):
    #what channel am I connected to?    
    voice = get(client.voice_clients)
    if (voice is not None):
        channel = voice.channel
        print('I am connected to ', channel.id)
        print('channel has ', len(channel.members))
        #if the channel only has 1 member, assume it's me and disconnect
        if (len(channel.members)==1):
            await voice.disconnect()
            print('cleaning up temp files:')
            for mp3File in mp3List:
                print('     '+mp3File)
                os.remove(mp3File)


            
@client.command(name='paxman', help='Add shouty bot to your current channel, in Jeremy Paxman mode')
async def join_voice(ctx):
    global MODE
    MODE = 'paxman'
    print('MODE='+MODE)
    if (ctx.author.voice is not None):        
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send('You need to be in a voice channel!')

@client.command(name='disconnect', help='forcibly disconnect the shoutybot from it\'s current channel')
async def join_voice(ctx):
    voice = get(client.voice_clients)
    if (voice is not None):
        await voice.disconnect()


@client.command(name='fry', help='Add shouty bot in your current channel, in Pub Quiz / Stephen Fry mode')
async def join_voice(ctx):    
    global MODE
    MODE = 'fry'
    print('MODE='+MODE)
    if (ctx.author.voice is not None):        
        await ctx.author.voice.channel.connect()      
    else:
        await ctx.send('You need to be in a voice channel!')          

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





