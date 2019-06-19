

# download and install spinnaker sdk

# download pyspin from box and install
# when in the downloaded directory (https://flir.app.boxcn.net/v/SpinnakerSDK/folder/73503062578)
# i installed \spinnaker_python-1.23.0.27-cp37-cp37m-win_amd64

conda create -n pyspin
conda activate pyspin
conda install python ipython 
pip install spinnaker_python-1.23.0.27-cp37-cp37m-win_amd64.whl
pip install matplotlib # conda install matplotlib doesn't work!
pip install opencv-python 