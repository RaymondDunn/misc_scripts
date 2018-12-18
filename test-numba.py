from numba import jit
import numpy as np
import time
import tifffile as tf
import pdb
import matplotlib.pyplot as plt


#@jit(nopython=True)
def quantify_peak_centers_sk(frame, xs, ys, roi_rMax=7, roi_quant_pixels=30):
    """

    :param peak_centers: note is mutable
    :return:
    """

    sig = []
    max_pixels = frame.shape[0] * frame.shape[1]

    for r in range(0, len(xs)):

        # grab circle patch around each roi
        x = xs[r]
        y = ys[r]

        # get pixels
        pix = frame[x-roi_rMax:x+roi_rMax, y-roi_rMax:y+roi_rMax]
        #pdb.set_trace()

        # sort and take top pixels
        flat = np.sort(pix.flatten())
        quant = np.mean(flat[-30:])

        # store
        sig.append(quant)

    # return dict with signal set
    return sig


#@jit(nopython=True)
def find_center(frame):

    # do some basic filtering
    # frame = med_threshold(frame)

    fb_threshold_margin = 80

    # apply threshold
    threshold = np.median(frame) + fb_threshold_margin
    frame = (frame > threshold) * frame


    # skipping edge pixels
    sd = frame.shape
    edg = 3
    [x, y] = np.where(frame[edg:sd[0] - edg, edg:sd[1] - edg - 1])

    # initialize outputs
    cent = []
    cent_map = np.zeros(sd)
    x = x + edg - 1
    y = y + edg - 1
    #links_x = []
    #links_y = []
    links_hi = []
    links_vi = []
    xs = []
    ys = []
    #federatedcenters_ind = []
    federatedcentermap = np.zeros(sd)

    for j in range(0, len(y)):
        if (frame[x[j], y[j]] >= frame[x[j] - 1, y[j] - 1]) and \
                (frame[x[j], y[j]] >= frame[x[j] - 1, y[j]]) and \
                (frame[x[j], y[j]] >= frame[x[j] - 1, y[j] + 1]) and \
                (frame[x[j], y[j]] >= frame[x[j], y[j] - 1]) and \
                (frame[x[j], y[j]] >= frame[x[j], y[j] + 1]) and \
                (frame[x[j], y[j]] >= frame[x[j] + 1, y[j] - 1]) and \
                (frame[x[j], y[j]] >= frame[x[j] + 1, y[j]]) and \
                (frame[x[j], y[j]] >= frame[x[j] + 1, y[j] + 1]):

            cent.append([x[j], y[j]])
            cent_map[x[j], y[j]] = cent_map[x[j], y[j]] + 1

            # ridge/mesa consolidation code
            # find horizontal neighbor pixels of equal value
            if (frame[x[j], y[j]] == frame[x[j] - 1, y[j]]):

                links_hi.append(j)
                federatedcentermap[x[j], y[j]] = federatedcentermap[x[j] - 1, y[j]]

            # find horizontal neighbor pixels of equal value
            elif (frame[x[j], y[j]] == frame[x[j], y[j] - 1]):

                links_vi.append(j)
                federatedcentermap[x[j], y[j]] = federatedcentermap[x[j], y[j] - 1]

            else:

                # federatedcenters['ind'].append(sub2ind(frame.shape, x[j], y[j]))
                # federatedcentermap[x[j], y[j]] = sub2ind(frame.shape, x[j], y[j])
                # print('x: {}; y: {}'.format(x[j], y[j]))
                # print('ravel: {}'.format(np.ravel_multi_index((x[j], y[j]), frame.shape, mode='raise',order='C')))
                # federatedcenters_ind.append(np.ravel_multi_index((x[j], y[j]), frame.shape, mode='raise', order='C'))
                federatedcentermap[x[j], y[j]] = 10000
                xs.append(x[j])
                ys.append(y[j])

    return federatedcentermap, xs, ys


# load image
filename = 'C:/Users/rldun/data/example_data/20180927_RLD/FC053A_w1_gfp_z10x40um_exp20ms_2/FC053A_w1_gfp_z10x40um_exp20ms_2_MMStack_Pos0.ome.tif'

tif = tf.TiffFile(filename)
frame = tif.pages[0].asarray()

# define test function
#@jit(nopython=True)
def testfunc(frame):
    #np.zeros([h, w])
    
    res, xs, ys = find_center(frame)
    quant = quantify_peak_centers_sk(frame, xs, ys)

    print('done...')

    return res


# time test function
t0 = time.time()
res = testfunc(frame)
t1 = time.time()

# do it again.. just to make sure...
t2 = time.time()
res = testfunc(frame)
t3 = time.time()

# one more time
t4 = time.time()
res = testfunc(frame)
t5 = time.time()



print('t1 - t0: {}', format(t1 - t0))
print('t3 - t2: {}', format(t3 - t2))
print('t5 - t4: {}', format(t5 - t4))


#pdb.set_trace()
#plt.imshow(res)
#plt.show()

