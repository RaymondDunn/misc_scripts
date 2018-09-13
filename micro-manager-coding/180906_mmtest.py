import sys
sys.path.append('C:\\Program Files\\Micro-Manager-2.0beta')
import MMCorePy
import pylab

 
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