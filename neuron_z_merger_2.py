import scipy.io
import numpy as np


# example for loading single file
mat = scipy.io.loadmat('registered [XYCTZ] 20190626_RLD_1_FC073_worm2_488_10min_5baseline5_30s_stim_crop_Z6.ome_z.tif.ome_lowPNR_wspace_STRUCT.mat')
c_raw = mat['neuron_struct']['C_raw'][0][0]
A = mat['neuron_struct']['A'][0][0]
#mask = A[:,n];
#mask = reshape(mask, my_h, my_w);

# declare file list of zs to go through
filelist = [
'lolz1.mat',
'lolz2.mat',
]

#### iinitial figure setup
fig = plt.figure('Neuron Z Merger', figsize=(9, 7))
original_traces_ax = fig.add_subplot(2,3,1)
normed_traces_ax = fig.add_subplot(2,3,2)
traces_diff_matrix_ax = fig.add_subplot(2,3,3)
xy_pos_ax = fig.add_subplot(2,3,4)
xy_pos_diff_matrix_ax = fig.add_subplot(2,3,5)


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


# function for calculating difference score between two traces
def calculate_traces_diff(traces_matrix):

    # initialize output matrix
    num_n = xy_matrix.shape[0]
    traces_diff_score = np.ones((num_n, num_n)) * 9999

    # sum
    for x in range(0, num_n):
        for y in range(x, num_n):

            # sum the di
            traces_diff_score[x,y] = np.sum(((traces_matrix[x,:] - traces_matrix[y,:])**2))

    return traces_diff_score


def calculate_xy_diff(xy_vector):
     
    num_n = len(xy_vector)
    xy_diff_score = np.ones((num_n, num_n)) * 200

    # calculate distances
    for n in range(num_n):
        for n2 in range(n + 1, num_n):

            # calculate distance
            dist = np.sqrt(((xy_vector[n,0] - xs[n2,0]) ** 2) + ((xy_vector[n,1] - xy_vector[n2,1]) ** 2))

            # add to distance matrix
            xy_diff_score[n, n2] = dist

    return xy_diff_score


def delete_neuron(n):

    # save info for undo
    deleted_neuron = n
    deleted_xy_score_row = xy_diff_score[:, n]
    delted_xy_score_column  = xy_diff_score[n,:]
    deleted_traces_score_row = traces_diff_score[:,n]
    deleted_traces_score_column = traces_diff_score[n,:]
    deleted_trace = traces_matrix[n, :]
    deleted_trace_normed = traces_normed[n,:]

    # remove from traces matrix and traces_normed
    traces_matrix = np.delete(traces_matrix[n,:])
    traces_normed = np.delete(traces_normed[n,:])

    # delete from xy
    xy_diff_score = np.delete(xy_diff_score, row)
    xy_diff_score = np.delete(xy_diff_score, column)

    # delete from similarity matrix
    traces_diff_score = np.delete(traces_diff_score, row)
    traces_diff_score = np.delete(traces_diff_score, column)


def save_progress():
    pass


"""
def loop_merge():

    xy_mindist = np.amin(dist_matrix)
    while xy_mindist < xy_thresh:

        # get current number of neurons
        num_n = dist_matrix.shape[0] 

        # get minimum distance
        xy_mindist = np.amin(dist_matrix)
        minpair = np.argmin(dist_matrix)
        [n1, n2] = np.unravel_index(minpair, (num_n, num_n), order='C')

        # take the neuron with more signal
        n1_score = np.sum(dist_matrix[n1,:])
        n2_score = np.sum(dist_matrix[n2,:])
        if n1_score > n2_score:
            to_delete = n1
        else:
            to_delete = n2

        # delete the other
        delete_neuron(to_delete)

        # set iterator var
        xy_mindist = np.amin(dist_matrix)
"""


def merge_button_callback()
    # take the neuron with more signal

    pass


# load first z plane and the one below it
current_z = 0
traces_list = []
traces_normed = []
traces_diff_score = []
xy_pos = []
xy_diff_score = []
def load_zs():

    for f in filelist:

        ######### trace data
        # load data from mat files
        mat = scipy.io.loadmat(f)

        # append every individual trace to data struct
        c_raw = mat['neuron_struct']['C_raw'][0][0]
        for t in range(c_raw.shape[0]):
            traces_list.append(c_raw[t, :])

        ######### xy data
        # load data from mat file
        A = mat['neuron_struct']['A'][0][0]

        # get positional info
        xy_pos.append(xys)

    # reshape list into one big array
    ta = np.array(traces_list)
    traces_matrix = np.reshape(ta, (ta.shape[0] * ta.shape[1], ta.shape[2]))

    # get correlation/diff squared score
    traces_diff_score = calculate_traces_diff(traces_matrix)

    # get xy distance score
    xy_vector = np.array(xy_pos)
    xy_diff_score = calculate_xy_diff(xy_vector)


# get putative neurons to merge
def get_putative_merge():

    # returns list of tuples, each containing the index of a neuron that might be worth merging...

    # use xy and a crude measure of similarity of trace?
    
    pass


# start gui
decorate_plots()
load_zs()
neurons_maybe_merge = get_putative_merge()
current_n = 0


# callback for keypress
def press(event):
    print('press', event.key)
    # sys.stdout.flush()
    if event.key == 'left':
        pass
    elif event.key = 'right':
        pass
    else:
        print('Keypress input not recognized...')
        plot_putative_merge(neurons_maybe_merge[current_n])
        # fig.canvas.draw()


# bind keypress
fig.canvas.mpl_connect('key_press_event', press)

# show gui
try:
    plt.show()
    save_progress()

except Exception as err:
    print(err)
    save_progress()