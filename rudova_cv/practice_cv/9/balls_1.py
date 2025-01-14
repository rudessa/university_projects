import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter

camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)
#red 120 185 190
lower = (60, 140, 140)
upper = (80, 255, 255)
prev_time = perf_counter()
cutt_time = perf_counter()
prev_x = 0
prev_y = 0
curr_x = 0
curr_y = 0
d = 7.37 #см
r = 1
points = []


while True:
    ret, image = camera.read()
    # image = image[:, ::-1, :]
    curr_time = perf_counter()

    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), r = cv2.minEnclosingCircle(c)
        if r > 10:
            cv2.circle(image, (int(curr_x), int(curr_y)), int(r), (0, 255, 255), 2)
    key = cv2.waitKey(10)
    delta = curr_time - prev_time
    dist = ((prev_x - curr_x)**2 +(prev_y - curr_y)**2) **0.5
    pxl_per_m = (d / 100) / (2*r)
    cv2.putText(image, f"Speed = {dist * pxl_per_m / delta:.4f}m/s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (127, 255, 255))
    print(dist * pxl_per_m)

    prev_x = curr_x
    prev_y = curr_y
    prev_time = curr_time 
    points.append((curr_x, curr_y))

    if len(points)>10:
        points.pop(0)

    if len(points) >= 2:
        for n,i in enumerate(range(len(points)-1)):
            p1 = int(points[i][0]), int(points[i][1]) 
            p2 = int(points[i+1][0]), int(points[i+1][1])
            print(p1, p2)
            cv2.line(image, p1, p2, (255, 0, 0), n+1)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

    cv2.imshow("Image", image)
    cv2.imshow("Mask", mask)
    prev_x = curr_x
    prev_y = curr_y
    prev_time = curr_time

camera.release()
cv2.destroyAllWindows()