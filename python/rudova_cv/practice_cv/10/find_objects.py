#ping 192.168.0.113
#SSID: lessons
import cv2
import numpy as np
import zmq 
import matplotlib.pyplot as plt
from skimage.measure import label


cv2.namedWindow("Image", cv2.WINDOW_GUI_EXPANDED )
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5055
socket.connect(f"tcp://192.168.0.113:{port}")
n = 0

while True:
    number_cubes = 0
    number_balls = 0
    bts = socket.recv()
    n += 1
    arr = np.frombuffer(bts, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    _, binary = cv2.threshold(hsv[:, :, 1], 70, 255, cv2.THRESH_BINARY)
    binary = cv2.dilate(binary, None, iterations = 2)
    labeled = label(binary)
    print(labeled.max())

    key = cv2.waitKey(10)
    if key == ord("q"):
        break
    cv2.putText(image, f"Image = {n}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (127, 255, 255))
    cv2.putText(binary, f"Number of cubes: {number_cubes}, Number of balls: {number_balls}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (127, 255, 255))
    cv2.imshow("Image", image)
    cv2.imshow("Image", binary)

bts = socket.recv()
print(len(bts))
cv2.destroyAllWindows()
