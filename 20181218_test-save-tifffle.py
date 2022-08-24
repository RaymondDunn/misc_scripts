from multiprocessing import Process
import tifffile as tf


class ImageSaver():

	def __init__(self, args):

		# create pipe to child process
		parent_conn, child_conn = Pipe()

		# initialize and start worker process
		proc = SaveWorker(args, child_conn)
		proc.start()


class SaveWorker(Process):

	def __init__(args, child_conn):

		# class super constructor
		super(SaveWorker, self).__init__()

		# save args
        self.clump_average = self.args.get('clump_average', 1)
        self.clump_size = self.args.get('clump_size')
        self.num_z = int(self.clump_size / self.clump_average)

		# save input stream
		self.child_conn = child_conn

		# save output stream
		savefilename = args.get('save_filename', 'temp.tif')
		self.tw = tf.TiffWriter(savefilename, imagej=True)
		self.images_saved = 0

	def run(self):

		try:
			while 1:

				# get images from stream
				clump, clump_start_time = self.child_conn.recv()

				# save each image in clump
				for z in self.num_z:
					self.tw.save(clump[:,:,z])
					self.images_saved += 1

				# TODO safety checks to make sure we don't try to write a single tiff
				# too big...
				# TODO alternatively we could try using MMCorePy to save images? 

		
		except EOFError as err:
			print('Saving multiprocess socket has been closed, closing output file.')
			self.tw.close()





# load images
filename = 'C:/Users/rldun/data/example_data/20180927_RLD/FC053A_w1_gfp_z10x40um_exp20ms_2/FC053A_w1_gfp_z10x40um_exp20ms_2_MMStack_Pos0.ome.tif'
save_filename = 'C:/Users/rldun/data/example_data/test_filesaving/temp.tif'

# import an image
tif = tf.TiffFile(filename)
frame = tif.pages[0].asarray()
frame2 = tif.pages[1].asarray()

# test saving with tiffwriter
tw = tf.TiffWriter(save_filename, imagej=True)
tw.save(frame)
tw.save(frame2)
tw.close()
