from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from api.models import Camera
from django.views.decorators import gzip

cam = Camera()
cam.start()

def index(request):
    return render(request, 'homepage.html', {})

def stream(camera):
	while True:
		frame = camera.frameBorder()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def streamFull(camera):
	while True:
		frame = camera.frameBorderFull()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def streamCamera(request):
    return StreamingHttpResponse(stream(cam), content_type='multipart/x-mixed-replace; boundary=frame')

@gzip.gzip_page
def streamCameraFull(request):
    return StreamingHttpResponse(streamFull(cam), content_type='multipart/x-mixed-replace; boundary=frame')