import numpy as np
import tifffile as tf
import time
import seaborn as sns



# initialize file objects
f1 = "Z:/RLD/Box Sync/Lab 2.0/data/20191030_RLD_1/20191031_RLD_analysis_1/20191030-12-04-00/20191030-12-04-00.tiff"
f2 = "C:/Users/rldun/Desktop/20191030-12-04-00.tiff"

# intialize tiff files
tiff1 = tf.TiffFile(f1)
tiff2 = tf.TiffFile(f2)

# individual frame timing
tiff1_time_list = []
tiff2_time_list = []

"""
# iterate some number of frames
frames_to_grab = 100
for i in range(frames_to_grab):

    # grab first
    t0 = time.time()
    f = tiff1.pages[i]
    t1 = time.time()
    tiff1_time_list.append(t1 - t0)

    # grab second
    t0 = time.time()
    f = tiff2.pages[i]
    t1 = time.time()
    tiff2_time_list.append(t1 - t0)


sns.distplot(tiff1_time_list)
sns.distplot(tiff2_time_list, rug=True)



# full file reads
tiff1_time_list = []
tiff2_time_list = []

for f in range(10):
    t0 = time.time()
    d = tf.imread(f1)
    t1 = time.time()
    tiff1_time_list.append(t1 - t0)

    t0 = time.time()
    d = tf.imread(f2)
    t1 = time.time()
    tiff2_time_list.append(t1 - t0)
"""

# grab 1 frame
tiff1_time_list = []
tiff2_time_list = []

# iterate some number of frames
frames_to_grab = [1, 10, 100,1000,10000]
for chunk in frames_to_grab:

    t0 = time.time()
    for f in range(chunk):
        res = tiff1.pages[f].asarray()
    t1 = time.time()
    tiff1_time_list.append(t1 - t0)

    t0 = time.time()
    for f in range(chunk):
        res = tiff2.pages[f].asarray()
    t1 = time.time()
    tiff2_time_list.append(t1 - t0)



#########################################################################################################

f1 = "Z:/SB/Good Rainbow Worms/20181011-col12-21/20181011-col12-21.tif"
f2 = "C:/Users/rldun/Desktop/20181011-col12-21.tif"



# intialize tiff files
tiff1 = tf.TiffFile(f1)
tiff2 = tf.TiffFile(f2)

# individual frame timing
tiff1_time_list = []
tiff2_time_list = []

# grab 1 frame
tiff1_time_list = []
tiff2_time_list = []

# iterate some number of frames
frames_to_grab = [1, 10, 100,1000,10000]
for chunk in frames_to_grab:

    t0 = time.time()
    for f in range(chunk):
        res = tiff1.pages[f].asarray()
    t1 = time.time()
    tiff1_time_list.append(t1 - t0)

    t0 = time.time()
    for f in range(chunk):
        res = tiff2.pages[f].asarray()
    t1 = time.time()
    tiff2_time_list.append(t1 - t0)
