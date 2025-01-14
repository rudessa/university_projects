#написать программу для определения движения на камере
import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter


camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Background", cv2.WINDOW_GUI_NORMAL)

background = None
prev_gray = None
min_area = 1000
prev_time = perf_counter()

while camera.isOpened():
    curr_time = perf_counter()
    ret, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0) 
    if prev_gray is None:
        prev_gray = gray.copy()
    diff_gray = cv2.absdiff (gray, prev_gray)
    diff_tresh = cv2.threshold(diff_gray, 45, 255, cv2.THRESH_BINARY)[1]
    diff_percent = np.sum(diff_tresh) / diff_tresh.size
    prev_gray = gray.copy()
    # gray = gray[:, ::-1, :]
    # image = image[:, ::-1, :]
    # cv2.imshow( "Background", gray )    
    key = cv2.waitKey(10)
    if key == ord('q') or key == ord ('й'):
        break
    if key == ord("b") or (curr_time - prev_time)>1:
        background = gray.copy()
        prev_time = curr_time
    if key == ord('b') or key == ord ('и'):
        background = gray.copy()
    if background is not None:
        delta = cv2.absdiff(background, gray)
        thresh  = cv2.threshold(delta, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if area > min_area:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.imshow("Background", delta)
        cv2.imshow("Image", image)


camera.release()
cv2.destroyAllWindows()