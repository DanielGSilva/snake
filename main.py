import pygame
import numpy as np
import time

def main ():
    board, snake = initBoard((10, 10))
    
    pygame.init()
    initializeBoardDisplay()
    
    while True:
        print(board, snake)
        board, snake, lost = advanceSnake(board, snake)
        
        if (lost):
            break
        
        time.sleep(1)
    
    print(board, snake)
    return

def initBoard(dimensions):
    #initialize board with empty spaces
    board = np.zeros(dimensions, dtype=int)
    
    #put snake on the center of the board, with head represented by 1 and body represented by 2
    center = ((int)(dimensions[0]/2), (int)(dimensions[1]/2))
    board[center] = 1
    board[center[0]][center[1]-1] = 2
    
    #put apple, represented by 3, on a random empty space
    board = generateApple(board)
    
    #initialize snake positions, direction and loss condition
    snake = ([center, (center[0], center[1]-1)], 'right')
    
    return board, snake
    
def generateApple(board):
    while True:
        np.random.seed((int) (time.time()))
        
        pos = (np.random.randint(0, len(board)), np.random.randint(0, len(board[0])))
        
        if (board[pos] == 0):
            board[pos] = 3
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
        
    #check if snake hits outer wall or own body
    if (next[1] >= len(board[0]) or board[next] == 2):
        return board, snake, True
        
    #TODO: check if snake eats apple
    
    #move head and tail
    board[next] = 1
    board[body[0]] = 2
    board[body[-1]] = 0
    body = [next] + body[:-1]
    
    return board, (body, direction), False
    
def initializeBoardDisplay():
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Snake')
    
    screen.fill((50, 200, 50))
    pygame.display.flip()
    
    return screen
    
main()