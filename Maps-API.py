import os
import sys

import pygame
import requests


width = 600
height = 450
mashtab = 0.005
lon = 65.572978
lat = 57.118832

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
# Переключаем экран и ждем закрытия окна.
run = True
fps = 5
clock = pygame.time.Clock()
while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if keys[pygame.K_PAGEUP]:
        if mashtab < 10000:
            mashtab += mashtab * 0.5
    if keys[pygame.K_PAGEDOWN]:
        if mashtab > 0.001:
            mashtab -= mashtab * 0.5
    if keys[pygame.K_LEFT]:
        lon -= mashtab * width * 0.01
    if keys[pygame.K_RIGHT]:
        lon += mashtab * width * 0.01
    if keys[pygame.K_UP]:
        if lat + mashtab * height * 0.003 < 80:
            lat += mashtab * height * 0.003
    if keys[pygame.K_DOWN]:
        lat -= mashtab * height * 0.003
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={lon}%2C{lat}&size={width},{height}&spn={mashtab},{mashtab}&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        run = False
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

# Удаляем за собой файл с изображением.
