from threading import Thread

import time
from django import forms
from django.http import StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators import gzip
from django.views.generic import TemplateView

from detector.drive import main
from detector.video import FaceDetector

default_path = "/Users/dineshsingh/Downloads/real-1-c.mp4"
# default_path = "rtsp://192.168.43.101:8554/unicast"
# default_path = 0
# default_path = "rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov"

def gen(camera):
    while True:

        frame = camera.videoStreamer(skip=10)
        if frame == -1:
            print("Error frame =-1...exhiting")
            return
        else:
            if frame:
                if frame is None:
                    return
                print("Returning frame")
                try:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                except:
                    print("error: Yield error")
                    return



def start_detecting(cam):
    cam.videoStreamer(skip=0)


@gzip.gzip_page
def index(request):
    main()
    try:
        path = request.GET.get("url")
        print(path)
        # if path is None:
        #     path = default_path
        path = default_path
        cam = FaceDetector(path)
        # thread = Thread(target=start_detecting, args=(cam, path))
        # thread.start()
        start_detecting(cam)



        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(e.with_traceback())


class URLForm(forms.Form):
    url = forms.CharField(label='URL', max_length=100)


def get_url(request):
    form = URLForm()
    return render(request, 'video_url.html', {'form': form})
