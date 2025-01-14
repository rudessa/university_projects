import cv2
import numpy as np

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)

image = cv2.imread("10 cube/lection_10/hand/hands.jpg")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# бинаризировать
_, binary = cv2.threshold(hsv[:,:,1], 95, 255, cv2.THRESH_BINARY_INV)
max_contour = 0
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# binary = cv2.erode(binary, None, iterations = 40)
# # Залатать дыры
# удалить шумы
hand = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if area < 100000:  # порог для удаления шумов
        cv2.drawContours(binary, [contour], 0, 0, -1)
    else: hand = contour
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
binary = cv2.dilate(binary, None, iterations = 5)


#ЭЛЛИПС описать вокруг руки
ellipse = cv2.fitEllipse(hand)
cv2.ellipse(binary, ellipse, (200, 255, 0), -2)



cv2.imshow("Image", binary)
cv2.waitKey(0)
cv2.destroyAllWindows()