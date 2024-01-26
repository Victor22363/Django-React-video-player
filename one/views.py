from django.shortcuts import render
from django.http import HttpResponse
import os, subprocess
from .models import *
# Create your views here.


def hlsConfig(id, path):
    subprocess.call(f"mkdir static/{id}")
    subprocess.call(f"ffmpeg -i \"{path}\" -c:a aac -b:a 128k -c:v libx264 -crf 18 -flags -global_header -map 0 -f segment -segment_time 10 -segment_list \"{path}\{id}\playlist.m3u8\" -segment_format mpegts -c:s:0 copy \"{path}\{id}\segment_%05d.ts\"")

    


def home(request):
    dictionary = {}
    shows_list = Show.objects.all()
    shows = [element.name for element in shows_list]

    first_ep = Video.objects.filter(epNum=1)
    list = [element.id for element in first_ep]

    for i in range(len(shows)):
        dictionary[shows[i]] = list[i]

    return render(request, 'catalog.html', {
        "dictionary":dictionary,
    })
    


def watch(request, episode_id):
    # using the ep_id to get to the show and season
    episode = Video.objects.filter(pk=int(episode_id)).first()
    show_num = episode.show.name
    season_num = episode.season

    #get a list with every episode of this season of the show
    episode_list = Video.objects.filter(show=episode.show.id, season=season_num).order_by("epNum")
    list = [element.id for element in episode_list]
    id = episode_id
    #get the video url for the video
    video_url = episode.file.url
    
    return render(request, 'watch.html', {
        "video":video_url,
        "list":list,
        "ep_number":episode_list,

        "ep":episode,
        "sh":show_num,
        "se":season_num,
        "id": id,
    })