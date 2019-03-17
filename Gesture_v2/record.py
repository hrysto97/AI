from time import time, sleep
from sys import argv, exit, stdout
from cPickle import load, dump
from os.path import exists
from os import getenv
import pygame
from camera import Camera



SHOW_UI = getenv("DISPLAY")

if SHOW_UI:
    pygame.init()

def main():
    if len(argv) != 3:
        exit(1)
    name = argv[1]
    seconds = int(argv[2])

    camera = Camera(training_mode=True)
    record(camera, name, seconds)


def status(text):
    if SHOW_UI:
        pygame.display.set_caption(text)
    stdout.write('\r%s' % text)
    stdout.flush()


def record(camera, filename, seconds):
    """ Record from the camera """

    if SHOW_UI:
        pygame.display.init()
        pygame.display.set_caption('Loading...')
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    delay = 0 
    started = time()

    frames = []
    started = time()
    while time() - started < seconds:
        frame = camera.next_frame()
        frames.append(frame)

        if SHOW_UI:
            surface = pygame.surfarray.make_surface(frame)
            screen.blit(pygame.transform.scale(surface, (512, 512)), (0, 0))
            pygame.display.flip()
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    exit(1)

    print('')

    if exists(filename):
        print("%s already exists, merging datasets" % filename)
        existing = load(open(filename, 'rb'))
        frames += existing

    stdout.write('Writing %d frames to %s... ' % (len(frames), filename))
    stdout.flush()
    dump(frames, open(filename, 'wb'))
    print('done.')


if __name__ == '__main__':
    main()
