from http import client
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl

from config import settings

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

Client = commands.Bot(command_prefix = settings['prefix'])
voice = None

@Client.command()
async def hello(ctx):
    author = ctx.message.author

    #await ctx.send(f'Hello, {author.mention}!')
    await author.create_dm()
    await author.dm_channel.send("hi")

async def join_channel(ctx):

    global voice
    
    user_voice = ctx.author.voice
    voice = ctx.guild.voice_client

    if user_voice == None:
        await ctx.send('Join a channel to summon a bot.')
    else:
        if voice and voice.is_connected():
            await voice.move_to(user_voice.channel)
        else:  
            voice = await user_voice.channel.connect()


@Client.command()
async def join(ctx):
    
    await join_channel(ctx)

@Client.command()
async def leave(ctx):

    await ctx.guild.change_voice_state(channel=None)

@Client.command()
async def play(ctx):
    
    await join_channel(ctx)
    
    if voice:

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            song_info = ydl.extract_info("https://www.youtube.com/watch?v=uwiTs60VoTM", download=False)
            
        voice.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"]))


Client.run(settings['token'])