# import libraries

import sys
import os
import time

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

rvr.wake()

time.sleep(2)

rvr.drive_control.reset_heading()

