import pygame
import numpy as np
import time

COLOR_GREEN = (50, 200, 50)

EMPTY_SPACE = 0
SNAKE_HEAD = 1
SNAKE_BODY_HORIZONTAL = 2
SNAKE_BODY_VERTICAL = 3
SNAKE_BODY_BOTTOM_LEFT = 4
SNAKE_BODY_BOTTOM_RIGHT = 5
SNAKE_BODY_TOP_LEFT = 6
SNAKE_BODY_TOP_RIGHT = 8
SNAKE_TAIL_UP = 9
SNAKE_TAIL_DOWN = 10
SNAKE_TAIL_RIGHT = 11
SNAKE_TAIL_LEFT = 12
APPLE = 13

def main ():
    boardSize = (10, 10)
    board, snake = initBoard(boardSize)
    
    pygame.init()
    screen = initializeBoardDisplay(board, snake)
    
    while True:
        snake = getKey(snake)
        board, snake, lost = advanceSnake(board, snake)
        
        if (lost):
            break
        
        screen = updateScreen(screen, board, snake)
        pygame.display.flip()
        
        time.sleep(0.5)
    
    return

def initBoard(dimensions):
    #initialize board with empty spaces
    board = np.zeros(dimensions, dtype=int)
    
    #put snake on the center of the board, turned right
    center = ((int)(dimensions[0]/2), (int)(dimensions[1]/2))
    board[center] = SNAKE_HEAD
    board[center[0]][center[1]-1] = SNAKE_TAIL_LEFT
    
    #put apple on a random empty space
    board = generateApple(board)
    
    #initialize snake positions and direction
    snake = ([center, (center[0], center[1]-1)], 'right')
    
    return board, snake
    
def generateApple(board):
    while True:
        np.random.seed((int) (time.time()))
        
        pos = (np.random.randint(0, len(board)), np.random.randint(0, len(board[0])))
        
        if (board[pos] == EMPTY_SPACE):
            board[pos] = APPLE
            return board
        
def advanceSnake(board, snake):
    body = snake[0]
    direction = snake[1]
    
    if (direction == 'right'):
        next = (body[0][0], body[0][1] +1)
    elif (direction == 'left'):
        next = (body[0][0], body[0][1] -1)
    elif (direction == 'up'):
        next = (body[0][0] -1, body[0][1])
    elif (direction == 'down'):
        next = (body[0][0] +1, body[0][1])
        
    #check if snake hits outer wall or itself
    if (not(0 <= next[0] < len(board)) or not(0 <= next[1] < len(board[0])) or SNAKE_HEAD <= board[next] <= SNAKE_TAIL_LEFT):
        return board, snake, True
    
    #check if snake eats apple and progress its body (snake grows in the head)
    if (board[next] == APPLE):
        body = [next] + body
        board = progressBody(board, body)
        board = generateApple(board)
    else:
        board[body[-1]] = EMPTY_SPACE
        body = [next] + body[:-1]
        board = progressBody(board, body)
    
    return board, (body, direction), False

