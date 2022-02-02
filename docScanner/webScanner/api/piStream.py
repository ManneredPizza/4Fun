from picamera import PiCamera
from picamera.array import PiRGBArray
from .scanner import Scanner
from threading import Thread
import time
import cv2
import gc


class CameraStream():
    def __init__(self):
        self.camera = PiCamera()
        resolution = (1920,1080)
        self.camera.resolution = resolution
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.scan = Scanner()
        self.stopped = False

    def start(self):
        #start il thread che legge i frame dai video
        Thread(target=self.update, args =()).start()
        time.sleep(1.0)
        return self.camera
    
    def update(self):
        #looppa all'infinito finchè il thread non è bloccato
        for f in self.stream:
            #prendi il frame dalla stream
            self.frame = f.array
            self.rawCapture.truncate(0)
            
            
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                # del self.camera
                # del self.rawCapture
                # gc.collect()
                return
    
    def read(self):
        #ritorna il frame più recente
        return self.frame
        
    def stop(self):
        self.stopped = True

    def frameBorder(self):
        #self.scan.readImage(self.frame)
        # self.scan.filter()
        # self.scan.contoursFinder()
        # self.image = self.scan.printContoursFinder()
        self.image = self.scan.scan(self.frame)
        ret, self.frame_buff = cv2.imencode('.jpg', self.image)
        return self.frame_buff.tobytes()

    def frameBorderFull(self):
        self.scan.readImage(self.frame)
        self.scan.filter()
        self.scan.contoursFinder()
        self.image = self.scan.printContoursFinder()
        ret, self.frame_buff = cv2.imencode('.jpg', self.image)
        return self.frame_buff.tobytes()