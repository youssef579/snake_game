import curses
from curses import wrapper
from random import randint

class Snake:
    def __init__(self):
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        self.COLOR = curses.color_pair(1)
        self.body = [[len(body) // 2, 2], [len(body) // 2, 3], [len(body) // 2, 4]]
        self.length = 3
        self.CHARACTER = curses.ACS_BLOCK
        self.direction = (0, 1)

    def draw(self, screen):
        for i in range(self.length):
            screen.addch(curses.LINES // 2 - LENGTH // 2 + self.body[i][0], curses.COLS // 2 - 22 + self.body[i][1], self.CHARACTER, self.COLOR)

    def input(self, screen):
        try:
            key = screen.getkey().lower()
        except curses.error:
            return

        if key == 'd' and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == 'a' and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == 'w' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == 's' and self.direction != (-1, 0):
            self.direction = (1, 0)

    def move(self):
        self.body.append((self.body[-1][0] + self.direction[0], self.body[-1][1] + self.direction[1]))
        self.body.pop(0)

    def check_collision(self):
        if self.body[-1][0] <= 0 or self.body[-1][0] >= LENGTH - 1 or self.body[-1][1] <= 0 or self.body[-1][1] >= len(body[0]) - 1 or self.body[-1] in self.body[:-1]:
            return False 
        
        if self.body[-1] == food.position:
            self.body.append((self.body[-1][0] + self.direction[0], self.body[-1][1] + self.direction[1]))
            self.length += 1
            while True:
                food.position = (randint(1, LENGTH - 2), randint(2, len(body[0]) - 3))
                if food.position not in self.body: break    

        return True

    def update(self, screen):
        self.draw(screen)
        self.input(screen)
        self.move()

class Food:
    def __init__(self):
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.curs_set(0)
        self.COLOR = curses.color_pair(2)
        self.CHARACTER = curses.ACS_DIAMOND
        while True:
            self.position = (randint(1, LENGTH - 2), randint(2, len(body[0]) - 3))
            if self.position not in snake.body: break

    def draw(self, screen):
        screen.addch(curses.LINES // 2 - LENGTH // 2 + self.position[0], curses.COLS // 2 - 22 + self.position[1], self.CHARACTER, self.COLOR)

def check_highest_score(window):
    global highest_score

    if snake.length - 3 > highest_score:
        with open('highest_score.txt', 'w') as f:    
            f.write(str(snake.length - 3))

        highest_score = snake.length - 3
        window.addstr("New high score !!!\n", curses.A_BOLD)

try:
    with open('highest_score.txt', 'r') as f:
        highest_score = int(f.read())
except:
    highest_score = 0

body = (
    [*'# # # # # # # # # # # # # # # # # # # # #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'#                                       #'],
    [*'# # # # # # # # # # # # # # # # # # # # #'])

LENGTH = len(body)

food = snake = None

def main(screen):
    global snake, food

    curses.curs_set(0)
    screen.nodelay(True)
    screen.timeout(100)
    curses.use_default_colors()
    curses.noecho()

    snake = Snake()
    food = Food()

    while snake.check_collision():
        screen.clear()
        for i in range(LENGTH):
            screen.addstr(curses.LINES // 2 - LENGTH // 2 + i, curses.COLS // 2 - 22, ''.join(body[i]))

        food.draw(screen)
        snake.update(screen)
        screen.refresh()

    screen.clear()
    screen.refresh()

    newwin = curses.newwin(6, 50)
    newwin.addstr('Game Over!\n')
    check_highest_score(newwin)
    newwin.addstr("Scroe: " + str(snake.length - 3) + '\n')
    newwin.addstr("Highest Score: " + str(highest_score) + '\n')
    newwin.addstr(5, 0, "Press any key to quit...", curses.A_STANDOUT)
    newwin.getch()
    curses.endwin()

wrapper(main)
