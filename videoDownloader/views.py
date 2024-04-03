from pathlib import Path
from django.shortcuts import render,redirect
from pytube import YouTube
from .models import Video,Audio
from .forms import DownloadedForm
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
        
        # to check if the object is downloaded, if not then skip
        
        try:
            item=Video.objects.all().filter(url=url,res=res).count()
        except:pass
        
        # if the object is already downloaded
        
        if item:
            if res=='audio':
                item_audio=Audio.objects.get(title=title,author=author)
                return render(request,'apps/download.html',{'item_audio':item_audio})

            yt_image=YouTube(url).thumbnail_url
            return render(request,'apps/download.html',{'item':item,'image':yt_image})
        
        # if not downloaded
        
        if res=='highest':
            stream=yt.streams.get_highest_resolution().download(downloads_path,filename=f'{title}.mp4')
            downloadedVideo=Video(title=title,author=author,url=url,res=res)
            downloadedVideo.save()
            
        elif res=='audio':
            stream=yt.streams.get_audio_only()
            stream.download(downloads_path,filename=f'{title}.mp4')
            image=yt.thumbnail_url
            file = AudioFileClip(f'{downloads_path}/{title}.mp4')
            audioFile = f'{downloads_path}/{title}.mp3'
            file.write_audiofile(audioFile)
            file.close()
            audio = eyed3.load(f'{downloads_path}/{title}.mp3')
            audio.tag.artist = f"{author}"
            urllib.request.urlretrieve(image, f"{title}.png") 
            imagedata = open(f"{title}.png","rb").read()
            audio.tag.images.set(3,imagedata,"image/jpeg",u"you can put a description here")
            audio.tag.save()
            downloadedAudio=Audio(title=title,length=yt.length,author=author,image=f"{title}.png")
            downloadedAudio.save()
            os.remove(f'{downloads_path}/{title}.mp4')
            os.remove(f'{title}.png')
            downloadedVideo=Video(title=title,author=author,url=url,res=res)
            downloadedVideo.save()
            return render(request,'apps/download.html',{'audio':downloadedAudio})
            
        else:
            stream=yt.streams.get_by_resolution(resolution=f'{res}')
            stream.download(downloads_path,filename=f'{title}.mp4')
            downloadedVideo=Video(title=title,author=author,url=url,res=res)
            downloadedVideo.save()
            
    return render(request,'apps/download.html',{'image':yt.thumbnail_url})
                
                
                