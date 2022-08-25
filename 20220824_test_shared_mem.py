"""
# Start with an existing NumPy array
a = np.array([1, 1, 2, 3, 5, 8])
shm = shared_memory.SharedMemory(create=True, size=a.nbytes, name="agarblargblarg")

# Now create a NumPy array backed by shared memory
b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)

# Copy the original data into shared memory
b[:] = a[:]

# In either the same shell or a new Python shell on the same machine
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import shared_memory

# Attach to the existing shared memory block
existing_shm = shared_memory.SharedMemory(name="agarblargblarg")

# Note that a.shape is (6,) and a.dtype is np.int64 in this example
c = np.ndarray((6,), dtype=np.int64, buffer=existing_shm.buf)

# Back in the first Python interactive shell, b reflects this change

# Clean up from within the second Python shell
existing_shm.close()

# Clean up from within the first Python shell
shm.close()
shm.unlink()  # Free and release the shared memory block at the very end


##################################################
import numpy as np


img_dims = [240, 800]
num_images = 10
img_list = []
for f in range(num_images):
    img_list.append(np.random.randint(low=0, high=8000, size=img_dims, dtype=np.uint16))

# get first image for figuring out
frame_0 = img_list[0]

# create shared memory buffer
frame_buffer_shm = SharedMemory(
    name="frame_buffer", create=True, size=img_list[0].nbytes
)

# create array with buffer set to shared memory
frame_buffer = np.ndarray(
    img_dims, buffer=frame_buffer_shm.buf, dtype=img_list[0].dtype
)

# get image
# img = mmc.getImage().astype(np.uint16).reshape((ysize, xsize))

#############################################################

img_dims = [240, 800]
ysize = img_dims[0]
xsize = img_dims[1]
dtype=np.uint16

shared_frame_memory = shared_memory.SharedMemory(
                name="shared_frame_memory"
            )

shared_image_count = shared_memory.ShareableList(
                name="shared_image_count"
            )

img = np.ndarray(
                shape=(ysize, xsize), buffer=shared_frame_memory.buf, dtype=dtype
            )


"""

from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph.opengl as gl
from matplotlib import cm
import pyqtgraph as pg
import numpy as np
from multiprocessing import Process, Pipe
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import shared_memory
import time
import json


class QtVisualizer:
    def __init__(self, vis_args):
        self.vis_args = vis_args
        self.ipc = self.vis_args.get("ipc", "sockets")

        try:

            # create a pipe to visualizer
            if self.ipc == "sockets":
                self.parent_conn, self.child_conn = Pipe()
            elif self.ipc == "shared_memory":
                self.child_conn = None
                dtype = self.vis_args.get("dtype", np.uint16)
                ysize = vis_args.get("ysize", None)
                xsize = vis_args.get("xsize", None)
                empty_arr = np.zeros(shape=(ysize, xsize), dtype=dtype)
                self.shared_frame_memory = shared_memory.SharedMemory(
                    create=True, size=empty_arr.nbytes, name="shared_frame_memory"
                )
                self.shared_image_count = shared_memory.ShareableList(
                    [0], name="shared_image_count"
                )
                self.shared_ndarray = np.ndarray(
                    shape=(ysize, xsize),
                    buffer=self.shared_frame_memory.buf,
                    dtype=dtype,
                )

            # create process and start it
            self.proc = QtVisualizerWorker(self.child_conn, vis_args)
            self.proc.start()

        except Exception as err:
            print("Problem while initializing QtVisualizer: {}".format(err))
            raise (err)

    def update_display_images(self, payload):

        if self.ipc == "sockets":
            self.parent_conn.send(payload)
        elif self.ipc == "shared_memory":
            self.shared_ndarray[:] = payload[:]
            self.shared_image_count[0] += 1

    def close(self):
        if self.ipc == "shared_memory":
            self.shared_frame_memory.close()
            self.shared_frame_memory.unlink()  # Free and release the shared memory block at the very end
            self.shared_image_count.shm.close()
            self.shared_image_count.shm.unlink()
            # alternatively use a manager

        else:
            self.parent_conn.close()


