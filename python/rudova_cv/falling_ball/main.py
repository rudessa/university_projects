import pygame
import sys
import cv2
import numpy as np
import math

pygame.init()

camera = cv2.VideoCapture(1 + cv2.CAP_DSHOW) 
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)

roi = None

while True:
    ret, img = camera.read()
        
    # Загрузка изображения доски с помощью OpenCV
    # img = cv2.imread("main/scr.jpg)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    _, thresh = cv2.threshold(imghsv[:, :, 1], 65, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, None, iterations=1)
    thresh = cv2.dilate(thresh, None, iterations=10)
    thresh = cv2.erode(thresh, None, iterations=0)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

mask = np.zeros_like(thresh)
for cnt in cnts:
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(mask, [box], 0, (255), -1)


thresh = mask
cv2.imshow("Screen", thresh)
cv2.waitKey(0)

height, width = thresh.shape
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Падающий шар")

board_img = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
board_img = np.fliplr(board_img)
# board_img = np.flipud(board_img)

board_img = np.rot90(board_img,1 )  # Поворачиваем на 90 градусов
board_img = pygame.surfarray.make_surface(board_img)

RED = (255, 0, 0)

# Параметры шара
ball_radius = 20
ball_x = width // 2
ball_y = ball_radius
ball_speed_x = 0
ball_speed_y = 0
gravity = 0.2
friction = 6  # Коэффициент трения
bounce = 0.2 # Коэффициент упругости

# Главный цикл
clock = pygame.time.Clock()
running = True

def get_surface_normal(x, y):
    if x < 0 or y < 0 or x >= width or y >= height:
        return 0, -1  # Возвращаем нормаль вниз, если координаты вне границ
    gx = cv2.Sobel(thresh, cv2.CV_64F, 1, 0, ksize=5)
    gy = cv2.Sobel(thresh, cv2.CV_64F, 0, 1, ksize=5)
    nx, ny = -gx[int(y), int(x)], -gy[int(y), int(x)]
    length = math.hypot(nx, ny)
    if length == 0:
        return 0, -1  # Возвращаем нормаль вниз, если длина равна 0
    return nx / length, ny / length

def check_collision(ball_x, ball_y):
    if ball_x < 0 or ball_y < 0 or ball_x >= width or ball_y >= height:
        return False
    return thresh[int(ball_y), int(ball_x)] == 255

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление скорости шара под действием гравитации
    ball_speed_y += gravity

    # Предполагаемое новое положение шара
    new_ball_x = ball_x + ball_speed_x
    new_ball_y = ball_y + ball_speed_y

    # Проверка коллизий с поверхностью
    if check_collision(new_ball_x, new_ball_y + ball_radius):
        normal_x, normal_y = get_surface_normal(new_ball_x, new_ball_y + ball_radius)
        
        velocity_along_normal = ball_speed_x * normal_x + ball_speed_y * normal_y
        velocity_along_tangent_x = ball_speed_x - velocity_along_normal * normal_x
        velocity_along_tangent_y = ball_speed_y - velocity_along_normal * normal_y

        velocity_along_tangent_x *= friction
        velocity_along_tangent_y *= friction

        ball_speed_x = velocity_along_tangent_x
        ball_speed_y = velocity_along_tangent_y

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        ball_speed_x = -velocity_along_normal * normal_x * bounce
        ball_speed_y = -velocity_along_normal * normal_y * bounce

    else:
        ball_x = new_ball_x
        ball_y = new_ball_y
        
    if ball_y + ball_radius > height:
        ball_y = height - ball_radius
        ball_speed_y = 0

    screen.fill((0, 0, 0))
    screen.blit(board_img, (0, 0))
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
