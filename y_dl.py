import youtube_dl

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
args = 'home video' 
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
     song_info = ydl.extract_info(f'ytsearch:{args}', download=False,)
     print(song_info['entries'][0])