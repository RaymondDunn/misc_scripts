# from https://stackoverflow.com/questions/44309437/python-store-video-as-hdf5-results-in-large-file-size
ABANDONED

import h5py
from skvideo.io import VideoCapture
frames = []
cap = VideoCapture('C:/Users/rldun/Videos/20180925_RLD/10fps about 3p2 aperture, upside down, autoexpos, uncompressed/tierpsy/002 light block on-09252018144815-0000.avi')
cap.open()

it = 0
while True:
    retval, image = cap.read()
    if image != None:
        frames.append(image)
        it += 1
        if (it % 500 == 0):
            print('Processed %d frames so far' % (it))
    if not retval:
        break

with h5py.File('C:/Users/rldun/Desktop/test.hdf5','w') as h5File:
    h5File.create_dataset('camera1',data=frames,compression='gzip',compression_opts=9)

# Initialize your dataset with the first image:
myDataSet = myFile.create_dataset('someName', data=image[None, ...], maxshape=(
                None, image.shape[0], image.shape[1], image.shape[2]), chunks=True)

# to add an image resize the whole dataset
myDataSet.resize(myDataSet.len() + 1, axis=0)
myDataSet[myDataSet.len() - 1] = image

# note that this forgots to add the compression. Without it the file size is the same as creating 
# separate datasets for each frame but takes 10+ times longer
