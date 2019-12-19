import pygame
import random
import msvcrt as m
import json
import math
import time

pygame.init()

size = w, h, = 900, 900
k = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


def wait():
    return m.getch()


def func(n):
    if n < 0:
        return 0
    return n


def sigmoid(n):
    return 1 / (1 + math.exp(-n))


class Drawing:
    def __init__(self):
        pass

    def drawing(self, **kwargs):
        screen.fill((50, 50, 50))

        for obj in kwargs:
            if obj == 'snake':
                for i in kwargs[obj]:
                    i.draw()
            else:
                kwargs[obj].draw()

        pygame.display.flip()


class Snake:
    def __init__(self):
        self.pos_head = [random.choice(range(10,40)), random.choice(range(10,40))]

        self.body = [[self.pos_head[0], self.pos_head[1]+1],[self.pos_head[0], self.pos_head[1]+2],[self.pos_head[0], self.pos_head[1]+3],[self.pos_head[0], self.pos_head[1]+4]]

        # self.pos_head = [random.choice(range(5, w // k - 10)), random.choice(range(5, h // k - 10))]
        # self.body = [[self.pos_head[0] - 1, self.pos_head[1]], [self.pos_head[0] - 2, self.pos_head[1]],
        #              [self.pos_head[0] - 3, self.pos_head[1]], [self.pos_head[0] - 4, self.pos_head[1]]]

        self.length = len(self.body) + 1
        self.speedx = 0
        self.speedy = 1
        self.score = 0
        self.k = 1
        file = open('dnk.json', mode='r')
        self.near_let = file.read()
        file.close()
        file = open('dnk2.json', mode='r')
        self.near_food = file.read()
        self.died = False
        file.close()
        file = open('dnk3.json', mode='r')
        self.near_me = file.read()
        file.close()

        self.steps = {
            'a': 0,
            'd': 1,
            'w': 2,
            's': 3
        }

        if len(self.near_let) < 2:
            self.near_let = [
                [[0, 0, 0, 0, 0] for i in
                 range(11)] for j in range(11)]
            self.near_let[5][4] = [-100, 0, 0, 0, 0]
            self.near_let[5][6] = [0, -100, 0, 0, 0]
            self.near_let[4][5] = [0, 0, -100, 0, 0]
            self.near_let[6][5] = [0, 0, 0, -100, 0]

        else:
            self.near_let = json.loads(self.near_let)

        if len(self.near_food) < 2:
            self.near_food = [
                [[0, 0, 0, 0, 0] for i in
                 range(11)] for j in range(11)]

        else:
            self.near_food = json.loads(self.near_food)

        if len(self.near_me) < 2:
            self.near_me = [
                [[0, 0, 0, 0, 0] for i in
                 range(11)] for j in range(11)]

            self.near_me[5][4] = [-100, 0, 0, 0, 0]
            self.near_me[5][6] = [0, -100, 0, 0, 0]
            self.near_me[4][5] = [0, 0, -100, 0, 0]
            self.near_me[6][5] = [0, 0, 0, -100, 0]


        else:
            self.near_me = json.loads(self.near_me)

        self.near_me[5][4] = [-10000, 0, 0, 0, 0]
        self.near_me[5][6] = [0, -10000, 0, 0, 0]
        self.near_me[4][5] = [0, 0, -10000, 0, 0]
        self.near_me[6][5] = [0, 0, 0, -10000, 0]

        self.near_let[5][4] = [-10000, 0, 0, 0, 0]
        self.near_let[5][6] = [0, -10000, 0, 0, 0]
        self.near_let[4][5] = [0, 0, -10000, 0, 0]
        self.near_let[6][5] = [0, 0, 0, -10000, 0]

        self.lifes = 200
        self.time = 0

    def move(self):
        if not self.died:
            self.time = 0
            self.time += 1
            self.length = len(self.body) + 1
            if self.length > 1 and (self.speedx != 0 or self.speedy != 0):
                for part in range(self.length - 2, 0, -1):
                    self.body[part] = self.body[part - 1]
                self.body[0] = self.pos_head[:]
            self.pos_head[0] += self.speedx
            self.pos_head[1] += self.speedy
            self.lifes -= 1

    def look_around(self):
        pass  # TODO

    def draw(self):
        if not self.died:
            for part in self.body:
                pygame.draw.rect(screen, (90, 140, 230), (part[0] * k, part[1] * k, k, k))
            pygame.draw.rect(screen, (230, 140, 230), (self.pos_head[0] * k, self.pos_head[1] * k, k, k))

    def train(self, want_to, need_to):
        if not self.died:
            if need_to == False:
                if want_to == 'w' and self.speedy != 1:
                    self.speedy = -1
                    self.speedx = 0

                elif want_to == 'a' and self.speedx != 1:
                    self.speedy = 0
                    self.speedx = -1

                elif want_to == 's' and self.speedy != -1:
                    self.speedy = 1
                    self.speedx = 0

                elif want_to == 'd' and self.speedx != -1:
                    self.speedy = 0
                    self.speedx = 1

    def do_choice(self):
        if not self.died:
            a = 0
            d = 0
            w = 0
            s = 0
            self.near_me[5][5] = [0, 0, 0, 0, 5]
            for i in self.near_food:
                for j in i:
                    if j[4] == 1:
                        a += j[0]
                        d += j[1]
                        w += j[2]
                        s += j[3]

            for i in self.near_let:
                for j in i:
                    if j[4] == 2:
                        a += j[0]
                        d += j[1]
                        w += j[2]
                        s += j[3]

            for i in self.near_me:
                for j in i:
                    if j[4] == 5:
                        a += j[0]
                        d += j[1]
                        w += j[2]
                        s += j[3]

            # print(w,a,s,d)

            if a >= d and a >= w and a >= s:
                # print('a')
                return 'a'

            elif d >= a and d >= w and d >= s:
                # print('d')
                return 'd'

            elif w >= a and w >= d and w >= s:
                # print('w')
                return 'w'

            elif s >= a and s >= d and s >= w:
                # print('s')
                return 's'

            else:
                return random.choice('wasd')


