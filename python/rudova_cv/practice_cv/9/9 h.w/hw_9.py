import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter

camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_EXPOSURE, -4)
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

lower = (50, 130, 130)
upper = (80, 255, 255)
prev_x = 0
prev_y = 0
curr_x = 0
curr_y = 0
d = 7.37 #см
r = 1

#65 150 150 #зеленый lower = (50, 130, 130) upper = (80, 255, 255)
#20 205 210 желтый lower = (10, 140, 130) upper = (20, 255, 255)
#0 255 155 красный lower = (0, 205, 100) upper = (5, 255, 255)
#100 240 120 голубой lower = (90, 200, 100) upper = (100, 255, 255)
def found_color():
    position = []
    def on_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global position
            position = [y, x]
            print(f"Clicked at {position}")
    cv2.setMouseCallback("Image", on_mouse_click)

    while True:
        ret, image = camera.read()
        if position:
            bgr = image[position[0], position[1]]
            hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)
            cv2.circle(image, (position[1], position[0]), 5, (255, 0, 0))
            cv2.putText(image, f"BGR = {bgr}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, tuple(map(int, bgr)))
            cv2.putText(image, f"HSV = {hsv}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, tuple(map(int, bgr)))


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

    if key == ord('q'):
        break
    cv2.imshow("Image", image)
    cv2.imshow("Mask", mask)
camera.release()
cv2.destroyAllWindows()