import urllib.request
import re

html = urllib.request.urlopen("https://www.youtube.com/results?search_query=mozart")
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
print(video_ids)