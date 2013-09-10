# Create your views here.
from django.shortcuts import render_to_response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from MS.models import TempFile
import uuid, os

FILE_PATH = '/home/robin/Documents/red5-1.0.0/webapps/oflaDemo/streams/'
RTMP_PATH = 'rtmp://localhost/oflaDemo'


def index(request, file_name=None):
    media_file = 'toystory3.flv'
    if file_name:
        media_file = file_name
    return render_to_response('index.html', {
        'media_file': media_file,
        'rtmp_path': RTMP_PATH
    })


@api_view(['POST'])
@parser_classes((FileUploadParser,))
def file_upload(request):
    file = request.FILES.get('fileUpload', None)
    if file:
        # TODO: Streaming Video (FLV, F4V, MP4, 3GP) Streaming Audio (MP3, F4A, M4A, AAC)
        file_name = ''
        if file.content_type == u'video/x-flv':
            file_name = str(uuid.uuid1()) + '.flv'
        elif file.content_type == u'video/mp4':
            file_name = str(uuid.uuid1()) + '.mp4'

        if file_name != '':
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


@api_view(['DELETE'])
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