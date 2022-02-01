from imutils.perspective import four_point_transform
import cv2
#from picamera import PiCamera

class Scanner():
    def __init__(self):
        self.height = 1080
        self.width = 1920

        self.green = (0, 255, 0)

    def readImage(self, image):
        #read image and resize that
        self.image = image
        self.image = cv2.resize(self.image, (self.width, self.height))
        self.orig_image = self.image.copy()

    def filter(self):
        #using gray scale, gaussian blur and canny i try to identify the edges
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.blur = cv2.GaussianBlur(self.gray, (5, 5), 0)
        self.edged = cv2.Canny(self.blur, 75, 200)

    def contoursFinder(self):
        #using the modified image through the filters i find the contours
        self.contours, _ = cv2.findContours(self.edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = sorted(self.contours, key=cv2.contourArea, reverse=True)

        # cv2.imshow("Image", self.image)
        # cv2.drawContours(self.image, self.contours, -1, self.green, 3)
        # cv2.imshow("All contours", self.image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        #to find the contour of the paper i have to disinguish the closed 4 points loop from others
        for self.contour in self.contours:
            self.peri = cv2.arcLength(self.contour, True)
            self.approx = cv2.approxPolyDP(self.contour, 0.05 * self.peri, True)

            if len(self.approx) == 4:
                self.doc_cnts = self.approx
                break

    def printContoursFinder(self):
        cv2.drawContours(self.image, self.contours, -1, self.green, 3)
        return self.image

    def birdView(self):
        #applico la BIRD VIEW
        self.warped = four_point_transform(self.orig_image, self.doc_cnts.reshape(4, 2))
        self.warped = cv2.cvtColor(self.warped, cv2.COLOR_BGR2GRAY)
        
    def print_cv(self):
        cv2.drawContours(self.orig_image, [self.doc_cnts], -1, self.green, 3)
        cv2.imshow("Contours of the document", self.orig_image)
        cv2.imshow("Scanned", cv2.resize(self.warped, (600, 800)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def scan(self):
        self.readImage()
        self.filter()
        self.contoursFinder()
        self.birdView()
        #self.print_cv()       


if __name__ == '__main__':
    s = Scanner()

    s.scan()