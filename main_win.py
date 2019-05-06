import pygame
import random

pygame.init()

size = w, h, = 900, 900
k = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


class Win:
    def __init__(self):
        self.event = True
        self.grid = Grid()
        self.grid.create_food()
        self.snake = Snake()
        self.e = EventsHandling(snake=self.snake, grid=self.grid)

        self.screen_updates()

    def screen_updates(self):
        while self.event:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.event = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    print(self.grid.get_by_pos(pygame.mouse.get_pos()))

            screen.fill((255,255,255))

            self.e.key_events()
            self.grid.draw()
            self.snake.draw()

            pygame.display.flip()

class Snake:
    def __init__(self):
        self.pos_head = [random.choice(range(10,w//k-10)), random.choice(range(10,h//k-10))]
        self.body=[[self.pos_head[0]-1,self.pos_head[1]]]
        self.length = len(self.body)+1
        self.speedx = 0
        self.speedy = 0

    def move(self):
        self.length = len(self.body)+1
        if self.length > 1 and (self.speedx != 0 or self.speedy != 0):
            for part in range(self.length-2,0,-1):
                self.body[part] = self.body[part-1]
            self.body[0] = self.pos_head[:]
        self.pos_head[0] += self.speedx
        self.pos_head[1] += self.speedy


    def draw(self):
        pygame.draw.rect(screen,(255,155,255), (self.pos_head[0]*k, self.pos_head[1]*k, k, k))
        for part in self.body:
            pygame.draw.rect(screen, (100, 155, 255), (part[0] * k, part[1] * k, k, k))



class Grid:
    def __init__(self):
        self.grid = [[0 for j in range(w//k)] for _ in range(h//k)]

    def draw(self):
        for column in range(w//k):
            pygame.draw.line(screen,(0,0,0), (column*k, 0), (column*k, h), 1)

        for row in range(w//k):
            pygame.draw.line(screen,(0,0,0), (0, row*k), (w, row*k), 1)

        for column in range(len(self.grid)):
            for row in range(len(self.grid[column])):
                if self.grid[column][row] == 1:
                    pygame.draw.rect(screen,(255,30,27), (column*k+k//4, row*k+k//4, k//2,k//2))

    def get_by_pos(self, pos):
        return pos[0]//k, pos[1] // k

    def create_food(self):
        x = random.choice(range(w//k))
        y = random.choice(range(h//k))

        self.grid[y][x] = 1

class EventsHandling:
    def __init__(self, **kwargs):
        print(kwargs)
        self.kwargs = kwargs
        self.move_cnt = 0

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

            if self.move_cnt >= 6:
                snake.move()
                self.move_cnt = 0

            self.move_cnt += 1

            if 'grid' in self.kwargs:
                grid = self.kwargs['grid']

                for column in range(len(grid.grid)):
                    for row in range(len(grid.grid[column])):
                        if grid.grid[column][row] == 1 and snake.pos_head == [column,row]:
                            snake.body.append(snake.body[-1])
                            grid.grid[column][row] = 0
                            grid.create_food()



if __name__=='__main__':
    win = Win()