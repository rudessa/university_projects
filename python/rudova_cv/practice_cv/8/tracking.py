import cv2
import numpy as np
import matplotlib.pyplot as plt

camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)

roi = None

while True:
    ret, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    key = cv2.waitKey(10)
    if key == ord('q'):
        break
    if key == ord("f"):
        x, y, w, h = cv2.selectROI("ROI selection", gray)
        roi = gray[y : y+h, x: x+w]
        cv2.imshow("ROI", roi)
        cv2.destroyWindow("ROI selection")

    cv2.imshow("Image", image)

camera.release()
cv2.destroyAllWindows()