class QtVisualizerWorker(Process):
    def __init__(self, child_conn, vis_args):

        # handheld timers
        self.initialization_t0 = time.time()
        self.timing_list_postrender = []
        self.timing_list_prerender = []

        super(QtVisualizerWorker, self).__init__()
        self.vis_args = vis_args
        self.first_img_flag = False
        self.image_count = 0
        self.total_frames = self.vis_args.get("total_frames", 100)
        self.ipc = self.vis_args.get("ipc", "sockets")
        self.dtype = self.vis_args.get("dtype", np.uint16)
        self.ysize = self.vis_args.get("ysize", None)
        self.xsize = self.vis_args.get("xsize", None)
        self.fps = self.vis_args.get("fps", None)

        if self.ipc == "sockets":
            self.child_conn = child_conn
        if self.ipc == "shared_memory":
            self.shared_frame_memory = shared_memory.SharedMemory(
                name="shared_frame_memory"
            )
            self.shared_image_count = shared_memory.ShareableList(
                name="shared_image_count"
            )

    def initialize_display(self):

        # make app
        self.app = QtWidgets.QApplication([])

        # make graphics widget
        self.graphics_layout = pg.GraphicsLayoutWidget()

        # create view box for image item with scrolling locked
        self.image_vbox = pg.ViewBox(lockAspect=True, enableMouse=False)
        self.image_vbox.invertY()

        # create image item, maintain reference to update later
        self.ii = pg.ImageItem()

        # make assemble objects into window
        self.image_vbox.addItem(self.ii)
        self.graphics_layout.addItem(self.image_vbox)
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.graphics_layout)
        self.window = QtWidgets.QWidget()
        self.window.resize(1400, 600)
        self.window.setLayout(self.grid)

        # initialize image holder, if shared mem has to be outside init
        if self.ipc == "shared_memory":
            self.img = np.ndarray(
                shape=(self.ysize, self.xsize),
                buffer=self.shared_frame_memory.buf,
                dtype=self.dtype,
            )

        # show
        self.window.show()

    def update_display_images(self, img):

        # update gui
        if self.ipc == "sockets":
            self.ii.setImage(img, autoLevels=True)
        elif self.ipc == "shared_memory":
            self.ii.setImage(img, autoLevels=True)

    def close(self):

        print("closing child connection")

        if self.ipc == "sockets":
            self.child_conn.close()
        elif self.ipc == "shared_memory":
            self.shared_frame_memory.close()
            self.shared_image_count.shm.close()

    def run(self):

        try:
            # initialize display, has to happen outside of init because
            self.initialize_display()
            self.app.processEvents()

            # pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=callback)
            try:

                while self.image_count <= self.total_frames - 1:

                    # process event loop unless there's data to work with
                    if self.ipc == "sockets":
                        while not self.child_conn.poll():
                            self.app.processEvents()
                        self.img = self.child_conn.recv()
                    elif self.ipc == "shared_memory":
                        while self.image_count == self.shared_image_count[0]:
                            self.app.processEvents()
                        # img = np.ndarray(shape=(ysize, xsize), buffer=self.shared_frame_memory.buf, dtype=dtype)

                    self.timing_list_prerender.append(time.time())
                    self.update_display_images(self.img)
                    self.timing_list_postrender.append(time.time())
                    self.image_count += 1

                    # continue event loop
                    self.app.processEvents()

            except Exception as err:
                print("Error in PointAndClick: {}".format(err))

        except Exception as err:
            print("Error: {}".format(err))

        print("Calculating inter-frame intervals...")

        time_arr_postrender = np.array(self.timing_list_postrender)
        time_arr_prerender = np.array(self.timing_list_prerender)
        # interval_arr = time_arr_prerender[1:] - time_arr_postrender[:-1]

        time_arr_render = time_arr_postrender - time_arr_prerender
        interval_arr = time_arr_postrender[1:] - time_arr_postrender[:-1]
        interval_arr = interval_arr - time_arr_render[:-1]

        expected_ifi = 1 / self.fps
        interval_arr = interval_arr - expected_ifi

        log_dict = {}
        log_dict["t0"] = self.initialization_t0
        log_dict["time_list_prerender[0] - t0:"] = (
            self.timing_list_prerender[0] - self.initialization_t0
        )
        log_dict["time_list_postrender[0] - t0:"] = (
            self.timing_list_postrender[0] - self.initialization_t0
        )
        log_dict["interval[0]"] = interval_arr[0]
        log_dict["interval[1]"] = interval_arr[1]
        log_dict["interval[2]"] = interval_arr[2]
        log_dict["interval mean"] = interval_arr.mean()
        log_dict["interval[1:] mean"] = interval_arr[1:].mean()
        log_dict["interval median"] = np.median(interval_arr)
        log_dict["interval stdev"] = np.std(interval_arr)
        log_dict["interval[1:] stdev"] = np.std(interval_arr[1:])
        log_dict["interval[:]"] = interval_arr.tolist()
        self.close()

        fname = "log.txt"
        with open(fname, "w") as f:
            json.dump(log_dict, f, indent=4)


# standalone testing
if __name__ == "__main__":

    import random

    random.seed(0)

    img_dims = [10000, 10000]
    ysize = img_dims[0]
    xsize = img_dims[1]
    num_images = 1
    img_list = []
    for f in range(num_images):
        img_list.append(
            np.random.randint(low=0, high=8000, size=img_dims, dtype=np.uint16)
        )

    # initialize visualizer with blank frame
    frame = img_list[0]
    fps = 10
    total_vols = 40
    vis_args = {
        "ysize": frame.shape[0],
        "xsize": frame.shape[1],
        "total_frames": total_vols,
        "ipc": "sockets",
        "dtype": np.uint16,
        "fps": fps,
    }

    vis = QtVisualizer(vis_args=vis_args)
    # vis.update_display_images(frame)
    time.sleep(10)

    # iterate and display images
    print("Starting...")
    img = np.random.randint(low=0, high=8000, size=img_dims, dtype=np.uint16)
    for i in range(0, total_vols):

        vis.update_display_images(img)

        if i % 10 == 0:
            print(i)

        # pause for fps sim
        if fps is not None:
            time.sleep(1 / fps)

    vis.close()
