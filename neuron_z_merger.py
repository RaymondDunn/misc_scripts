import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np


# declare file list of zs to go through
filelist = [
'lolz1.mat',
'lolz2.mat',
]

# prepare output data
num_z = len(filelist)
num_n_z0 = 1
num_n_z1 = 1
num_t = 1 

#### iinitial figure setup
fig = plt.figure('Neuron Z Merger', figsize=(9, 7))
original_traces_ax = fig.add_subplot(2,3,1)
normed_traces_ax = fig.add_subplot(2,3,2)
traces_diff_matrix_ax = fig.add_subplot(2,3,3)
xy_pos_ax = fig.add_subplot(2,3,4)
xy_pos_diff_matrix_ax = fig.add_subplot(2,3,5)


# initialize diff matrices and traces
normed_traces_z0 = np.zeros((1,1))
normed_traces_z1 = np.zeros((1,1))
traces_diff_matrix = np.zeros((1,1)) 
xy_pos_diff_matrix = np.zeros((1,1))
def plot_difference_matrices():

	# calculate normed traces
	#normed_traces_z0 = 
	#normed_traces_z1 = 

	# 
	
	# calculate traces difference matrix
	#traces_diff_matrix = 
	#xy_pos_diff_matrix = 

	# plot
	#traces_diff_matrix_ax.imshow(traces_diff)
	#xy_pos_diff_matrix_ax.imshow(xy_pos_diff)
	pass


# load first z plane and the one below it
current_z = 0
traces = []
xy_pos = []
#traces_z0 = np.zeros((1,1))
#traces_z1 = np.zeros((1,1))
#xy_pos_z0 = np.zeros((1,1,1,1))
#xy_pos_z1 = np.zeros((1,1,1,1))
def load_z_and_zplus1(current_z):

	# if there's already a 
	
	# set z plus 1
	zplus1 = current_z + 1
	if zplus1+ 1 > num_z - 1:
		zplus1 = 0

	# load data from mat files
	#traces_z0 = 
	#traces_z1 =  
	#xy_pos_z0 = 
	#xy_pos_z1 = 

	# do computation and plot plots
	plot_difference_matrices()
	goto_next_n("")

	# make a super title
	fig.suptitle('neuron {}, Z: {}, \nneuron {}, Z+1: {}'.format(current_n_z0, filelist[current_z], current_n_z1, filelist[current_z+1]))


# decorate plots
def decorate_plots():

	# set title
	original_traces_ax.set_title('DFF traces')
	normed_traces_ax.set_title('Normalized traces')
	traces_diff_matrix_ax.set_title('Traces sum squares diff matrix')
	xy_pos_ax.set_title('XY positions')
	xy_pos_diff_matrix_ax.set_title('XY position diff matrix')

	# set axes for line plots
	original_traces_ax.set_xlabel('frame')
	original_traces_ax.set_ylabel('dff')
	normed_traces_ax.set_xlabel('frame')
	normed_traces_ax.set_ylabel('min/max normed dff')

	# set axes for position plots
	xy_pos_ax.set_xlabel('x px coord')
	xy_pos_ax.set_ylabel('y px coord')


decorate_plots()

#### buttons
# take z
def submit_merge_z(event):
    print('Taking neuron from z plane')

    # adjust activity mat of other z
    traces_z1[current_n_z1, :] = np.NaN
    # adjust xyz entry

    # recalculate difference matrice
    plot_difference_matrices()



submit_merge_z_ax = plt.axes([0.70, 0.25, 0.15, 0.08])
submit_merge_z_button = Button(submit_merge_z_ax, "Merge and take Z")
submit_merge_z_button.on_clicked(submit_merge_z)

# take z + 1
def submit_merge_z_plus_1(event):
    print('Taking neuron from z+1 plane')
    # adjust activity mat of other z
    traces_z0[current_n_z0, :] = np.NaN
    # adjust xyz entry

    # recalculate matrices
    plot_difference_matrices()


submit_merge_z_plus_1_ax = plt.axes([0.70, 0.15, 0.15, 0.06])
submit_merge_z_plus_1_button = Button(submit_merge_z_plus_1_ax, "Merge and take Z+1")
submit_merge_z_plus_1_button.on_clicked(submit_merge_z_plus_1)

# take neither
def submit_different_neurons(event):
    print('Taking both neurons!')

    # z0 neuron to skip list
    merge_skip_list.append((current_n_z0, current_n_z1))

submit_different_neurons_ax = plt.axes([0.70, 0.05, 0.15, 0.06])
submit_different_neurons_button = Button(submit_different_neurons_ax, "Neurons are different")
submit_different_neurons_button.on_clicked(submit_different_neurons)

# next Z button/callback
def submit_next_z(event):
	current_z += 1

	# apply wrap around
	if current_z > num_z-1:
		current_z =  0
	else if current_z < 0:
		current_z= num_z - 1

	print('Moving onto Zs {} and {}'.format(current_z, current_z+1))

	# load
	load_z_and_zplus1(current_z)

# next N button/callback
current_n_z0 = 0
current_n_z1 = 0
merge_skip_list = []
def goto_next_n(event):

	# take next two neurons to compare based on traces difference and xy difference data
	#current_n_z0 = 
	#current_n_z1 = 

	# if pair of neurons is in merge_skip_list, go to next n!

	# update plot
	# plot raw traces
	original_traces_ax.plot(traces_z0[current_n_z0, :], 'b')
	original_traces_ax.plot(traces_z1[current_n_z1, :], 'r')

	# plot normalized traces
	normed_traces_ax.plot(normed_traces_z0[current_n_z0, :], 'b')
	normed_traces_ax.plot(normed_traces_z1[current_n_z1, :], 'r')

	# plot circles for each roi circles
	#x0 = 
	#y0 = 
	#x1 = 
	#y1 = 
	#plt.circle(x0, y0, 'b')
	#plt.circle(x1, y1, 'r')

	# calculate 
	pass

# set side arrow keys to progress forward/backeward through ns
# set up/down arrow keys to progress through zs



###################
# utility function to save after gui closes
def save_progress():

	# save workspace vars... e.g.
	# save overall activity matrices with nans in them
	# save pos data
	# save n/z info
	pass

def submit_load_merging_session(event):

	# load overall activity matrices
	# load pos data
	# load n/z info
	pass

submit_load_merging_session_ax = plt.axes([0.90, 0.15, 0.09, 0.06])
submit_load_merging_session_button= Button(submit_load_merging_session_ax, "Load...")
submit_load_merging_session_button.on_clicked(submit_load_merging_session)

def submit_finished_merging(event):

	# combine traces matrices and remove nans
	# save mat as numpy array
	# save xyz pos array etc
	pass

submit_finished_merging_ax = plt.axes([0.90, 0.05, 0.09, 0.06])
submit_finished_merging_button= Button(submit_finished_merging_ax, "Done!")
submit_finished_merging_button.on_clicked(submit_finished_merging)

# load first z
load_z_and_zplus1(current_z)

# show gui
try:
	plt.show()
	save_progress()

except Exception as err:
	print(err)
	save_progress()



