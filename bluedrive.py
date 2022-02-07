"""note-python Raspberry Pi example.

This file contains a complete working sample for using the note-python
library on a Raspberry Pi device.
"""
import sys
import os
import time

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard   # noqa: E402

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


if sys.implementation.name != 'cpython':
    raise Exception("Please run this example in a \
                    Raspberry Pi or CPython environment.")

from periphery import I2C  # noqa: E402

def NotecardExceptionInfo(exception):
    """Construct a formatted Exception string.

    Args:
        exception (Exception): An exception object.

    Returns:
        string: a summary of the exception with line number and details.
    """
    s1 = '{}'.format(sys.exc_info()[-1].tb_lineno)
    s2 = exception.__class__.__name__
    return "line " + s1 + ": " + s2 + ": " + ' '.join(map(str, exception.args))


def transactionTest(card):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    req = {"req": "card.status"}

    try:
        rsp = card.Transaction(req)
        print(rsp)
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)


def get_action(card):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    req_hub_sync = {"req": "hub.sync"}
    req_file_changes = {"req": "file.changes"}
    req_note_get = {"req":"note.get","file":"data.qi"}
    req_note_get_delete = {"req":"note.get","file":"data.qi","delete":True}

    try:
        print('hub.sync')
        rsp = card.Transaction(req_hub_sync)
        print(rsp)
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)

    try:
        print('file.changes')
        rsp = card.Transaction(req_file_changes)
        print(rsp)
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)

    try:
        n_changes = rsp['total']
        print(n_changes)
    except KeyError:
        print('No changes')
        n_changes = 0

    action = None
    try:
        if n_changes > 0:
            print('note.get')
            rsp = card.Transaction(req_note_get_delete)
            print(rsp)

            action = rsp['body']['action']
            print(action)

    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)

    return action




def drive():
    """ This program has RVR drive with how to drive RVR using the drive control helper.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.drive_control.reset_heading()

        '''
        rvr.drive_control.drive_forward_seconds(
            speed=64,
            heading=0,  # Valid heading values are 0-359
            time_to_drive=1
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        rvr.drive_control.drive_backward_seconds(
            speed=64,
            heading=0,  # Valid heading values are 0-359
            time_to_drive=1
        )

        # Delay to allow RVR to drive
        time.sleep(2)
        '''

        print('spin')
        # Spin in place quickly
        rvr.drive_tank_normalized(
            left_velocity=-127,  # Valid velocity values are [-127..127]
            right_velocity=127  # Valid velocity values are [-127..127]
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        rvr.drive_tank_normalized(
            left_velocity=0,  # Valid velocity values are [-127..127]
            right_velocity=0  # Valid velocity values are [-127..127]
        )


        # Delay to allow RVR to drive
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()




def main():
    """Connect to Notcard and run a transaction test."""
    print("Opening port...")
    try:
        port = I2C("/dev/i2c-1")
    except Exception as exception:
        raise Exception("error opening port: "
                        + NotecardExceptionInfo(exception))

    print("Opening Notecard...")
    try:
        card = notecard.OpenI2C(port, 0, 0)
    except Exception as exception:
        raise Exception("error opening notecard: "
                        + NotecardExceptionInfo(exception))

    # If success, do a transaction loop
    print("Performing Transactions...")
    while True:
        print('Polling')
        action = get_action(card)
        if action == 'move':
            drive()
            break
        time.sleep(15)


main()