def progressBody(board, body):
    #progress head
    board[body[0]] = SNAKE_HEAD
    
    #progress body
    for i in range(1, len(body)-1):
        if (body[i+1][1] < body[i][1]): #body is coming from left
            if (body[i-1][0] < body[i][0]): #body is going up
                board[body[i]] = SNAKE_BODY_TOP_LEFT
            elif (body[i-1][0] > body[i][0]): #body is going down
                board[body[i]] = SNAKE_BODY_BOTTOM_LEFT
            else: #body is going right
                board[body[i]] = SNAKE_BODY_HORIZONTAL
        elif (body[i+1][1] > body[i][1]): #body is coming from right
            if (body[i-1][0] < body[i][0]): #body is going up
                board[body[i]] = SNAKE_BODY_TOP_RIGHT
            elif (body[i-1][0] > body[i][0]): #body is going down
                board[body[i]] = SNAKE_BODY_BOTTOM_RIGHT
            else: #body is going left
                board[body[i]] = SNAKE_BODY_HORIZONTAL
        elif (body[i+1][0] < body[i][0]): #body is coming from up
            if (body[i-1][1] < body[i][1]): #body is going left
                board[body[i]] = SNAKE_BODY_TOP_LEFT
            elif (body[i-1][1] > body[i][1]): #body is going right
                board[body[i]] = SNAKE_BODY_TOP_RIGHT
            else: #body is going down
                board[body[i]] = SNAKE_BODY_VERTICAL
        elif (body[i+1][0] > body[i][0]): #body is coming from down
            if (body[i-1][1] < body[i][1]): #body is going left
                board[body[i]] = SNAKE_BODY_BOTTOM_LEFT
            elif (body[i-1][1] > body[i][1]): #body is going right
                board[body[i]] = SNAKE_BODY_BOTTOM_RIGHT
            else: #body is going up
                board[body[i]] = SNAKE_BODY_VERTICAL
    
    #progress tail
    if (body[-2][1] < body[-1][1]): #body is going left
        board[body[-1]] = SNAKE_TAIL_RIGHT
    elif (body[-2][1] > body[-1][1]): #body is going right
        board[body[-1]] = SNAKE_TAIL_LEFT
    elif (body[-2][0] < body[-1][0]): #body is going up
        board[body[-1]] = SNAKE_TAIL_DOWN
    elif (body[-2][0] > body[-1][0]): #body is going down
        board[body[-1]] = SNAKE_TAIL_UP
    
    return board
    
def initializeBoardDisplay(board, snake):
    screen = pygame.display.set_mode((len(board)*40, len(board[0])*40))
    pygame.display.set_caption('Snake')
    
    screen = updateScreen(screen, board, snake)
    pygame.display.flip()
    
    return screen

def updateScreen(screen, board, snake):
    screen.fill(COLOR_GREEN)
    for x in range(len(board)):
        for y in range(len(board[0])):
            if (board[(x, y)] == SNAKE_HEAD):
                head = pygame.image.load("graphics/head_" + snake[1] + ".png")
                screen.blit(head, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_BODY_HORIZONTAL):
                body = pygame.image.load("graphics/body_horizontal.png")
                screen.blit(body, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_BODY_VERTICAL):
                body = pygame.image.load("graphics/body_vertical.png")
                screen.blit(body, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_BODY_BOTTOM_LEFT):
                body = pygame.image.load("graphics/body_bottomleft.png")
                screen.blit(body, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_BODY_BOTTOM_RIGHT):
                body = pygame.image.load("graphics/body_bottomright.png")
                screen.blit(body, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_BODY_TOP_LEFT):
                body = pygame.image.load("graphics/body_topleft.png")
                screen.blit(body, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_BODY_TOP_RIGHT):
                body = pygame.image.load("graphics/body_topright.png")
                screen.blit(body, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_TAIL_UP):
                tail = pygame.image.load("graphics/tail_up.png")
                screen.blit(tail, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_TAIL_DOWN):
                tail = pygame.image.load("graphics/tail_down.png")
                screen.blit(tail, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_TAIL_RIGHT):
                tail = pygame.image.load("graphics/tail_right.png")
                screen.blit(tail, (y*40, x*40))
            elif (board[(x, y)] == SNAKE_TAIL_LEFT):
                tail = pygame.image.load("graphics/tail_left.png")
                screen.blit(tail, (y*40, x*40))
            elif (board[(x, y)] == APPLE):
                apple = pygame.image.load("graphics/apple.png")
                screen.blit(apple, (y*40, x*40))
                
    return screen
    
def getKey(snake):
    for event in pygame.event.get(eventtype=pygame.KEYDOWN):
        if event.key == pygame.K_UP:
            pygame.event.clear()
            return (snake[0], "up")
        if event.key == pygame.K_DOWN:
            pygame.event.clear()
            return (snake[0], "down")
        if event.key == pygame.K_RIGHT:
            pygame.event.clear()
            return (snake[0], "right")
        if event.key == pygame.K_LEFT:
            pygame.event.clear()
            return (snake[0], "left")
    
    pygame.event.clear()
    
    return snake

main()