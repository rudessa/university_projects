# ping 192.168.0.111
import cv2
import zmq #pip install pyzmq
import numpy as np
from skimage.measure import regionprops

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)

port = 5055
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect(f"tcp://192.168.0.113:{port}")
# while True:
#     # bts = socket.recv()
#     # num_orb = 0
#     # num_balls = 0
#     # number_pict += 1
#     # arr = np.frombuffer(bts, np.uint8)
#     # image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
#     # blured = cv2.GaussianBlur(image, (11, 11), 0)
#     image = cv2.imread()
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     _, thresh = cv2.threshold(hsv[:, :, 1], 50, 255, cv2.THRESH_BINARY)
#     distance_map = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
#     distance_map = cv2.normalize(distance_map, None, 0, 1.0, cv2.NORM_MINMAX)
#     ret, dist_thresh = cv2.threshold(distance_map, 0.6*np.max(distance_map), 255, cv2.THRESH_BINARY)
#     confuse = cv2.subtract(thresh, dist_thresh.astype("uint8"))
#     ret, markers = cv2.connectedComponents(dist_thresh.astype("uint8"))
#     markers += 1
#     markers[confuse==255] = 0
#     segments = cv2.watershed(blured, markers)
#     cnts, hierrachy = cv2.findContours(segments, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#     for i in range(len(cnts)):
#         if hierrachy[0][i][3] == -1:
#             cv2.drawContours(image, cnts, i, (0, 255, 0), 1)
#     property = []
#     for i, region in enumerate(regionprops(segments)):
#             property.append((region.eccentricity, (region.area/region.image.size)))
#     orb = 0
#     balls = 0
#     objects = markers.max()-1
#     for i in property:
#         if i[0] < 0.43 and i[1] > 0.5:
#             orb += 1
#     balls = objects - orb
#     key = cv2.waitKey(10)
#     if key == ord("q") or ord("й"):
#         break


number_pict = 0
image = cv2.imread("11_segment/out.png")

blured = cv2.GaussianBlur(image, (11, 11), 0)
hsv = cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)
_, thresh = cv2.threshold(hsv[:, :, 1], 55, 255, cv2.THRESH_BINARY)
distance_map = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
distance_map = cv2.normalize(distance_map, None, 0, 1, cv2.NORM_MINMAX)
ret, dist_thresh = cv2.threshold(distance_map, 0.45 * np.max(distance_map), 255, cv2.THRESH_BINARY)
confuse = cv2.subtract(thresh, dist_thresh.astype("uint8"))
ret, markers = cv2.connectedComponents(dist_thresh.astype("uint8"))
markers += 1
markers[confuse==255] = 0
segments = cv2.watershed(image, markers)
cnts, hierrachy = cv2.findContours(segments, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(cnts)):
    if hierrachy[0][i][3] == -1:
        cv2.drawContours(image, cnts, i, (0, 255, 0), 2)

property = []
for i, region in enumerate(regionprops(segments)):
        property.append((region.eccentricity, (region.area/region.image.size)))
orb = 0
balls = 0
objects = markers.max()-1

for i in property:
    if i[0] < 0.43 and i[1] > 0.5:
        orb += 1
balls = objects - orb

cv2.putText(image, f"Objects: {objects}", (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
cv2.putText(image, f"orb: {orb}, Balls: {balls}", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
cv2.imshow("Im_1", segments.astype("uint8"))
cv2.imshow("Im_2", image.astype("uint8"))
cv2.waitKey(0)
cv2.destroyAllWindows()