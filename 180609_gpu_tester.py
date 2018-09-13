import numpy as np
from timeit import default_timer as timer
from numba import vectorize
from numba import cuda

@vectorize(['float32(float32, float32)'], target='cuda')
def pow(a, b):
    # for i in range(a.size):
    #    c[i] = a[i] ** b[i]
    return a ** b


def main():

    vec_size = 100000000

    a = b = np.array(np.random.sample(vec_size), dtype=np.float32)

    # c = np.zeros(vec_size, dtype=np.float32)

    start = timer()

    c = pow(a, b)

    duration = timer() - start

    print('Vector size {} took {} seconds.'.format(vec_size, duration))


cuda.select_device(1)
main()
