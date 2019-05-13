import tifffile as tf
import codecs
import json



fname = 'C:/Users/rldun/data/example_data/20141231_SSK/TS20140715e_lite-1_punc-31_NLS3_2eggs_56um_1mMTet_basal_1080s/TS20140715e_lite-1_punc-31_NLS3_2eggs_56um_1mMTet_basal_1080s_01.ome.tiff'
tiff = tf.TiffFile(fname)
frame = tiff.pages[0].asarray()

# convert to json string
imgjson = json.dumps(frame.tolist()) 

# print, which is directed to electron process
#print('Hello from Python!')
print(imgjson)
sys.stdout.flush()
