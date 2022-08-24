# In the first Python interactive shell
import numpy as np

# Start with an existing NumPy array
a = np.array([1, 1, 2, 3, 5, 8])  
from multiprocessing import shared_memory
shm = shared_memory.SharedMemory(create=True, size=a.nbytes, name='agarblargblarg')

# Now create a NumPy array backed by shared memory
b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)

# Copy the original data into shared memory
b[:] = a[:]  

# In either the same shell or a new Python shell on the same machine
import numpy as np
from multiprocessing import shared_memory

# Attach to the existing shared memory block
existing_shm = shared_memory.SharedMemory(name='agarblargblarg')

# Note that a.shape is (6,) and a.dtype is np.int64 in this example
c = np.ndarray((6,), dtype=np.int64, buffer=existing_shm.buf)

c[-1] = 888

array([  1,   1,   2,   3,   5, 888])

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
frame_buffer_shm = SharedMemory(name="frame_buffer", create=True, size=img_list[0].nbytes)

# create array with buffer set to shared memory
frame_buffer = np.ndarray(img_dims, buffer=frame_buffer_shm.buf, dtype=img_list[0].dtype)

# get image
img = mmc.getImage().astype(np.uint16).reshape((ysize, xsize))
