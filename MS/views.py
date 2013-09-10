# Create your views here.
from django.shortcuts import render_to_response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from MS.models import TempFile
import uuid, os

FILE_PATH = '/home/robin/Documents/red5-1.0.0/webapps/oflaDemo/streams/'
RTMP_PATH = 'rtmp://localhost/oflaDemo'


def index(request):
    media_file = '72964322-19e3-11e3-a6f3-000c294c1bd8.flv'
    return render_to_response('index.html', {
        'media_file': media_file,
        'rtmp_path': RTMP_PATH
    })


@api_view(['POST'])
@parser_classes((FileUploadParser,))
def file_upload(request):
    file = request.FILES.get('fileUpload', None)
    if file:
        if file.content_type == 'video/x-flv':
            file_name = str(uuid.uuid1()) + '.flv'
            file_path = FILE_PATH + file_name
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
            temp_file = TempFile(name=file_name, path=file_path)
            temp_file.save()
            return Response({
                'file name': file_name
            })
    return Response({
        'received data': request.DATA
    })


@api_view(['POST'])
@parser_classes((JSONParser,))
def remove_file(request):
    try:
        file_name = request.DATA.get('file_name', None)
        if file_name:
            current_file = TempFile.objects.filter(name=file_name)[0]
            os.remove(current_file.path)
            current_file.delete()
    except:
        return Response({
            'status': 'remove file fail'
        })

    return Response({
        'status': 'remove file success'
    })