import matplotlib.pyplot as plt
import random
import time

letters = [
'A',
'B',
'C',
'D',
'E',
'F',
'G',
]
fingers = [
'1',
'2',
'3',
'4',
'5'
]
hands = [
'L',
'R']


# params
display_type = 'matplotlib'
num_notes = 30
delay = 6


if display_type == 'console':
	for note in range(num_notes):
		n = random.choice(letters)
		print('\n\n\n\n\n\n\n\n\n\n\n\n{}'.format(n))
		time.sleep(delay)
elif display_type == 'matplotlib':
	fig, ax = plt.subplots(figsize=(10,10))
	plt.show(block=False)

	for note in range(num_notes):
		plt.cla()
		n = random.choice(letters)
		#f = random.choice(fingers)
		#h = random.choice(hands)
		f = ''
		h = ''
		plt.text(0.3, 0.5, '{} {} {}'.format(h, f, n), fontsize=100)
		plt.pause(delay)