class Grid:
    def __init__(self):
        hlp = [0 for _ in range(50)]
        hlp.append(2)
        self.grid = [[random.choice(hlp) for j in range(w // k)] for _ in range(h // k)]
        self.last_food = None
        self.food_on_grid = 0
        # self.grid_items = {
        #     0: None,
        #     1: 'food'
        # }

    def draw(self):
        for column in range(w // k):
            pygame.draw.line(screen, (80, 80, 80), (column * k, 0), (column * k, h), 1)

        for row in range(w // k):
            pygame.draw.line(screen, (80, 80, 80), (0, row * k), (w, row * k), 1)

        for column in range(len(self.grid)):
            for row in range(len(self.grid[column])):
                if self.grid[column][row] == 1:
                    pygame.draw.rect(screen, (205, 30, 27), (column * k + k // 4, row * k + k // 4, k // 2, k // 2))

                elif self.grid[column][row] == 2:
                    pygame.draw.rect(screen, (205, 70, 105), (column * k, row * k, k, k))

    def get_by_pos(self, pos):
        return pos[0] // k, pos[1] // k

    def create_food(self):
        x = random.choice(range(w // k))
        y = random.choice(range(h // k))
        self.last_food = [x, y]
        self.grid[y][x] = 1
        self.food_on_grid += 1

    def what_is_near(self, pos, snake, scan_radius=5):
        scan_radius = int(scan_radius)
        # scan_pos = [func(pos[0] - scan_radius), func(pos[1] - scan_radius)]
        scan_pos = [pos[0], pos[1]]
        scan_res = [[0 for _ in range(scan_radius * 2 + 1)] for __ in range(scan_radius * 2 + 1)]
        for y in range(-scan_radius, scan_radius + 1):
            for x in range(-scan_radius, scan_radius + 1):
                if pos[1] + y > len(self.grid) - 1 or pos[1] + y < 0 or pos[0] + x > len(self.grid) - 1 or pos[
                    0] + x < 0 or self.grid[pos[0]+x][pos[1]+y] == 2:
                    scan_res[y + 5][x + 5] = 2
                elif self.grid[pos[0] + x][pos[1] + y] == 1:
                    scan_res[y + 5][x + 5] = 1

                elif [x + pos[0], y + pos[1]] in snake.body:
                    scan_res[y + 5][x + 5] = 5

                if x == 0 and y == 0:
                    scan_res[5][5] = 5

        # for i in scan_res:
        #     print(i)
        # print()

        return scan_res


class Controller:
    def __init__(self):
        self.move_cnt = 0
        self.food_cnt = 0
        self.event = True
        self.grid = Grid()
        self.grid.create_food()
        self.snakes = [Snake() for _ in range(10)] # SNAKES COUNT
        self.canvas = Drawing()
        self.cnt = 0
        self.continiue = True

        self.sc_cnt = 0

        self.update()

    def update(self):
        self.mx = 0
        best_food = self.snakes[0].near_food
        best_let = self.snakes[0].near_let
        best_me = self.snakes[0].near_me
        while self.event:
            clock.tick(100)
            comp = sorted(self.snakes, key=lambda x: x.score)[-1]
            if self.mx < comp.score:
                self.mx = comp.score
                print(self.mx, 'MAX')
                best_food = comp.near_food
                best_let = comp.near_let
                best_me = comp.near_me


                # file = open('dnk.json', mode='w')
                # file.writelines(str(best_let))
                # file.close()
                #
                # file = open('dnk2.json', mode='w')
                # file.writelines(str(best_food))
                # file.close()
                #
                # file = open('dnk3.json', mode='w')
                # file.writelines(str(best_me))
                # file.close()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.event = False
                    for snake in range(len(self.snakes)):
                        print(snake)
                        print('FOOD:\n', self.snakes[snake].near_food)
                        print('LETS:\n', self.snakes[snake].near_let)
                        print('ITSELF:\n', self.snakes[snake].near_me)
                        print()
                        print()

                    print('WRITED\n', 'food:\n', best_food, '\nlet:\n', best_let, '\nitself:\n', best_me)

                if e.type == pygame.MOUSEBUTTONDOWN:
                    print(self.grid.get_by_pos(pygame.mouse.get_pos()))

            for self.snake in self.snakes:

                nr = self.grid.what_is_near(self.snake.pos_head, self.snake)
                for i in range(len(self.snake.near_let)):
                    for j in range(len(self.snake.near_let[i])):
                        self.snake.near_let[j][i][4] = nr[j][i]
                        self.snake.near_food[j][i][4] = nr[j][i]
                        self.snake.near_me[j][i][4] = nr[j][i]

                ch = self.snake.do_choice()

                self.snake.train(ch, False)

                self.events_handling()

            self.canvas.drawing(snake=self.snakes, grid=self.grid)

            # time.sleep(5)

    def events_handling(self):
        # self.move_cnt += 1
        # if self.move_cnt >= 6:
        self.snake.move()
        self.move_cnt = 0
        self.food_cnt += 1
        self.food_again = 0
        self.sc_cnt += 1
        if self.food_cnt >= 1 and self.grid.food_on_grid <= 500:
            self.food_cnt = 0
            self.grid.create_food()
            # print(self.sc_cnt, 'CNTR')
            # print(clock.get_fps(), 'FPS')

        for column in range(len(self.grid.grid)):
            for row in range(len(self.grid.grid[column])):
                if self.grid.grid[column][row] == 1 and self.snake.pos_head == [column, row]:
                    if len(self.snake.body) == 0:
                        self.snake.body.append(self.snake.pos_head)
                    else:
                        self.snake.body.append(self.snake.body[-1])
                    self.grid.grid[column][row] = 0
                    self.grid.food_on_grid -= 1
                    self.snake.lifes = 180
                    self.snake.score += 1

                if self.grid.grid[column][row] == 1:
                    self.food_again += 1

        if self.snake.pos_head in self.snake.body or (
                self.snake.pos_head[0] >= w // k or self.snake.pos_head[0] < 0 or self.snake.pos_head[
            1] >= h // k or
                self.snake.pos_head[1] < 0) or self.grid.grid[self.snake.pos_head[0]][
            self.snake.pos_head[1]] == 2 or self.snake.lifes <= 0:
            self.snakes.remove(self.snake)
            self.snakes.append(Snake())

        # if self.sc_cnt >= 5000 and self.snake.length <= 10:
        #     file = open('dnk.json', mode='w')
        #     file.writelines(str(self.snake.near))
        #     file.close()
        #     return self.__init__()

        self.grid.food_on_grid = self.food_again

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


if __name__ == '__main__':
    app = Controller()
