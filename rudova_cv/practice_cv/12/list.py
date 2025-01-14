#list
import cv2
import numpy as np
import matplotlib.pyplot as plt

camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, -3)
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

lower = 100
upper = 200


def lower_update(value):
    global lower
    lower = value


def upper_update(value):
    global upper
    upper = value


cv2.createTrackbar("Lower", "Mask", lower, 255, lower_update)
cv2.createTrackbar("Upper", "Mask", upper, 255, upper_update)

while True:
    ret, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (11,11), 0)
    mask = cv2.Canny(gray, lower, upper)
    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, cnts, -1, (0, 0, 0), 1)
    key = cv2.waitKey(10)
    if key == ord('q'):
        break
    if key == ord("f"):
        x, y, w, h = cv2.selectROI("ROI selection", gray)
        roi = gray[y : y+h, x: x+w]
        cv2.imshow("ROI", roi)
        cv2.destroyWindow("ROI selection")

    cv2.imshow("Image", image)
    cv2.imshow("Mask", mask)

camera.release()
cv2.destroyAllWindows()