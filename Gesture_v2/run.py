from sys import argv, stderr, exit
from os import getenv
import time
import numpy as np
from tensorflow import keras

from camera import Camera
from pinet import PiNet


import requests
import musicplay

url_switch_on  = 'http://172.26.17.196/LED=ON'
url_switch_off  = 'http://172.26.17.196/LED=OFF'

SMOOTH_FACTOR = 0.8

SHOW_UI = getenv("DISPLAY")

if SHOW_UI:
    import pygame


def main():
    if len(argv) != 2 or argv[1] == '--help':
        exit(1)

    model_file = argv[1]

    extractor = PiNet()

    classifier = keras.models.load_model(model_file)

    camera = Camera(training_mode=False)

    if SHOW_UI:
        pygame.display.init()
        pygame.display.set_caption('Loading')
        screen = pygame.display.set_mode((512, 512))

    smoothed = np.ones(classifier.output_shape[1:])
    smoothed /= len(smoothed)
    
    isLampOn = False
    last_selected = None
    inRoom = False
    
    print('Now running!')
    while True:
        raw_frame = camera.next_frame()

        z = extractor.features(raw_frame)

        classes = classifier.predict(np.array([z]))[0]

        smoothed = smoothed * SMOOTH_FACTOR + classes * (1.0 - SMOOTH_FACTOR)
        selected = np.argmax(smoothed)
        
        summary = 'Class %d [%s]' % (selected, ' '.join('%02.0f%%' % (99 * p) for p in smoothed))
        stderr.write('\r' + summary)
        
###        #python train.py models/model1.h5  records/lights records/random records/start_music records/stop_music records/greeting records/empty
        try:
            if selected == 0 and last_selected != 0:
                last_selected = 0
                if isLampOn:
                    requests.post(url_switch_off)
                    isLampOn = False
                    
                else:
                    requests.post(url_switch_on)
                    isLampOn = True
              
            elif selected == 1 and last_selected != 1:
                last_selected = 1
                pass
            elif selected == 2 and last_selected != 2:
                last_selected = 2
                musicplay.play_song()
            elif selected == 3 and last_selected != 3:
                last_selected = 3
                musicplay.stop_music()
            elif selected == 4 and last_selected != 4:
                last_selected = 4
                if inRoom == False:
                    musicplay.play_sound_GE()
                    inRoom = True
            elif selected == 5 and last_selected != 5:
                last_selected = 5
                requests.post(url_switch_off)
                inRoom = False
        except Exception:
            print("UNABLE TO SEND COMMAND TO SONOFF\n")

        if SHOW_UI:
            pygame.display.set_caption(summary)
            surface = pygame.surfarray.make_surface(raw_frame)
            screen.blit(pygame.transform.smoothscale(surface, (512, 512)), (0, 0))
            pygame.display.flip()

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    break


if __name__ == '__main__':
    main()
