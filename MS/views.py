# Create your views here.
from Tkinter import Image
import uuid
import os

from django.shortcuts import render_to_response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.http import Http404
from converter import Converter

from MS.models import TempFile


FILE_PATH = '/root/red5-1.0.0/webapps/oflaDemo/streams/'
RTMP_PATH = 'rtmp://192.168.1.165/oflaDemo'
JAR_PATH = os.path.join(os.path.dirname(__file__), '..', 'jar/').replace('\\', '/')


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
    file = request.FILES.get('file', None)
    type = request.DATA.get('type', None)
    if file:
        # TODO: Streaming Video (FLV, F4V, MP4, 3GP) Streaming Audio (MP3, F4A, M4A, AAC)
        file_name = ''
        thumbnail = ''
        convert = Converter()
        if type == u'video/x-flv':
            uuid_string = str(uuid.uuid1())
            file_name = uuid_string + '.flv'
            thumbnail = uuid_string + '.jpg'
        elif type == u'video/mp4':
            uuid_string = str(uuid.uuid1())
            file_name = uuid_string + '.mp4'
            thumbnail = uuid_string + '.jpg'
        if file_name != '':
            file_path = FILE_PATH + file_name
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
                convert.thumbnail(file_path, 10, FILE_PATH + thumbnail)
            temp_file = TempFile(name=file_name, path=file_path)
            temp_file.save()
            return Response({
                'file_name': file_name,
                'thumbnail': thumbnail
            })
        else:
            return Response({
                'status': 'Current just support .mp4 && .flv.'
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


@api_view(['GET'])
def attachment(request, file_name=None):
    if file_name is not None:
        file_path = FILE_PATH + file_name
        file_type = file_name.split('.')[-1]
        content_type = ''
        if file_type == u'flv':
            content_type = 'video/x-flv'
        elif file_type == u'mp4':
            content_type = 'video/mp4'
        media_file = FileWrapper(open(file_path, 'rb'))
        response = HttpResponse(media_file, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response
    else:
        return Http404


@api_view(['GET'])
def thumbnail(request, name=None):
    if name is not None:
        file_path = FILE_PATH + name
        try:
            with open(file_path, "rb") as f:
                return HttpResponse(f.read(), mimetype="image/jpeg")
        except IOError:
            return Http404
