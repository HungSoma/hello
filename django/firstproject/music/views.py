from django.http import HttpResponse
from django.shortcuts import render
from .models import  Album

def index(request):
    all_album = Album.objects.all()

    return render(request, 'AdminLTE/index2.html')

def detail(request, album_id):
    all_album_1 = Album.objects.all()
    for album_1 in all_album_1:
        aa = '<h2>DEtail for album id number :' + str(album_id) +' And name : '+ album_1.album_title +'<h2>'
    return HttpResponse(aa)
