from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from api.models import Camera


def index(request):
    return render(request, 'homepage.html', {})

def stream(camera):
	while True:
		frame = camera.frameBorder()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def streamCamera(request):
    cam = Camera()
    cam.start()
    return StreamingHttpResponse(stream(cam), content_type='multipart/x-mixed-replace; boundary=frame')