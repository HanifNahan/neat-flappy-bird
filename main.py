import pygame
import neat
import time
import random
import os
from bird import Bird
from pipe import Pipe
from ground import Ground

window_height = 800
window_width = 500
pygame.font.init()

bg_image = pygame.transform.scale2x(
    pygame.image.load(os.path.join('images', 'bg.png')))
font = pygame.font.SysFont('comicsans', 50, True)


def draw_window(win, bird, pipes, ground, score):
    win.blit(bg_image, (0, 0))
    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
    ground.draw(win)
    text = font.render("Score:" + str(score), 1, (255,255,255))
    win.blit(text, (window_width - 10 - text.get_width(), 10))
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    pipes = [Pipe(600)]
    ground = Ground(730)
    win = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()
        add_pipe = False
        remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.pipe_top.get_width() < 0:
                remove.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        for r in remove:
            pipes.remove(r)
        if bird.y + bird.image.get_height() >= 730:
            pass
        ground.move()
        draw_window(win, bird, pipes, ground, score)
    pygame.quit()
    quit()


main()
