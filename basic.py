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

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

TOKEN = os.getenv('TOKEN')
debug = 1


client = commands.Bot(command_prefix='$derp', intents=intents)
#824575380006502400 robot wars
async def hello(request):
    channel = client.get_channel(824575380006502400)
    #channels = client.get_all_channels()
    #for channel in channels:
    #    print(channel.name+"= ",  channel.id)
    #
    
    await channel.connect()
    voice = get(client.voice_clients)
    voice.play(discord.FFmpegPCMAudio("/home/iain/git/shoutybot/shout.mp3"))
    return web.Response(text="Hello, world")

app = web.Application()
app.add_routes([web.get('/', hello)])
channels = client.get_all_channels()
@client.event
async def on_ready():
    print('connected')
    #channels = client.get_all_channels()
    #for channel in channels:
    #    print (channel.name+" " ,channel.id)
    
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

    
    
            
@client.command(name='paxman', help='Paxman?')
async def join_voice(ctx):
    print('joining voice channel I hope')
    channel = ctx.author.voice.channel    
    print(ctx.author.id)
    await channel.connect()

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




