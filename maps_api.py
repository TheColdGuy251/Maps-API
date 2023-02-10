import pygame
import sys
import requests
import os
from PIL import Image


def response_get():
    map_request = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": "sat"
    }
    response = requests.get(map_request, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return response


def pil_image_to_surface(pil_image):
    mode, size, data = pil_image.mode, pil_image.size, pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


class Button():
    def __init__(self, x, y, buttonText, onclickFunction):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.onclickFunction = onclickFunction
        self.buttonText = buttonText
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.alreadyPressed = False
        self.buttonSurf = None
        objects.append(self)

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface = self.buttonSurface.convert_alpha()
        if not self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill((0, 0, 0, 0))
            font = pygame.font.SysFont("arial", 25)
            self.buttonSurf = font.render(self.buttonText, True, (255, 255, 255))
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill((0, 39, 62, 150))
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2])
        screen.blit(self.buttonSurface, self.buttonRect)


def nothing():
    pass

def yet():
    pass


if __name__ == "__main__":
    pygame.init()
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    lon = 133
    lat = -27
    delta = 65
    map_file = "map.png"
    responser = response_get()
    with open(map_file, "wb") as file:
        file.write(responser.content)
    pil_image = Image.open(map_file)
    pil_image = pil_image.resize((width, height))
    pygame_image = pil_image_to_surface(pil_image.convert('RGBA'))

    pygame.display.set_caption("Я карта")
    objects = []
    fps = 60
    clock = pygame.time.Clock()
    Button(width * 0.8, height * 0.008, 'Nothing', nothing)
    Button(width * 0.9, height * 0.008, 'Yet', yet)
    running = True
    while running:
        keys = pygame.key.get_pressed()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                pygame.quit()
                sys.exit()
        if keys[pygame.K_1]:
            if delta > 10:
                delta -= 10
                responser = response_get()
                with open(map_file, "wb") as file:
                    file.write(responser.content)
        width, height = pygame.display.get_surface().get_size()
        pil_image = Image.open(map_file)
        pil_image = pil_image.resize((width, height))
        pygame_image = pil_image_to_surface(pil_image.convert('RGBA'))
        screen.blit(pygame_image, (0, 0))
        for object in objects:
            object.process()
        pygame.display.flip()
        clock.tick(fps)

