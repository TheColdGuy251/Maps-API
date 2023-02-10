import pygame
import sys


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
            font = pygame.font.SysFont("arial", 45)
            self.buttonSurf = font.render(self.buttonText, True, (255, 255, 255))
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill((0, 39, 62, 0))
            shape_surf = pygame.Surface(pygame.Rect(0, self.y, pygame.display.Info().current_w, self.height).size,
                                        pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 39, 62, 230), shape_surf.get_rect())
            screen.blit(shape_surf, (0, self.y, pygame.display.Info().current_w, self.height))
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
    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Я карта")
    objects = []
    fps = 60
    clock = pygame.time.Clock()
    Button(width / 2, height / 2, 'Nothing', nothing)
    Button(width / 2, height / 2, 'Yet', yet)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pass
        for object in objects:
            object.process()
        pygame.display.flip()
        clock.tick(fps)

