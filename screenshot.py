import cv2
import time
from text_recognition import Text_Recognition

class ScreenshotCamera:
    def screenshot(self):
        filename = "capture" + str(self.i) + ".jpg"

        #cv2.imshow("screenshot" + str(self.i), self.cam.read()[1])
        cv2.imwrite(filename, self.cam.read()[1])
        
        self.tr.start(filename, self.target_word, self.isRotated)
        
        self.i = self.i + 1

    def start(self, target_word, isRotated):
        self.cam = cv2.VideoCapture(0)
        self.i = 0
        self.target_word = target_word
        self.isRotated = isRotated

        self.tr = Text_Recognition()

        while True:
            rect, img = self.cam.read()
            cv2.imshow("cameraFeed", img)
            ch = cv2.waitKey(5)

            if ch == 27:
                break
            if ch == ord('c'):
                self.screenshot()

        destroy()

    def destroy(self):
        cv2.destroyAllWindows()
