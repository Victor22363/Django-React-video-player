'''
from django.shortcuts import render
from django.http import HttpResponse
import os, subprocess
from .models import *
# Create your views here.
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
        "ep_list":episode_list,
        "id": id,
    })

'''