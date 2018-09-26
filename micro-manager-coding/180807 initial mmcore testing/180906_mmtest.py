import sys
path_to_mm = 'C:\\Program Files\\Micro-Manager-2.0beta'
sys.path.append(path_to_mm)
import MMCorePy
import pylab

# path hack
cd C:/Program Files/Micro-Manager-2.0beta

config_file = "C:/Users/rldun/code/misc_scripts/micro-manager-coding/amscope_mu1403_config.cfg"
# config_file = "C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg"

# initialize and set camera
mmc = MMCorePy.CMMCore()
mmc.loadSystemConfiguration(config_file)
mmc.setCameraDevice('AmScope')

# snap image and show
mmc.snapImage()
rgb32 = mmc.getImage()

# take view of same data... aparently fastest way of doing it
rgb = rgb32.view(dtype=pylab.uint8).reshape(rgb32.shape[0], rgb32.shape[1], 4)[...,2::-1]   

# show
#pylab.imshow(rgb)
#pylab.show()



"""
PUT A CHANNEL ON THE SCOPE SO WE HAVE SOMTHING TO FOCUS ON...

MMCorePy tests
* install appropriate micromanager, python environment, get MMCorePy working
*** take ROI'd images
*** acquisition sequence tests
*** Move stage during sequence acquisition

BEANSHELL TESTS
* Grab images straight from the beanshell
mm.getCore().continuousAcquisition
* save system state from beanshell
mm.getCore().saveSystemState(fileName)
*** IPC mechanisms via beanshell
import java.net.Socket;
https://stackoverflow.com/questions/31983000/serverpython-clientjava-communication-using-sockets
http://www.beanshell.org/examples/httpd.html

GUI tests
**change setting, save that system state, load into
MMCorePy, and see if change is maintained.
Also check camera settings (e.g. if there's cropping...)

"""

"""
Can do this at Sinistar:

** MMCorePy test saving images 

"""