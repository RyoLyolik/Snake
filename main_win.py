import pygame
import random

pygame.init()

size = w, h, = 900, 900
k = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


class Drawing:
    def __init__(self):
        pass

    def drawing(self, **kwargs):
            screen.fill((50,50,50))

            for obj in kwargs:
                kwargs[obj].draw()

            pygame.display.flip()

class Snake:
    def __init__(self):
        self.pos_head = [random.choice(range(10,w//k-10)), random.choice(range(10,h//k-10))]
        self.body=[[self.pos_head[0]-1,self.pos_head[1]],[self.pos_head[0]-2,self.pos_head[1]]]
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
        for part in self.body:
            pygame.draw.rect(screen, (90, 140, 230), (part[0] * k, part[1] * k, k, k))
        pygame.draw.rect(screen, (230, 140, 230), (self.pos_head[0] * k, self.pos_head[1] * k, k, k))



class Grid:
    def __init__(self):
        self.grid = [[0 for j in range(w//k)] for _ in range(h//k)]

    def draw(self):
        for column in range(w//k):
            pygame.draw.line(screen,(80,80,80), (column*k, 0), (column*k, h), 1)

        for row in range(w//k):
            pygame.draw.line(screen,(80,80,80), (0, row*k), (w, row*k), 1)

        for column in range(len(self.grid)):
            for row in range(len(self.grid[column])):
                if self.grid[column][row] == 1:
                    pygame.draw.rect(screen,(205,30,27), (column*k+k//4, row*k+k//4, k//2,k//2))

    def get_by_pos(self, pos):
        return pos[0]//k, pos[1] // k

    def create_food(self):
        x = random.choice(range(w//k))
        y = random.choice(range(h//k))

        self.grid[y][x] = 1

class Controller:
    def __init__(self):
        self.move_cnt = 0
        self.event = True
        self.grid = Grid()
        self.grid.create_food()
        self.snake = Snake()
        self.canvas = Drawing()

        self.update()

    def update(self):
        while self.event:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.event = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    print(self.grid.get_by_pos(pygame.mouse.get_pos()))

            self.key_events()
            self.events_handling()

            self.canvas.drawing(snake=self.snake, grid=self.grid)

    def events_handling(self):
        self.move_cnt += 1
        if self.move_cnt >= 6:
            self.snake.move()
            self.move_cnt = 0

        for column in range(len(self.grid.grid)):
            for row in range(len(self.grid.grid[column])):
                if self.grid.grid[column][row] == 1 and self.snake.pos_head == [column,row]:
                    self.snake.body.append(self.snake.body[-1])
                    self.grid.grid[column][row] = 0
                    self.grid.create_food()


        if self.snake.pos_head in self.snake.body or (self.snake.pos_head[0] >= w//k or self.snake.pos_head[0] < 0 or self.snake.pos_head[1] >= h//k or self.snake.pos_head[1] < 0):
            print('Your score:',self.snake.length-3)
            return self.__init__()


    def key_events(self, e=None):
        if pygame.key.get_pressed()[pygame.K_a] and self.snake.speedx != 1:
            self.snake.speedx = -1
            self.snake.speedy = 0

        elif pygame.key.get_pressed()[pygame.K_d] and self.snake.speedx != -1:
            self.snake.speedx = 1
            self.snake.speedy = 0

        elif pygame.key.get_pressed()[pygame.K_s] and self.snake.speedy != -1:
            self.snake.speedy = 1
            self.snake.speedx = 0

        elif pygame.key.get_pressed()[pygame.K_w] and self.snake.speedy != 1:
            self.snake.speedy = -1
            self.snake.speedx = 0


if __name__=='__main__':
    app = Controller()