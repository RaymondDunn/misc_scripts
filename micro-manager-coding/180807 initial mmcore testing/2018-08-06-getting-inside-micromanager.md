---
layout: post
title: "Getting inside of micromanager"
---

# Introduction to my science
As part of my thesis project I want to do real-time analysis of worm whole-brain volumetric imaging data so that we can use the animal's active brain state to drive neural perturbations in a closed-loop fashion. This is a technical achievement which is absolutely necessary for systems neuroscience. 

This crucial observation has not gone unnoticed. Indeed the concept of "in-manifold" and "out-of-manifold" perturbations has been examined at length (see [Jazayeri and Afraz 2017 Neuron][Jazayeri and Afraz 2017 Neuron] for an excellent survey). Without considerations of a neural networks natural dynamics, it is exceedingly risky to interpret the effects of a perturbation.

[Jazayeri and Afraz 2017 Neuron]: https://www.ncbi.nlm.nih.gov/pubmed/28279349

So we want to start poking around and figure out how to do it! The first step naturally seems to be getting image frames out of a camera fast enough.


# Micro-manager core module

We currrently use micro-manager for our image acquisition in the imaging core facility. Fortunately, as far as open source projects go, MM has been developed surprisingly well. Without going into too much detail right now, it's core functionality is a number of functions written in C which can be accessed with bindings in Java, Matlab, and python. 

For more on the architecture of micro-manager, check out the [project overview page][Micro-manager project overview]

[Micro-manager project overview]: https://micro-manager.org/wiki/Micro-Manager_Project_Overview

Let's write a barebones program which grabs frames out of a dummy camera we have lying around lab and see how the python bindings work with respect to image acquisition overhead. We're going to compare this with the acquisition speed reported in the micromanager imageJ GUI for our same camera.

When we pull up micromanager and hit "live", data fps rate jiggles around, hitting 70, 75, and 80. It's not clear why it's jumping around, but if I had to eyeball it I'd say it's averaging right around 75. Lol.

Ok now let's write a quick program that loads the camera and runs through 1000 images (or if there's no image, prints "no frame"). See below.

{% highlight python%}
import MMCorePy
import time

mmc = MMCorePy.CMMCore()

config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)

mmc.enableStderrLog(False)
mmc.enableDebugLog(False)
mmc.setCircularBufferMemoryFootprint(1000)
mmc.setCameraDevice('AmScope')

mmc.startContinuousSequenceAcquisition(0)
t0 = time.time()
frames_to_grab = 1000
for t in range(0, frames_to_grab):
    if mmc.getRemainingImageCount() > 0:
        grey = mmc.getLastImage()
    else:
        print('No frame')
t1 = time.time()
print('total time is {}'.format(t1-t0))

cv2.destroyAllWindows()
mmc.stopSequenceAcquisition()
mmc.reset()
{% endhighlight %}

How long does this take to run? 21.8050000668 seconds, which comes out to 45.861 frames/second. If we run it right again we see 22.8360002041 and  23.5799999237 seconds. If we run it not in Ipython  (which we're doing above), and instead straight in python, we get 25.0759999752. We also run into lots of "No frame" prints... which I'm not quite sure the implications of that. Ok so streaming the images from the camera during a continuous acquisition has it's problems... And anyways I'm grabbing at frames, sometimes getting none, sometimes definitely missing some. Is there a way to stream everything into the circular buffer and keep it there?

Well first we want to do some circular buffer testing. Note that in order to see how many frames can fit in the circular buffer, we have to initialize it:

{% highlight python %}
import MMCorePy

mmc = MMCorePy.CMMCore()

config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)
mmc.setCameraDevice('AmScope')
mmc.initializeCircularBuffer()
mmc.getBufferTotalCapacity()
{% endhighlight %}

If we jack up the circular buffer with `mmc.setCircularBufferMemoryFootprint(1000)` we get `mmc.getBufferTotalCapacity()` = 19. If we jack it up more to `mmc.setCircularBufferMemoryFootprint(10000)` we get a `mmc.getBufferTotalCapacity()` of 194. Seeing as how our images from this camera, according to `mmc.getLastImage()` are 32 bit, 3286 x 4096 pixels, then 3286 x 4096 x 32 = 52.8 megabytes per image. So yeah it looks like our circular buffer sizes are right about right. Wow!

So why isn't our circular buffer just filling up like we would normally expect, maxing out and then staying at full size? Why when we repeatedly check the circular buffer size via `mmc.getRemainingImageCount()` do we see zeros, ones, twos, etc? Well the problem is that it's not a real circular buffer, according to some [blog posts I found][circular-buffer-blog-post]. Instead, the "buffer" gets emptied when it fills up, after which it begins re-filling...
We can help this with cropping the image... but let's not worry about that for now.

[circular-buffer-blog-post]: http://micro-manager.3463995.n2.nabble.com/Very-slow-acquisition-of-live-images-td7587918.html

