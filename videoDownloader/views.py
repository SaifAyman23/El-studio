from pathlib import Path
from django.shortcuts import render,redirect
from pytube import YouTube
from .models import Video,Audio
import os                               
from moviepy.editor import *
import eyed3
import urllib.request 
# your views here.

# main startup page

def page(request):
    return render(request,'apps/about.html',{'page_image':'img/Screenshot (614).png'})

# download page
    
def download(request):
    downloads_path = str(Path.home() / "Downloads")
    if request.method=='POST':
        url=request.POST['url']
        res=request.POST['res']
        yt = YouTube(url)
        author=yt.author
        title=yt.title.replace('|','')
        title=yt.title.replace('-','')
        title=yt.title.replace('?','')
        
        # to check if the object is downloaded, if not then skip
        
        try:
            item=Video.objects.all().filter(url=url,res=res).count()
            yt_image=YouTube(url).thumbnail_url
            if res=='audio':
                item=Audio.objects.get(title=title,author=author)
            context={
                'item':item,
                'image':yt_image,
                'image':yt.thumbnail_url,
                'title':title,
                'author':author,
            }
            return render(request,'apps/download.html',context)
        except:
        
        # if not downloaded
        
            if res=='highest':
                stream=yt.streams.get_highest_resolution().download(downloads_path,filename=f'{title}.mp4')
                downloadedVideo=Video(title=title,author=author,url=url,res=res)
                downloadedVideo.save()
                
            elif res=='audio':
                stream=yt.streams.get_audio_only()
                stream.download(downloads_path,filename=f'{title}.mp4')
                file = AudioFileClip(f'{downloads_path}/{title}.mp4')
                audioFile = f'{downloads_path}/{title}.mp3'
                file.write_audiofile(audioFile)
                file.close()
                audio = eyed3.load(f'{downloads_path}/{title}.mp3')
                audio.tag.artist = f"{author}"
                urllib.request.urlretrieve(yt.thumbnail_url, f"{title}.png") 
                imagedata = open(f"{title}.png","rb").read()
                audio.tag.images.set(3,imagedata,"image/jpeg",u"you can put a description here")
                audio.tag.save()
                downloadedAudio=Audio(title=title,length=yt.length,author=author,image=yt.thumbnail_url)
                downloadedAudio.save()
                os.remove(f'{downloads_path}/{title}.mp4')
                os.remove(f'{title}.png')
                downloadedVideo=Video(title=title,author=author,url=url,res=res)
                downloadedVideo.save()
                
            else:
                stream=yt.streams.get_by_resolution(resolution=f'{res}')
                stream.download(downloads_path,filename=f'{title}.mp4')
                downloadedVideo=Video(title=title,author=author,url=url,res=res)
                downloadedVideo.save()
    context={
        'image':yt.thumbnail_url,
        'title':title,
        'author':author,
    }
    return render(request,'apps/download.html',context)
                
                
                