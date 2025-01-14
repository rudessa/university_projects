import cv2
import numpy as np
from skimage.measure import label

camera = cv2.VideoCapture("pictures.avi") 
# cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cnt = 0

while True:
    ret, image = camera.read()
    if not ret:
        break
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.bitwise_not(gray)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    thresh = np.bitwise_not(thresh)
    cnts,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    num_cnts = len(cnts)
    if num_cnts == 28:
        cnt += 1
    # cv2.putText(thresh, f"{num_cnts}", (60, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (60, 0, 255))
    # cv2.imshow("Image", thresh)
print(cnt)
cv2.destroyAllWindows()
camera.release()
