import matplotlib.pyplot as plt
import numpy as np
import socket


host = "84.237.21.36"
port = 5152


def check(B, y, x):
    if not 0 <= x < B.shape[0]:
        return False
    if not 0 <= y < B.shape[1]:
        return False
    if B[y, x] != 0:
        return True
    return False


def neighbors4(B, y, x):
    left = y, x-1
    top = y - 1, x
    right = y, x+1
    bottom = y+1, x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top = None
    if not check(B, *right):
         right = None
    if not check(B, *bottom):
        bottom = None
    return left, top, right, bottom


def recvall(sock, N):
    data = bytearray()
    while len(data) < N:
        packet = sock.recv(N-len(data))#пакет данных
        if not packet:
            return
        data.extend(packet)
    return data


def extremum(picture):
    extremums = []
    for y in range(picture.shape[0]):
        for x in range(picture.shape[1]):
            count = 0
            find_neighbors = neighbors4(picture, y, x)
            for find_neighbor in find_neighbors:
                if find_neighbor is not None and (picture[y, x] > picture[find_neighbor[0], find_neighbor[1]]):
                    count += 1
            if count == len(find_neighbors):
                extremums.append((y, x))

    return extremums

def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


pictures = []
all_distances = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    for i in range(10):
        distance_between_point = "None"
        sock.send(b"get")
        bytes = recvall(sock, 40002)
        picture = np.frombuffer(bytes[2 : 40002], dtype="uint8").reshape(bytes[0], bytes[1])
        pictures.append(picture)
        points = extremum(picture)
        if len(points) == 2:
          distance_between_point = distance(points[0], points[1])
        all_distances.append(distance_between_point)
        #Проверка
        sock.send(f"{distance_between_point:.1f}".encode())
        responce = sock.recv(20)
    sock.send(b'beat')
    print(sock.recv(20))

for number, pic in enumerate(pictures):
    plt.subplot(2, 5, number+1)
    plt.title(f"diss ={all_distances[number]:.1f}")
    plt.imshow(pic)
plt.show()
