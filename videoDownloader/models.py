from django.db import models

# Create your models here.
def image_upload(instance,filename:str):
    extension=filename.split('.')[1]
    return f"downloaded/{instance.name}.{extension}"

class Audio(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    image=models.ImageField(upload_to=image_upload)
    length=models.IntegerField()
    
    def __str__(self) -> str:
        return self.title
    
class Video(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    url=models.URLField(max_length=200)
    res=models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return self.title