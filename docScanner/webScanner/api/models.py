from django.db import models
from .piStream import CameraStream


class Camera():
    def __init__(self):
        self.piStream = CameraStream()

    def __del__(self):
        self.piStream.stop()

    def start(self):
        self.piStream.start()

    def frameBorder(self):
        return self.piStream.frameBorder()

    def frameBorderFull(self):
        return self.piStream.frameBorderFull()