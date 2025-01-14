import cv2
import numpy as np
import random

camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW) 
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)
our_balls = {0: [], 1: [], 2: []}
color_by_id = {0: 'red', 1:'blue', 2:'yellow'}
colors = {0: (25, 0, 255), 1: (255, 0, 25), 2: (0, 120, 120)}
i = 0
balls = [0, 1, 2]

random.shuffle(balls)
position = []
def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        position = [y, x]
cv2.setMouseCallback("Image", on_mouse_click)

while i != 3:
    ret, image = camera.read()
    cv2.putText(image, f"Take the {color_by_id[i]} ball", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[i])

    if position:
        bgr = image[position[0], position[1]]
        hsv = tuple(cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV))[0][0]
        position = []
        our_balls[i] = ((hsv[0]-15, hsv[1]-15, hsv[2]-15), (hsv[0]+30, 255, 255))
        i += 1
    cv2.waitKey(10)
    cv2.imshow("Image", image)

while camera.isOpened():
    coords_of_balls = []
    ret, image = camera.read()
    cv2.putText(image, f"Arrange the balls in this order: {color_by_id[balls[0]], color_by_id[balls[1]], color_by_id[balls[2]]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, tuple(map(int, our_balls[2][0])), tuple(map(int, our_balls[2][1])))
    yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
    yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)
    count = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    if len(count) > 0:
        c = max(count, key=cv2.contourArea)
        (curr_x, curr_y), r = cv2.minEnclosingCircle(c)

        if r > 10:
            cv2.circle(image, (int(curr_x), int(curr_y)), int(r), colors[2], 2)
        coords_of_balls.append((curr_x, 2))
    red_mask = cv2.inRange(hsv, tuple(map(int, our_balls[0][0])), tuple(map(int, our_balls[0][1])))
    red_mask = cv2.erode(red_mask, None, iterations=2)
    red_mask = cv2.dilate(red_mask, None, iterations=2)
    count = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    if len(count) > 0:
        c = max(count, key=cv2.contourArea)
        (curr_x, curr_y), r = cv2.minEnclosingCircle(c)

        if r > 10:
            cv2.circle(image, (int(curr_x), int(curr_y)), int(r), colors[0], 2)
        coords_of_balls.append((curr_x, 0)) 
    blue_mask = cv2.inRange(hsv, tuple(map(int, our_balls[1][0])), tuple(map(int, our_balls[1][1])))
    blue_mask = cv2.erode(blue_mask, None, iterations=2)
    blue_mask = cv2.dilate(blue_mask, None, iterations=2)
    count = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    if len(count) > 0:
        c = max(count, key=cv2.contourArea)
        (curr_x, curr_y), r = cv2.minEnclosingCircle(c)
        if r > 10:
            cv2.circle(image, (int(curr_x), int(curr_y)), int(r), colors[1], 2)
        coords_of_balls.append((curr_x, 1))

    if len(coords_of_balls) == 3:
        coords_of_balls = sorted(coords_of_balls) 
        if balls == [coords_of_balls[0][1], coords_of_balls[1][1], coords_of_balls[2][1]]:
            cv2.putText(image, f"Right", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))

    key = cv2.waitKey(10)
    if key == ord('q'):
        break
    cv2.imshow("Image", image)
camera.release()
cv2.destroyAllWindows()