from time import sleep
from random import choice, uniform

from picamera.array import PiRGBArray
from picamera import PiCamera



class Camera:
    
    def __init__(self, training_mode):
        self.training_mode = training_mode
        self.camera = PiCamera()
        self.camera.resolution = (128, 128)
        self.camera.framerate = 30
        self.camera.rotation = 270
        self.capture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.stream = self.camera.capture_continuous(self.capture,
                                                     format='rgb',
                                                     use_video_port=True)
        if training_mode:
            sleep(5)
            self.camera.shutter_speed = self.camera.exposure_speed
            self.camera.exposure_mode = 'off'
            self.base_awb = self.camera.awb_gains
            self.camera.awb_mode = 'off'


    def next_frame(self):
        self.capture.truncate(0)
        if self.training_mode:
            self.camera.iso = choice([100, 200, 320, 400, 500, 640, 800])
            awb_r = max(0., uniform(-.5, .5) + self.base_awb[0])
            awb_b = max(0., uniform(-.5, .5) + self.base_awb[1])
            self.camera.awb_gains = (awb_r, awb_b)

        frame = self.stream.next().array
        return frame
