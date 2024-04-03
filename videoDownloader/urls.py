from django.urls import path
from . import views

app_name='videoDownloader'
urlpatterns = [
    path('',views.page,name='page'),
    path('download',views.download,name='download'),
]
