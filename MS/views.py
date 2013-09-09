# Create your views here.
from django.shortcuts import render, render_to_response


def index(request):
    media_file = 'toystory3.flv'
    rtmp_path = 'rtmp://localhost/oflaDemo'
    return render(request, 'index.html', {
        'media_file': media_file,
        'rtmp_path': rtmp_path
    })