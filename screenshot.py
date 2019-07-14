import cv2
import time

def screenshot(i):
    global cam
    cv2.imshow("screenshot" + str(i), cam.read()[1])
    cv2.imwrite("filename"+ str(i)".jpg", cam.read()[1])
if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    i = 0
    while True:
        rect, img = cam.read()
        cv2.imshow("cameraFeed", img)
        ch = cv2.waitKey(5)
        print(ch)
        if ch == 27:
            break
        if ch == ord('c'):
            screenshot(i)
            i = i + 1
            
    cv2.destroyAllWindows()