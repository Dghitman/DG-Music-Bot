settings = {
    'token': 'OTYyNDM0MDAxMTYxODMwNDIw.YlHegw.4f5uDSOv78_VkH9_aUmyhPrJ8G8',
    'bot': 'DG Music Bot',
    'id': 962434001161830420,
    'prefix': '!',
    'ffmpeg': "D:\\Documents\\VS Code Files\\ffmpeg\\ffmpeg.exe"
    }

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }