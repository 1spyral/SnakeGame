# Luke Zhan
# GUI Project #1

# Description: This program is a template for Snake Game.
# It demonstrates how to move and lengthen the snake.
#########################################
import pygame
import random

pygame.init()

# Load in the custom font
font = pygame.font.SysFont("Comic Sans MS", 30)

WIDTH = 800
HEIGHT = 600

pts = 0 # Amount of apples eaten

WHITE = (255, 255, 255)
Background = (0, 0, 0)
OUTLINE = 0
RED = (255, 0, 0)

# Set screen
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
win.fill(Background)
delay = 100  # Delay is the framerate

# ---------------------------------------#
# snake's properties                    #
# ---------------------------------------#
BODY_SIZE = 20
X_START = int(WIDTH/2)
Y_START = HEIGHT - BODY_SIZE
step = 20
dir = pygame.K_UP # Direction of snake

apple = [pygame.Rect(WIDTH / 2, HEIGHT / 2, BODY_SIZE, BODY_SIZE)]
applecount = 0 # Time since last apple was eaten

seg = [] # Segments

for i in range(3):
    seg.append(pygame.Rect(X_START, Y_START + step * i, BODY_SIZE, BODY_SIZE))
last = None

speed = [0, -step]

# Snake head is orange and body is blue
head = (255, 165, 0)
body = (0, 0, 255)

x2 = 220
y2 = 200
size = 50


# ---------------------------------------#
# function that redraws all objects     #
# ---------------------------------------#
def redraw_win():
    win.fill(Background)
    for i in apple:
        pygame.draw.rect(win, (255, 0, 0), i)
    # Display the score
    count = font.render(str(pts), True, WHITE)
    win.blit(count, (10, 10))
    for i in range(len(seg)):
        color = head if i == 0 else body
        pygame.draw.rect(win, color, seg[i], OUTLINE)


# ---------------------------------------#
# the main program begins here          #
# ---------------------------------------#
print("Use the arrows and the space bar.")
print("Hit ESC to end the program.")
pygame.time.delay(1000)


# Function called when you lose the game
def lose():
    print("You lose")
    pygame.quit()
    quit()


# Apple generator
def generate_apple():
    return pygame.Rect(random.randint(0, 39) * 20, random.randint(0, 29) * 20, BODY_SIZE, BODY_SIZE)


while True:
    pygame.time.delay(delay)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        keys = pygame.key.get_pressed()
        # act upon key events
        if keys[pygame.K_ESCAPE]:
            print("Quit game")
            pygame.quit()
            quit()

        if keys[pygame.K_LEFT] and dir not in [pygame.K_RIGHT, pygame.K_LEFT]:
            speed = [-step, 0]
            dir = pygame.K_LEFT
            break

        elif keys[pygame.K_RIGHT] and dir not in [pygame.K_RIGHT, pygame.K_LEFT]:
            speed = [step, 0]
            dir = pygame.K_RIGHT
            break

        elif keys[pygame.K_UP] and dir not in [pygame.K_UP, pygame.K_DOWN]:
            speed = [0, -step]
            dir = pygame.K_UP
            break

        elif keys[pygame.K_DOWN] and dir not in [pygame.K_UP, pygame.K_DOWN]:
            speed = [0, step]
            dir = pygame.K_DOWN
            break

        elif keys[pygame.K_SPACE]:
            seg.append(last)
            break

    applecount += 1 # Adds to the apple clock

    # move all segments
    last = seg[-1]
    for i in range(len(seg) - 1, 0, -1):  # start from the tail, and go backwards
        seg[i] = seg[i-1]  # every segment takes the coordinates of the previous one
    seg[0] = seg[0].move(speed[0], speed[1])  # move the head

    # Check if snake eats apple
    if (remove := seg[0].collidelist(apple)) != -1:
        del apple[remove]
        pts += 1
        seg.append(last)  # Makes the snake longer
        applecount = 0
        # Every 10 apples, the speed doubles
        if pts % 10 == 0:
            delay //= 2
        while True and len(apple) == 0:
            apple.append(generate_apple())
            if apple[-1].collidelist(seg) == -1:  # Makes sure apple is not on top of snake
                break

    # Check if another apple should be summoned
    if applecount >= 160 * 100/delay:
        applecount = 0
        while True:
            apple.append(generate_apple())
            if apple[-1].collidelist(seg) == -1:  # Makes sure apple is not on top of snake
                break


    # Checks if snake runs into itself
    if seg[0].collidelist(seg[1:]) > -1:
        lose()

    # Checks if snake hits the wall
    if seg[0].y > 600 or seg[0].y < 0 or seg[0].x > 800 or seg[0].x < 0:
        lose()

    # update the screen
    redraw_win()

    # pygame.time.delay(2000)
    pygame.display.update()