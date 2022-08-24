import pyautogui, time
import mss
import mss.tools
import numpy as np
import timeit

#trying to click on window, and then move mouse back to original position 
#while having active window stay the same
def myclick(x, y, button):
	orig = pyautogui.position()
	print(orig)
	#pyautogui.click(x, y, button = 'left')
	pyautogui.click(x, y, button = 'left')
	pyautogui.keyDown('command')
	pyautogui.keyDown('tab')
	pyautogui.keyUp('command')
	pyautogui.keyUp('tab')
	pyautogui.moveTo(orig)

#checking if my in game inventory is full
#take a 1pi (i think actually 2x2pi) screenshot of a location in my screen
#and comparing to reference color
def isFull():
	with mss.mss() as sct:
		#monitor = {"top": 0, "left": 0, "width": 1680, "height": 1050}
		monitor = {"top": 865, "left": 801, "width": 1, "height": 1}
		sct_img = sct.grab(monitor)
		#plt.imshow(sct_img)
		#plt.show()

		if np.linalg.norm(np.array(sct_img.raw)[0:3] - [40,  52,  61]) < 5:
			return False
		else:
			return True

#clicking and walking to places on screen
def bankiron():
	myclick(369.49609375, 158.75, 'left')
	print(1)
	time.sleep(11)

	myclick(262.92578125, 182.61328125, 'left')
	print(2)
	time.sleep(13)

	myclick(429.35546875, 216.98828125, 'left')
	print(3)
	time.sleep(13)

	myclick(671.1484375, 299.94140625, 'left')
	print(4)
	time.sleep(13)


	#bank
	myclick(515.8515625,336.4296875, 'left')
	myclick(515.8515625,336.4296875, 'left')
	print(6)
	time.sleep(10)


	#bank all inventory
	myclick(497.62109375,771.80078125, 'left')
	print(7)
	time.sleep(1)


	myclick(708.37890625,178.30859375, 'left')
	print(8)
	time.sleep(13)

	myclick(752.55859375,198.5390625, 'left')
	print(9)
	time.sleep(13)

	myclick(775.41796875,198.078125, 'left')
	print(10)
	time.sleep(13)

	myclick(793.27734375,189.12890625, 'left')
	print(11)
	time.sleep(13)

	myclick(308.7734375,597.93359375, 'left')
	time.sleep(13)
	print(8)

#check if pixel on ore is colored, and click when color changes from gray to iron color
#frequency of checking ~10hz, but if maxed out could be like ~30 (300?)
def mine():
	prevIron = False
	isIron = False
	full = False
	counter = 0
	while full == False:
		start = timeit.default_timer()
		with mss.mss() as sct:
			#monitor = {"top": 0, "left": 0, "width": 1680, "height": 1050}
			monitor = {"top": 525, "left": 421, "width": 1, "height": 1}
			sct_img = sct.grab(monitor)
			#plt.imshow(sct_img)
			#plt.show()			
		stop = timeit.default_timer()
		#print(stop - start)
		if np.linalg.norm(np.array(sct_img.raw)[0:3]-[36,38,80]) < np.linalg.norm(np.array(sct_img.raw)[0:3]-[77,77,84]):
			isIron = True
		else:
			isIron = False

		if isIron == True and prevIron == False:
			myclick(421, 525, 'left')
		prevIron = isIron
		time.sleep(0.1 - stop + start)
		#print('Time:', stop-start)
		counter = counter + 1
		#if counter == 20:
		full = isFull()
		#iron 36 38 80
		#gray 77 77 84

