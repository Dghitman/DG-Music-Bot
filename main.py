from pickle import NONE
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import re
import requests

from config import settings, ydl_opts

queue = dict()
track_n = dict()

Client = commands.Bot(command_prefix = settings['prefix'])
VoiceClient = dict()

############################
# FUNCTIONS
############################

async def add_to_queue(guild, vid_info):
    global queue
    if queue[guild.id] == None:
        queue[guild.id] = list()

    queue[guild.id].append(vid_info)

async def join_channel(ctx):

    user_voice = ctx.author.voice
    voice = ctx.guild.voice_client

    if user_voice == None:

        await ctx.send('Join a channel to summon a bot.')
    
    else:

        if voice and voice.is_connected():
            
            if voice.channel == user_voice.channel:

                ctx.send("You are already in the same channel.")

            else:

                await voice.move_to(user_voice.channel)
        
        else:  
            
            await user_voice.channel.connect()

    return voice

async def get_vid_info(query, vid_num=5):

    if query == ():

        return None

    try:
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            vid_info = ydl.extract_info(query[0], download=False)
        
        return [vid_info]
    
    except:

        response = requests.get(f"https://www.youtube.com/results?search_query={'+'.join(query)}")
        video_ids = re.findall(r"watch\?v=(\S{11})", response.text)[:vid_num]
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            vid_info_list = []
            for vid_id in video_ids:
                vid_info = ydl.extract_info('https://www.youtube.com/results?v=' + vid_id, download=False)
                vid_info_list.append(vid_info)
        
        return vid_info_list

async def start_playing(ctx, args):
    
    global track_n
    global queue

    guild = ctx.guild

    voice = guild.voice_client
    
    vid_info = queue[guild.id][track_n[guild.id]]

    if voice:

        audio = discord.FFmpegPCMAudio(vid_info["formats"][0]["url"], executable=settings['ffmpeg'])    
        voice.play(audio, start_playing)
        await ctx.send(f'Bot is playing {vid_info["title"]}.')
############################
# COMMANDS
############################

@Client.command()
async def join(ctx):
    global VoiceClient

    VoiceClient[ctx.guild.id] = await join_channel(ctx)

@Client.command()
async def leave(ctx):

    await ctx.guild.change_voice_state(channel=None)   

@Client.command()
async def play(ctx, *args):
    
    await join_channel(ctx)

    if args != ():
        vid_info = await get_vid_info(args, 1)
        await add_to_queue(ctx.guild, vid_info[0])

    if track_n[ctx.guild.id] == None:
        track_n[ctx.guild.id] = 0    
    voice = ctx.guild.voice_client

    if voice:

        audio = discord.FFmpegPCMAudio(vids_info[0]["formats"][0]["url"], executable=settings['ffmpeg'])    
        voice.play(audio)
        await ctx.send(f'Bot is playing {vids_info[0]["title"]}.')

@Client.command()
async def pause(ctx):

    voice = ctx.guild.voice_client
    
    if voice == None:
        await ctx.send('Bot is not in a voice channel.')
        return

    if voice.is_playing():

        voice.pause()
        await ctx.send('Bot is paused.')
    
    else:
        await ctx.send('Bot is not playing anything at the moment.')

@Client.command()
async def resume(ctx):

    voice = ctx.guild.voice_client
    
    if voice == None:
        await ctx.send('Bot is not in a voice channel.')
        return

    if voice.is_paused():

        voice.resume()
        await ctx.send('Bot is playing.')
    
    else:
        await ctx.send('Bot is not paused.')

############################
# EVENTS
############################

@Client.event
async def on_voice_state_update(member, before, after):
    global queue
    
    if member == Client.user:
        if after.channel == None:
            
            queue[before.channel.guild.id] = None
            return

        if before.channel == None:

            queue[after.channel.guild.id] = []
            return
        

Client.run(settings['token'])