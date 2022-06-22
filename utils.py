import requests
import re
import youtube_dl
from config import ydl_opts
import discord
from config import settings

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
    
    voice = ctx.guild.voice_client

    vids_info = await get_vid_info(args, 1)

    if voice:

        audio = discord.FFmpegPCMAudio(vids_info[0]["formats"][0]["url"], executable=settings['ffmpeg'])    
        voice.play(audio)
        await ctx.send(f'Bot is playing {vids_info[0]["title"]}.')