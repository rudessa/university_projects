import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter


camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_EXPOSURE, -4)
roi = None 
position = []

def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        position = [y, x]
        print(f"Clicked at {position}")
cv2.setMouseCallback("Image", on_mouse_click)

while True:
    ret, image = camera.read()
    # image = image[:, ::-1, :]
    if position:
        bgr = image[position[0], position[1]]
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)
        cv2.circle(image, (position[1], position[0]), 5, (255, 0, 0))
        cv2.putText(image, f"BGR = {bgr}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, tuple(map(int, bgr)))
        cv2.putText(image, f"HSV = {hsv}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, tuple(map(int, bgr)))

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    cv2.imshow("Image", image)

camera.release()
cv2.destroyAllWindows()
#red 45 40 170