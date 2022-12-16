#!/usr/bin/env python3

import sys
import io
import os
import time
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import picamera.array
import numpy as np
from PIL import Image
import board
import neopixel
import math

#np.set_printoptions(threshold=sys.maxsize)
stream = io.BytesIO()

matrix_width  = 16
matrix_height = 16
matrix_size = (matrix_width,matrix_height) #x|columns|width,y|rows|height

pixel_pin = board.D18
num_pixels = matrix_width*matrix_height
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# clear screen
pixels.fill((0, 0, 0))
pixels.show()

# camera initialization
cam = PiCamera()
cam.contrast=100 #Default:0
cam.iso = 100 #Default:0
#cam.brightness=10 #Default:50
#cam.meter_mode = 'matrix' #Default:Average
sleep(2)
cam.shutter_speed = cam.exposure_speed
g = cam.awb_gains
cam.awb_mode = 'off'
cam.awb_gains = g
cam.hflip = True
#cam.resolution = (64,64)

#an RGB image with dimensions x and y would produce an array with shape (y, x, 3)
rawCapture = PiRGBArray(cam, size=(matrix_size[1], matrix_size[0])) #https://picamera.readthedocs.io/en/release-1.13/api_array.html

try:
  for frame in cam.capture_continuous(rawCapture, format='rgb', use_video_port=True, resize=(matrix_size[1], matrix_size[0])):
    #print('Captured %dx%d image as ' % (frame.array.shape[1], frame.array.shape[0]), frame.array.shape, " as (rows, columns, plane)")    
    #print(frame.array)
    
    #Current pixel position
    pix = 0
    for i in range(matrix_size[0]):
      # Flip every other row for zig-zag/serpentine LED wiring
      if (i%2==0):
        for j in reversed(range(matrix_size[1])):
          pixels[pix] = (frame.array[i,j][0],frame.array[i,j][1],frame.array[i,j][2])
          pix = pix + 1
      else:
        for j in range(matrix_size[1]):
          pixels[pix] = (frame.array[i,j][0],frame.array[i,j][1],frame.array[i,j][2])
          pix = pix + 1
    
    pixels.show()

    """    
    input = np.frombuffer(frame.getvalue(), dtype=np.uint8)
    image = Image.frombuffer('RGB', (64,64), input)
    image.save("image_" + str(i) + ".jpg")
    print("Saved image #", i)
    sleep(1)
    i=i+1
    """
    
    frame.truncate(0)
    frame.seek(0)

except SystemExit:
  pixels.fill((0, 0, 0))
  pixels.show()
  cam.close()
  os._exit(0)
except KeyboardInterrupt:
  pixels.fill((0, 0, 0))
  pixels.show()
  cam.close()
  os._exit(0)
# except:
#   print("Error:", sys.exc_info()[0])
#   os._exit(0)
