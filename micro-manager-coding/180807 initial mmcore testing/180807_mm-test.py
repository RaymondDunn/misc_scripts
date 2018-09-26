import MMCorePy
import cv2
import numpy as np
import pylab
import time

mmc = MMCorePy.CMMCore()

config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)

# mmc = MMCorePy.CMMCore()
mmc.enableStderrLog(False)
mmc.enableDebugLog(False)
mmc.setCircularBufferMemoryFootprint(1000)
# mmc.loadDevice(*DEVICE)
# mmc.initializeDevice(DEVICE[0])
mmc.setCameraDevice('AmScope')
# mmc.setProperty('AmScope', 'PixelType', '32bitRGB')

cv2.namedWindow('Video')


mmc.startContinuousSequenceAcquisition(0)
t0 = time.time()
frames_to_grab = 100
while True:
    #grey = mmc.getLastImage()
    if mmc.getRemainingImageCount() > 0:
        #rgb32 = mmc.popNextImage()
        grey = mmc.getLastImage()
        # Efficient conversion without data copying.
        #bgr = rgb32.view(dtype=np.uint8).reshape(
        #    rgb32.shape[0], rgb32.shape[1], 4)[..., :3]
        lol = pylab.array(grey, dtype=pylab.uint8)
        cv2.imshow('Video', lol)
        #pylab.show()
        #time.sleep(1)
    else:
        print('No frame')
    cv2.waitKey(1)
t1 = time.time()
print('total time is {}'.format(t1-t0))

cv2.destroyAllWindows()
mmc.stopSequenceAcquisition()
mmc.reset()



####


import MMCorePy
import time

mmc = MMCorePy.CMMCore()

config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)

mmc.enableStderrLog(False)
mmc.enableDebugLog(False)
mmc.setCircularBufferMemoryFootprint(1000)
mmc.setCameraDevice('AmScope')

#mmc.startContinuousSequenceAcquisition(0)
mmc.startSequenceAcquisition(1000, 0, 0)
t0 = time.time()
frames_to_grab = 1000
for t in range(0, frames_to_grab):
    if mmc.getRemainingImageCount() > 0:
        grey = mmc.getLastImage()
    else:
        print('No frame')
t1 = time.time()
print('total time is {}'.format(t1-t0))

#cv2.destroyAllWindows()
mmc.stopSequenceAcquisition()
mmc.reset()

###

import MMCorePy

mmc = MMCorePy.CMMCore()

config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)
mmc.setCameraDevice('AmScope')
mmc.setCircularBufferMemoryFootprint(30000)
mmc.initializeCircularBuffer()
mmc.getBufferTotalCapacity()

#######

import MMCorePy
import time

# initialize
mmc = MMCorePy.CMMCore()
frames_to_grab = 500

# configure and prep for image acquisition
config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)
mmc.setCameraDevice('AmScope')
mmc.setCircularBufferMemoryFootprint(30000)
# mmc.prepareSequenceAcquisition('AmScope')

# start frame grabbing
print('Curr img count: {}'.format(mmc.getRemainingImageCount()))
t0 = time.time()
mmc.startSequenceAcquisition(frames_to_grab, 0, 0)

while True:
    if mmc.getRemainingImageCount() == frames_to_grab:
        break

t1 = time.time()
print('total time is: {}'.format(t1-t0))

#######

import sys
sys.path.append('C:\\Program Files\\Micro-Manager-2.0beta')
import MMCorePy
import pylab

# initialize core object
mmc = MMCorePy.CMMCore()
config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)
mmc.setCameraDevice('AmScope')

# snap image and show
mmc.snapImage()
rgb32 = mmc.getImage()

# take view of same data... aparently fastest way of doing it
rgb = rgb32.view(dtype=pylab.uint8).reshape(rgb32.shape[0], rgb32.shape[1], 4)[...,2::-1]   

# show
pylab.imshow(rgb)
pylab.show()

