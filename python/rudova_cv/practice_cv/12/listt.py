#ping 192.168.0.113
#SSID: lessons
import cv2
import numpy as np
import zmq 
import matplotlib.pyplot as plt
from skimage.measure import label

camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, -3)
cv2.namedWindow("Image", cv2.WINDOW_GUI_EXPANDED )
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5055
socket.connect(f"tcp://192.168.0.113:{port}")
n = 0

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
    number_cubes = 0
    number_balls = 0
    bts = socket.recv()
    n += 1
    arr = np.frombuffer(bts, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (11,11), 0)
    mask = cv2.Canny(gray, lower, upper)
    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, cnts, -1, (0, 0, 0), 1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    arrow = cnts[0]
    eps = 0.001 * cv2.arcLength(arrow, True)
    approx = cv2.approxPolyDP(arrow, eps, True)
    for p in approx:
        cv2.circle(image, tuple(*p), 6, (0, 255, 0), 2)
    hull = cv2.convexHull(arrow)
    for i in range(1, len(hull)):
        cv2.line(image, tuple(*hull[i-1]), tuple(*hull[i], (0, 255, 0), 2))
    cv2.line(image, tuple(*hull[-1]), tuple(*hull[0]), (0, 255, 0), 2)
    x, y, w, h = cv2.boundingRect(arrow)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    key = cv2.waitKey(10)
    if key == ord("q"):
        break
    if  key == ord("p"):
        cv2.imwrite("out.png", image)
    cv2.imshow("Image", image)

bts = socket.recv()
print(len(bts))
cv2.destroyAllWindows()