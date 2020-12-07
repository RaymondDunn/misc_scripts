import PIL.ImageGrab
from PIL import Image
import numpy as numpy
import matplotlib.pyplot as plt
import pyautogui, time
import timeit
from pymouse import PyMouse, PyMouseEvent


m = PyMouse()


class printxy(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        '''Print Fibonacci numbers when the left click is pressed.'''
        #if button == 1:
        if press:
            stop = timeit.default_timer()
            print(x,y)

        #else:  # Exit if any other mouse button used
        #    self.stop()

C = printxy()
C.run()

'''
walk back:
418.26171875 533.43359375
369.49609375 158.75
262.92578125 182.61328125
429.35546875 216.98828125
671.1484375 299.94140625

#right click on bank
502.9765625 335.33984375
496.36328125 362.515625
497.6953125 772.90234375
698.26171875 163.53125
763.8203125 198.3359375
757.07421875 197.20703125
767.83984375 196.5703125
642.72265625 603.41796875
'''