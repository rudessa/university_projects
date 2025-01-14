import cv2
import numpy as np

image = cv2.imread("10 cube/lection_10/arrow.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
cnts,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# print(cnts)
arrow = cnts[0]
cv2.drawContours(image, cnts, 0, (0, 150, 255), 8)

print(f"Area = {cv2.contourArea(arrow)}")
print(f"Lenght = {cv2.arcLength(arrow, False)}")#открытый контур
print(f"Lenght = {cv2.arcLength(arrow, True)}")#закрытый контур

#информация
moments = cv2.moments(arrow)
print(moments)

#ЦЕНТРОИД
centroid = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
print(f"Centroid = {centroid}")
cv2.circle(image, centroid, 4, (0, 150, 255), 10)#точка

#точками строит контур
eps = 0.001 * cv2.arcLength(arrow, True)
approx = cv2.approxPolyDP(arrow, eps, True)
for p in approx:
    cv2.circle(image, tuple(*p), 6, (0, 255, 0), 2)

#выпуклый полигон/выпуклая фигура, в которую помещается обьект
hull = cv2.convexHull(arrow)
for i in range(1, len(hull)):
    cv2.line(image, tuple(*hull[i - 1]), tuple(*hull[i]), (0, 255, 0), 2) #распаковка *
cv2.line(image, tuple(*hull[- 1]), tuple(*hull[0]), (0, 255, 0), 2) #распаковка *

#пример_1
x, y, w, h = cv2.boundingRect(arrow)
cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2 )
#сколько площади занимает объект заключенный в фигуру?
#вписывается фигура в повернутый прямоугольник
rect = cv2.minAreaRect(arrow)
box = cv2.boxPoints(rect)
box = np.intp(box)
cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

#пример_2
#вписывается фигура в круг
(x, y), r = cv2.minEnclosingCircle(arrow)
center = int(x), int(y)
r = int(r)
cv2.circle(image, center, r, (0, 255, 0), 2)

#определяет наклон объекта ЭЛЛИПС
ellipse = cv2.fitEllipse(arrow)
cv2.ellipse(image, ellipse, (0, 255, 0), 2)

#уравнение прямой 
#найти прямую с ее наклоном
#нахождение направление объекта(Главная ось обьекта)
vx, vy, x, y = cv2.fitLine(arrow, cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x * vy / vx) + y)
righty = int(((image.shape[0]-x) * vy / vx ) + y)
cv2.line(image, (image.shape[0] - 1, righty), (0, lefty), (0, 255, 0), 2)




cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
