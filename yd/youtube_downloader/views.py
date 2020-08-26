from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import IndexForm
from django.urls import reverse_lazy
from pytube import YouTube
from pytube.extract import video_id
from django.http import FileResponse
import os

url = ''

# функция главной страницы
def index(request):
    return render(request, 'index.html')

# завершение загрузки
def download_complete(request, itag):
    global url
    # return render(request, 'download_complete.html', context={'res': resolution})
    # 
    # для варианта №1
    # homedir = os.path.expanduser('~')
    # dirs = homedir + '/Downloads'
    # print(f'DIRECT:', f'{dirs}/Downloads')
    # 
    if request.method == 'POST':
        # 
        # варинат №1 не работает на боевом - сохраняет файл на сервере
        # YouTube(url).streams.get_by_resolution(resolution).download(homedir+'/Downloads')
        # 
        # рабочий вариант №2 - свойство as_attachment позволяет сохранить как приложение, но предварительно сохраняет на сервере
        try:
            # return FileResponse(open(YouTube(url).streams.get_by_resolution(resolution).download(skip_existing=True),'rb'), as_attachment=True)
            return FileResponse(open(YouTube(url).streams.get_by_itag(itag).download(skip_existing=True),'rb'), as_attachment=True)
        except Exception as err:
            print(err)
            return render(request, 'sorry.html', {'err': err})
        # рабочий вариант №2 - но по itag
        # return FileResponse(open(YouTube(url).streams.get_by_itag(int(itag)).download(skip_existing=True),'rb'), as_attachment=True)
    else:
        return render(request, 'sorry.html')

# сбор информации со streams
def yt_download(request):
    global url
    url = request.GET.get('url')
    url = f'https://youtube.com/embed/{video_id(url)}'
    try:
        obj = YouTube(url)
        resolutions = []
        # только видео формат
        strm_all = obj.streams.filter(progressive=True, file_extension='mp4')

        for i in strm_all:
            resolutions.append(i.resolution)
        # 
        # способ убрать дубликаты из списка - в словарь с ключами из списка и обратно в список
        resolutions = list(dict.fromkeys(resolutions))
        # 
        embed_link = f'https://youtube.com/embed/{video_id(url)}'
        return render(request, 'yt_download.html', context={'resolutions': resolutions, 'url': url, 'embed_link': embed_link})

    except:
        return render(request, 'sorry.html')


def yt_download2(request):
    global url
    url = request.GET.get('url')
    url = f'https://youtube.com/embed/{video_id(url)}'
    try:

        obj = YouTube(url)
        
        # только видео формат
        strm_v = obj.streams.filter(progressive=True, file_extension='mp4')
        strm_v_out = {}
        strm_a_out = {}
        for v in strm_v:
            size = str(round(obj.streams.get_by_itag(v.itag).filesize_approx / (1024**2)))
            strm_v_out.update({v.itag: {'resolution': v.resolution, 'size': size}})
        print('strm_v_out', strm_v_out)
        
        # только аудио формат
        strm_a = obj.streams.filter(type='audio')
        for a in strm_a:
            size = str(round(obj.streams.get_by_itag(a.itag).filesize_approx / (1024**2)))
            strm_a_out.update({a.itag: {'format': a.mime_type, 'size': size}})
        print('strm_a_out', strm_a_out)

        # 
        # способ убрать дубликаты из списка - в словарь с ключами из списка и обратно в список
        # resolutions = list(dict.fromkeys(resolutions))
        # 
        embed_link = f'https://youtube.com/embed/{video_id(url)}'
        return render(request, 'yt_download2.html', context={'strm_v_out': strm_v_out, 'strm_a_out': strm_a_out, 'url': url, 'embed_link': embed_link})

    except Exception as err:
        print(err)
        return render(request, 'sorry.html', {'err': err})


# def get_stream(url):
#     yt = YouTube(url).streams
#     return yt


# class GetVideo(FormView):
#     template_name = 'index.html'
#     form_class = IndexForm
#     success_url = reverse_lazy('index')

