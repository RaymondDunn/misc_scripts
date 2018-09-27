import socket
import json
import sys

path_to_mm = 'C:\\Program Files\\Micro-Manager-2.0beta'
sys.path.append(path_to_mm)
import MMCorePy

def save_image_sequence(mmc):

    #

def acquire_image_sequence(mmc, um_frames):

    # start acquisition
    mmc.startSequenceAcquisition(frames_to_grab, 0, 0)

    # wait until acq, show progress along the way...
    while True:

        # print on progress
        if m

        # 
        if mmc.getRemainingImageCount() == frames_to_grab:
            break




########################################

def load_acquisition_params(mmc):

    print("params: {}".format(params))

    # load system state
    mmc.loadSystemState(params["systemState"])

   # other initialization settings (not sure if necessary)
    mmc.setCircularBufferMemoryFootprint(30000)
    mmc.setCameraDevice('AmScope')
    mmc.initializeCircularBuffer()

    # set roi
    roi = params["roi"]
    mmc.setROI(roi[0], roi[1], roi[2], roi[3])


def control_stage(mmc):

    def sendASICommand(command):
        # sent command to serial port and wait for answer
        # note "wait for answer" might not be necessary (see docs)
        mmc.getSerialPortCommand("COM3", command, "\r")
        asi_return = mmc.getSerialPortAnswer()

        # reformat multi line responses for display
        asi_return = asi_return.replace('\r', "\r\n")
        return asi_return

    # params from ASIUniZScan.bsh
    print("Starting stage control...")
    z_position_baseline = -250.
    z_step_size = 35
    num_z_levels = 10
    total_z_positions = 1*num_z_levels

    # create z position array
    z_position_array = []
    for i in range(0, num_z_levels):

        # append position to array
        z_position_array.append(z_position_baseline + (i * z_step_size)) 

    # Clear the ring buffer, set to move Z only
    ans = sendASICommand("RM X=0 Y=4 Z=0");
    print("TODO: check if ring buffer cleared...")
    #if (!ans.regionMatches(1,"A",0,1)){
    #    error("Couldn't clear ring buffer");
    #}
    
    # load positions into asi controller ring buffer
    z_num = 0
    while z_num < total_z_positions:

        # String command = String.format("LD Z=%1$-4.1f", new Object[] {zPositionArray[zNum]});
        command = "LD Z={0:4.1f}".format(z_position_array[z_num])
        print("Command is: {}".format(command))

        # get answer
        ans = sendASICommand(command)
        print("Response is: {}".format(ans))

        # increment z counter
        z_num += 1

    # set trigger mode to move to next ring buffer Z position upon TTL pulse
    ans = sendASICommand("TTL X=1")
    print("TODO: check if couldn't set TTL trigger mode")
    #if (!ans.regionMatches(1,"A",0,1)){
    #    error("Couldn't set TTL trigger mode.");
    #}
    # note that camera stage sync may be done via direct connection 
    # see https://micro-manager.org/wiki/ASIStage

def run_acquisition(params_string):

    # create mmc object
    mmc = MMCorePy.CMMCore()

    # load json and set params
    params = json.loads(params_string)
    load_acquisition_params(params)

    # start stage moving
    control_stage(mmc)

    # start acq
    num_frames = params["numFrames"]
    acquire_image_sequence(mmc, num_frames)



def listen():

    # vars
    port = 9999
    buffer_size = 4096

    #create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host,
    server_socket.bind(("localhost", port))

    # listen for up to x connections
    print("Listening for a connection...")
    server_socket.listen(15)

    while True:

        # accept connections from outside
        (client_socket, client_address) = server_socket.accept()

        # in this case, we'll pretend this is a threaded server
        # ct = client_thread(clientsocket)
        # ct.run()

        try:
            print("connection from", client_address)

            data = client_socket.recv(buffer_size)
            print("Received {}".format(data))

            if data:

                print("Reading data...")
                run_acquisition(data)
                client_socket.sendall(data)

        finally:

            # closing connection
            print("closing connection...")
            
            # close connection with client
            client_socket.close()
            
            # close connection with server
            server_socket.close()
            break

# run...
listen()