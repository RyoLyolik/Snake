import pygame
import random

pygame.init()

size = w, h, = 900, 900
k = 50
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


class Win:
    def __init__(self):
        self.event = True
        self.grid = Grid()
        self.snake = Snake()
        self.e = EventsHandling(snake=self.snake)

        self.screen_updates()

    def screen_updates(self):
        while self.event:
            clock.tick(10)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.event = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    print(self.grid.get_by_pos(pygame.mouse.get_pos()))

            screen.fill((255,255,255))

            self.e.key_events()
            self.grid.draw()
            self.snake.move()
            self.snake.draw()

            pygame.display.flip()

class Snake:
    def __init__(self):
        self.pos_head = [random.choice(range(18)), random.choice(range(18))]
        self.speedx = 0
        self.speedy = 0

    def move(self):
        self.pos_head[0] += self.speedx
        self.pos_head[1] += self.speedy

    def draw(self):
        pygame.draw.rect(screen,(100,155,255), (self.pos_head[0]*k, self.pos_head[1]*k, k, k))

class Grid:
    def __init__(self):
        self.grid = [[j for j in range(w//k)] for _ in range(h//k)]

    def draw(self):
        for column in range(w//k):
            pygame.draw.line(screen,(0,0,0), (column*k, 0), (column*k, h), 1)

        for row in range(w//k):
            pygame.draw.line(screen,(0,0,0), (0, row*k), (w, row*k), 1)

    def get_by_pos(self, pos):
        return pos[0]//k, pos[1] // k


class EventsHandling:
    def __init__(self, **kwargs):
        print(kwargs)
        self.kwargs = kwargs

    def key_events(self, e=None):
        if 'snake' in self.kwargs:
            snake = self.kwargs['snake']
            if pygame.key.get_pressed()[pygame.K_a]:
                snake.speedx = -1
                snake.speedy = 0

            if pygame.key.get_pressed()[pygame.K_d]:
                snake.speedx = 1
                snake.speedy = 0

            if pygame.key.get_pressed()[pygame.K_s]:
                snake.speedy = 1
                snake.speedx = 0

            if pygame.key.get_pressed()[pygame.K_w]:
                snake.speedy = -1
                snake.speedx = 0


if __name__=='__main__':
    win = Win()