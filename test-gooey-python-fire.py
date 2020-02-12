import numpy as np
import fire
from gooey import Gooey, GooeyParser
import time


@Gooey(dump_build_config=True, program_name="wb-live launcher", tabbed_groups=True)
def main():
    desc = "Example application for launching closed-loop experiment!"

    file_help_msg = "Name of the file you want to process"

    parser = GooeyParser(description=desc)

    # add argument elements that get added to the gui
    acq_group = parser.add_argument_group(
       "Acquisition", 
        "Settings for experimental acquisition."
    )
    acq_group.add_argument("DirectoryChooser", help=file_help_msg, widget="DirChooser")
    acq_group.add_argument("directory", help="Directory to store output")
    acq_group.add_argument('-d', '--duration', default=2,type=int, help='Duration (in seconds) of the program output')
    acq_group.add_argument('-s', '--cron-schedule', type=int, help='datetime when the cron should begin', widget='DateChooser')
    acq_group.add_argument("-c", "--showtime", action="store_true", help="display the countdown timer")
    acq_group.add_argument("-p", "--pause", action="store_true", help="Pause execution")
    acq_group.add_argument('-v', '--verbose', action='count')
    acq_group.add_argument("-o", "--overwrite", action="store_true", help="Overwrite output file (if present)")
    acq_group.add_argument('-r', '--recursive', choices=['yes', 'no'], help='Recurse into subfolders')
    acq_group.add_argument("-w", "--writelog", default="writelogs", help="Dump output to local file")


    search_group = parser.add_argument_group(
    "Search Options", 
    "Customize the search options"
    )
    search_group.add_argument("-e", "--error", action="store_true", help="Stop process on error (default: No)")


    # example of mutually exclusive arguments
    closed_loop_group = parser.add_argument_group(
       "Acquisition", 
        "Settings for experimental acquisition."
    )
    verbosity = closed_loop_group.add_mutually_exclusive_group()
    verbosity.add_argument('-t', '--verbozze', dest='verbose',action="store_true", help="Show more details")
    verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")

    # get "command line" arguments from GUI
    args = parser.parse_args()

    # display all arguments
    ops = vars(args)
    print('Incoming arguments: {}'.format(ops))
    time.sleep(2)
    print('Exiting...')
    

if __name__ == '__main__':
    main()
