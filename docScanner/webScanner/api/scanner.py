from imutils.perspective import four_point_transform
import cv2
import numpy as np
import sys
#from picamera import PiCamera

class Scanner():
    def __init__(self):
        self.height = 1080
        self.width = 1920

        self.green = (0, 255, 0)
        np.set_printoptions(threshold=sys.maxsize)

    def readImage(self, image):
        #read image and resize that
        self.image = image
        self.height_img, self.width_img, c = self.image.shape
        self.orig_image = self.image.copy()

    def filter(self):
        #using gray scale, gaussian blur and canny i try to identify the edges
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.kernel = np.ones((5, 5), np.uint8)
        self.erosion = cv2.erode(self.gray, self.kernel, iterations=1)
        self.opening = cv2.morphologyEx(self.erosion, cv2.MORPH_OPEN, self.kernel)
        self.closing = cv2.morphologyEx(self.opening, cv2.MORPH_CLOSE, self.kernel)
        self.edged = cv2.Canny(self.closing, 20, 240)

    def contoursFinder(self):
        #using the modified image through the filters i find the contours
        self.thresh = cv2.adaptiveThreshold(self.edged, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        self.contours, _ = cv2.findContours(self.thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        self.areas = [cv2.contourArea(c) for c in self.contours]
        self.max_index = np.argmax(self.areas)

        # Find the approx poly of the image
        self.epsilon = 0.05 * cv2.arcLength(self.contours[self.max_index], True)
        self.approx = cv2.approxPolyDP(self.contours[self.max_index], self.epsilon, True)
        if len(self.approx) == 4:
            self.doc_cnts = self.approx

    def printContoursFinder(self):
        cv2.drawContours(self.image, self.contours, -1, self.green, 3)
        return cv2.resize(self.image, (800, 600))

    def birdView(self):
        #applico la BIRD VIEW

        self.pts1 = np.float32(self.doc_cnts)
        self.pts = np.float32([[0, 0], [self.width_img, 0], [self.width_img, self.height_img], [0, self.height_img]])
        self.matrix = cv2.getPerspectiveTransform(self.pts1, self.pts)
        self.result = cv2.warpPerspective(self.orig_image, self.matrix, (self.width_img, self.height_img))
        self.flip = cv2.flip(self.result, 1) # Flip Image
        self.rotate = cv2.rotate(self.flip, cv2.ROTATE_90_COUNTERCLOCKWISE) # Rotate Image
        self.warped = cv2.cvtColor(self.rotate, cv2.COLOR_BGR2GRAY)
        
    def print_cv(self):
        cv2.imshow("Contours of the document", self.orig_image)
        cv2.imshow("Scanned", cv2.resize(self.warped, (600, 800)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print(self):
        cv2.drawContours(self.orig_image, [self.doc_cnts], -1, self.green, 3)
        return cv2.resize(self.warped, (600, 800))

    def scan(self,image):
        self.readImage(image)
        self.filter()
        self.contoursFinder()
        self.birdView()
        return self.print()       


if __name__ == '__main__':
    s = Scanner()

    image = cv2.imread('prova.jpg')

    s.scan(image)