What happens if we jack up the requested RAM, to say 100000 megabytes (which we def don't have...)? Well nothing interesting really, the program just hangs while the Task Manager memory reports 99% usage.

Using what we've learned we can now write a much tighter program that seems to work a lot better, right? Specifically we can do a `startSequenceAcquisition(args)` for a fixed number of frames, and loop until we've hit the right number of frames. This should tell use exactly how fast we can go. Code is:

{% highlight python%}
import MMCorePy
import time

# initialize
mmc = MMCorePy.CMMCore()
frames_to_grab = 500

# configure and prep for image acquisition
config_file = 'C:/Program Files/Micro-Manager-2.0beta/amscope_mu1403_config.cfg'
mmc.loadSystemConfiguration(config_file)
mmc.setCameraDevice('AmScope')
mmc.setCircularBufferMemoryFootprint(30000)

# start frame grabbing
print('Curr img count: {}'.format(mmc.getRemainingImageCount()))
t0 = time.time()
mmc.startSequenceAcquisition(frames_to_grab, 0, 0)

while True:
	if mmc.getRemainingImageCount() == frames_to_grab:
		break

t1 = time.time()
print('total time is: {}'.format(t1-t0))
{% endhighlight %}

How long does this take? 8.62700009346, 8.70100021362,  8.74500012398 seconds. What if we add a `prepareSequenceAcquisition('AmScope')` before the timer starts? We get 8.71399998665 and we crash python several times. All in all this gives us about 57 frames/s acquisition. That's better than before but not by that much.

Weird. according to this camera's catalog, we're actually above framerate: 54fps @ 1024x822, 21fps @ 2048x1644, 6.2fps @ 4096x3286. What's going on here? We're in the ballpark of 1024 x 822 fps, but we get images of 4096x3286. What's up with that?

# Other resources I'm stumbling upon

Other things that look relevant to me... I've read through, but putting here in case I need to re-find them sometime.

https://pypi.org/project/Micro-Manager/
https://github.com/zfphil/micro-manager-py36 (LOL from a graduate student in the Waller lab)
https://github.com/fcollman/MosaicPlannerLive

# Configuring micro-manager with python 3.0

Out-of-the-box bindings for micro-manager are for python=2.7. This is inconvenient, as a lot of the "speeding up" resources that I've stumbled upon online are for >python3.3. Ideally we can use the latest python.

Apparently according to https://valelab4.ucsf.edu/svn/micromanager2/trunk/doc/how-to-build.md we can build our own micro-manager set to a particular python version. However that's extra work... we could always try and use pre-built bindings that I found on github published by a graduate student in the waller lab: https://github.com/zfphil/micro-manager-py36

Note that I might have to have all this on the Desktop for weird file permissions reasons. I found this in the backwoods of some forum and I'm going with that for my testing environment. So unless I say so, let's assume we have to be outside of `C:/Program Files`

Great, I can download those github files, plop them into the micro-manager root directory replacing other python files, and all's good right? Well no -- I run into another snag, which suggests there's an incompatible version number between the python build and the micro-manager version. In other words I've got to go back and find the right base version of micro-manager to use with these github'd python bindings. Fortunately those versions can be well tracked via https://valelab4.ucsf.edu/trac/micromanager/log/MMDevice/MMDevice.h. So the device version update from 67 (our goal) to 68 happened on Nov. 7th, 2017. I should be able to grab a nightly build from Nov. 6th 2017 and that should work.

Aaaand it does! Cool so the nightly build was `MMSetup_64bit_2.0.0-beta3_20171106.exe`. If it turns out I need a newer micro-manager build I'll have to re-build myself to get python3.0+ bindings which we can either (A) do ourselves according to the document I cited above or (B) hit up that student from the Waller lab.

I re-installed in `C:\Program Files` for a sanity check, and things worked fine as far as I could tell. 

Some quick details about python environment:
`conda create -n micro-manager-p3 python=3.6`
`activate micro-manager-p3`
`pip install numpy`
`conda install -c conda forge opencv ffmpeg`
`conda install numba`

NOTE THAT I"M STILL FIGURING THIS OUT!

Micro-manager test code was:
{% highlight python%}
import sys

sys.path.append('C:\\Program Files\\Micro-Manager-2.0beta')

import MMCorePy

mmc = MMCorePy.CMMCoreo()

mmc.loadSystemConfiguration('C:\\Program Files\\Micro-Manager-2.0beta\\MMConfig_demo.cfg')
{% endhighlight %}

# What about controlling the ASI stage?

So we can grab images from the camera alright. We can set ROIs of the image (though we haven't tested it, I see how to do it in the documentation). The next big part of our imaging workflow is the volumetric part - direct communication with the ASI stage. Can we do that in our API? My suspicion is yes - after all, our current Beanshell script for controlling the stage (made with the help of Kurt Thorn, who [described this effort in his blog][kurt-thorn-blog-speeding-up-asi-stage]) makes use of the api just like we are. An equally important consideration is the synchronization between image acquisition and stage movement.

[kurt-thorn-blog-speeding-up-asi-stage]: http://nic.ucsf.edu/blog/2013/07/speeding-up-the-asi-stage/

Indeed it looks like we can control the Z-stage with the same function calls made in the beanshell script, provided we refactor for python bindings of course. But this raises a weird question that I don't fully understand - there's no explicit synchronization with camera image acquisition. Are we even camera-synched?

If it's any clue, according to `setSerialPortCommand()`, this command blocks until it receives an answer from the device. Kurt's script calls `getSerialPortAnswer(args)` but it looks like that might be unnecessary because `setSerialPortCommand()` implicitly receives an answer. Whatever let's keep it in because it works.

So perhaps that's the answer, and `startSequenceAcquisition()` implicitly synchronizes because of the block placed. Alternatively we might have to look into `assignImageSynchro()`

Hopefully we can do all of this without any additional settup past the initial loading of the system configuration. This is the big make or break. Well not break but it makes life real real annoying.


Looks like the next steps are to test a few things out!
1) Get image saving from the buffer working, and save with appropriate tags.

On the NIC scope (get permission from the techs first)
1) Setup python environment.
2) Test sequence acquisition.
3) Test stage movement.
4) Test volumentric sequence image saving.