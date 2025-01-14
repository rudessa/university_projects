import cv2
import zmq
import numpy as np


cv2.namedWindow("Image", cv2.WINDOWGUI_NORMAL)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

port = 5055
ip = "192.168.0.113"

socket.connect(f"tcp://{ip}:{port}")

n = 0
while True:
    num_cubes = 0
    num_balls = 0

    bts = socket.recv()
    n += 1
    arr = np.frombuffer(bts, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    _, binary = cv2.threshold(hsv[:,:,1], 65, 255, cv2.THRESHBINARY)
    binary = cv2.dilate(binary, None, iterations=3)

    contours,  = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        center, radius = cv2.minEnclosingCircle(contour)
        ploshat = (1/4) * (radius*2)**2 * 3.14
        ploshat1 = cv2.contourArea(contour)
        print(ploshat, ploshat1)
        if abs(ploshat1-ploshat) < 1500:
            num_balls += 1
        else:
            num_cubes += 1
    num_objects = len(contours)
    key = cv2.waitKey(10)
    if key in (ord("q"), ord("й")):
        break
    cv2.putText(binary, f"Image: {n}", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
    cv2.putText(binary, f"Cubes: {num_cubes}, Balls: {num_balls}", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
    cv2.putText(binary, f"Objects: {num_objects}", (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
    cv2.imshow("Image", binary)
print(len(bts))

cv2.destroyAllWindows()