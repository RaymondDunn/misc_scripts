import random
from sklearn import metrics
import numpy as np
import os

#############################
bins = 2 ## MI bin number
SEED = 1 ## seed for random

#############################


# calculate MI matrix
def calc_MI_matrix(xs, bins):
    
    score_matrix = np.zeros((len(xs), len(xs)))
    for i in range(len(xs)):
        for j in range(len(xs)):
            curr_score = calc_MI(xs[i], xs[j], bins)
            score_matrix[i, j] = curr_score

    return score_matrix

def calc_MI(x, y, bins):
    
    # calcuate the mutual info of a single segment to the 
    # John Webb 2018
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = metrics.mutual_info_score(None, None, contingency=c_xy)
    return mi


def getDataLists(p1_file='p1.txt', p2_file='p2.txt'):

    # local file names
    p1_file = "p1.txt"
    p2_file = "p2.txt"
    cwd = os.getcwd()

    # local path
    p1_path = os.path.join(cwd, p1_file)
    p2_path = os.path.join(cwd, p2_file)

    # open files
    f1 = open(p1_path, 'r')
    f2 = open(p2_path, 'r')

    # save in list
    filelist = [f1, f2]
    datalist = []

    # iterate files
    for f in filelist:

        # holder for file data
        flist = []
        fcontent = f.readlines()
        
        for line in fcontent:

            # append formatted list
            flist.append(float(line.replace('\n', "")))

        # push file data as array
        datalist.append(np.array(flist))

    # return
    return datalist

# seed rng
random.seed(SEED)

# get data from text files
datalist = getDataLists()

# local vars
xs = []
for x in datalist:
    xs.append(x)

# get mutual information of dataset
mi_mat = calc_MI_matrix(xs, bins)

calc_MI_pvalue(xs, bins)
# shuffle samples and calculate mutual information
iterations = 10000
xs_shuffled = []
shuffled_mi_mats = np.zeros((len(xs), len(xs), iterations))
for i in range(iterations):
    
    # shuffle each vector
    for x in datalist:
        xs_shuffled.append(random.shuffle(x[i]))

    # calculate mi mat of shuffled
    mi_mat_shuffled = calc_MI_matrix(xs_shuffled, bins)
    shuffled_mi_mats[:,:,i] = mi_mat_shuffled

# calculate two-sided p value as proportion of values big enough away from sample
p_mat = np.sum(np.abs(mi_mat) > np.abs(shuffled_mi_mats), axis=2) / iterations