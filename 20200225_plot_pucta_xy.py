# before running code:
# pip install matplotlib xlrd pandas seaborn numpy 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# decorating before plotting for saving as SVG 
#sns.set_style('whitegrid')
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['svg.fonttype'] = 'none'
plt.rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

# manually enter x/y
xs = [0.0058266,
-0.147607,
-0.205089,
-0.018677,
-0.1036024,
0.0078227,
-0.283345,
-0.193521,
-0.152002,
-0.205825,
-0.2435493,
-0.0545001,
-0.1915573,
0.0164003,
-0.2814322,
-0.258453,
-0.173571,
-0.3441172,
-0.1546507,
-0.1626672,
-0.2676011
]
ys = [

]

# load excel file
fname = 'C:/Users/rldun/Desktop/Chrx.xlsx'
df = pd.read_excel(fname, header=None)

# convert dataframe to numpy array
arr = df.values
xs = arr[:,0]
ys = arr[:,1]

# function to interpolate between two points
def interpolation_1d(p1, p2, interval):
    """
    linear interpolation between two points
    :param p1: first point
    :param p2: last point
    :param interval: how many points to squish between
    :return: returns interpolated vector of length inteval + 2 where v[0] and v[-1] and p1 and p2
    """

    ip = (p2 - p1) / (interval + 1)

    # iterate and append increments of p
    interp = []
    interp.append(p1)
    for i in range(0, interval):

        p = p1 + (ip * (i + 1))
        interp.append(p)

    # append last val
    interp.append(p2)
    return interp

# make interpolated xs/ys
new_xs = []
new_ys = []
num_squished = 100
for i in range(len(xs) - 1):
	new_xs = new_xs + interpolation_1d(xs[i], xs[i+1], 50)
	new_ys = new_ys + interpolation_1d(ys[i], ys[i+1], 50)

# get sequential colors
cs = plt.get_cmap('viridis', len(new_xs)).colors

# plot each point, colored
fig = plt.figure(figsize=(8,6))
for i in range(len(new_xs)):
	plt.scatter(new_xs[i], new_ys[i], color=cs[i], s=4)

# decorate
ax = fig.axes[0]
axis_bounds = 3 / 2
plt.clim(0,20)
cb = plt.colorbar()
cb.set_label('Minutes')
plt.xlim(-axis_bounds, axis_bounds)
plt.ylim(-axis_bounds, axis_bounds)
plt.xlabel('um from nucleus center')
plt.ylabel('um from nucleus center')
ax.tick_params(axis='x', direction='in')
ax.tick_params(axis='y', direction='in')
ax.set_aspect('equal')
