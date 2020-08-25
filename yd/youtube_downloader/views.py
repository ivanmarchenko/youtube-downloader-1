from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import IndexForm
from django.urls import reverse_lazy
from pytube import YouTube
from pytube.extract import video_id
from django.http import FileResponse
import os

url = ''

def index(request):
    return render(request, 'index.html')

def download_complete(request, resolution):
    global url
    # print('global url:', url)
    # return render(request, 'download_complete.html', context={'res': resolution})
    homedir = os.path.expanduser('~')
    dirs = homedir + '/Downloads'
    print(f'DIRECT:', f'{dirs}/Downloads')
    if request.method == 'POST':
        # YouTube(url).streams.get_by_resolution(resolution).download(homedir+'/Downloads')
        return FileResponse(open(YouTube(url).streams.get_by_resolution(resolution).download(skip_existing=True),'rb'), as_attachment=True)
    else:
        return render(request, 'sorry.html')

def yt_download(request):
    global url
    url = request.GET.get('url')
    url = f'https://youtube.com/embed/{video_id(url)}'
    try:
        obj = YouTube(url)
        resolutions = []
        strm_all = obj.streams.filter(progressive=True, file_extension='mp4')
        for i in strm_all:
            resolutions.append(i.resolution)
        # способ убрать дубликаты из списка - в словарь с ключами из списка и обратно в список
        resolutions = list(dict.fromkeys(resolutions))
        embed_link = f'https://youtube.com/embed/{video_id(url)}'
        return render(request, 'yt_download.html', context={'resolutions': resolutions, 'url': url, 'embed_link': embed_link})

    except:
        return render(request, 'sorry.html')


def get_stream(url):
    yt = YouTube(url).streams
    return yt


class GetVideo(FormView):
    template_name = 'index.html'
    form_class = IndexForm
    success_url = reverse_lazy('index')

