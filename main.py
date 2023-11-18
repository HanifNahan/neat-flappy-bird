import pygame
import neat
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


def draw_window(win, birds, pipes, ground, score):
    win.blit(bg_image, (0, 0))
    for bird in birds:
        bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
    ground.draw(win)
    text = font.render("Score:" + str(score), 1, (255, 255, 255))
    win.blit(text, (window_width - 10 - text.get_width(), 10))
    pygame.display.update()


def main(genomes, config):
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)
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
                pygame.quit()
                quit()
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind = 1
        else:
            run = False
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[birds.index(bird)].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()
        add_pipe = False
        remove = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.pipe_top.get_width() < 0:
                remove.append(pipe)
            pipe.move()
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        for r in remove:
            pipes.remove(r)
        for x, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        ground.move()
        draw_window(win, birds, pipes, ground, score)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
