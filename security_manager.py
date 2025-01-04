#!/usr/bin/env python
"""
File:             security_manager.py
Date:             3/01/2025
Description:      Central manager of the security system and command line interface.
                  The CommandUI utilises the cmd module and threading to allow for
                  concurrent processes
"""

import os
import cmd
import threading
import datetime
import argparse
import logging_handler
import event_notifier as en
from event_logger import EventLogger
from security_camera import CameraManager
from security_states import SecurityStateMachine

__author__ = "Benjamin Vernon-Bosley"
__copyright__ = "Livestock Visibility Solutions"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Benjamin Vernon-Bosley"
__email__ = "ben.vernon.bosley@gmail.com"
__status__ = "Prototype"


class CommandUI(cmd.Cmd, threading.Thread):
    """The command line interface to use with LVS Security"""
    intro = 'Welcome to the LVS Security system. Type help or ? to list commands.\n'
    prompt = "> "
    file = None

    def __init__(self, manager_interface) -> None:
        super().__init__(completekey="tab")
        threading.Thread.__init__(self)
        self.manager:SecurityManager = manager_interface

    def run(self):
        """Holds the main command loop to use with threading"""
        self.cmdloop()

    def do_sim(self, action):
        """cmd callable function to interface with state machine actions, for specific actions
            see the state machine in use"""
        try:
            self.manager.security_action(action)
        except Exception as e:
            print(f"{e} is not a possible action")

    def do_quit(self, args):
        """Calls the manager to quit"""
        self.manager.quit()
        return True

    def do_show_feed(self, camera):
        """Displays the camera feed specified, if none specified then show all"""
        if not camera:
            self.manager.show_all()
        else:
            self.manager.camera_manager.display_camera(camera)

    def do_hide_feed(self, camera):
        """Displays the camera feed specified, if none specified then show all"""
        if not camera:
            self.manager.hide_all()
        else:
            self.manager.camera_manager.hide_camera(camera)

    def do_trigger_event(self, args):
        print(f"Triggering event {args}")
        self.manager.trigger_event(args)


class SecurityManager():
    """Main security interface"""
    def __init__(self, camera_feed=None):
        logging_handler.logging_init()
        self.camera_manager = CameraManager(camera_feed)

        self.logger = EventLogger()
        self.simulator = SecurityStateMachine(allowable_ids=[42, 100, 55])
        self.ui = CommandUI(self)

        self.threads = []
        self.setup_camera_threads()
        self.threads.append(self.ui)
        for thread in self.threads:
            thread.start()

        en.subscribe(en.SubscribedEventType.SECURITY_EVENT, self.trigger_event)

    def setup_camera_threads(self):
        """Adds the camera display loops to the central threading task"""
        for camera_name, camera in self.camera_manager.cameras.items():
            print(f"Adding {camera_name}")
            self.threads.append(camera)

    def security_action(self, action, arguments=None):
        """Searches for available actions in the statemachine and calls it"""
        print(f"Action: {action}")
        function = getattr(self.simulator, action)
        result = function(arguments)
        if type(result) == en.EventTypes:
            self.trigger_event(result)

    def trigger_event(self, event_id):
        time = datetime.datetime.now()
        formatted_time = f"{time.year}-{time.month}-{time.day}_{time.hour}{time.minute}{time.second}"
        folder_name = f"event_{event_id}_{formatted_time}"

        path = os.path.dirname(os.path.realpath('__file__')) + "\\event_captures"
        assert os.path.exists(path)
        folder_path = path + "\\" + folder_name
        os.makedirs(name=folder_path)
        self.camera_manager.capture(folder_path)

        self.logger.log_event(event_type=event_id, image_path=folder_path, event_time=str(time))

    def show_all(self):
        """Enable all camera threads to show in a new window"""
        self.camera_manager.show_all_cameras()

    def hide_all(self):
        """Disable updating the displayed camera"""
        self.camera_manager.hide_all_cameras()

    def quit(self):
        """Calls for all processes to quit"""
        self.camera_manager.quit_all()


if __name__ == "__main__":
    # For multiple cameras add -c before each camera input
    # eg: python security_manager.py -c 0 -c 1 -c 2
    parser = argparse.ArgumentParser(prog="LVS Security Application",
                                     description="A basic security system simulation")
    parser.add_argument("-c", "--camera", action='append', required=False)
    args = parser.parse_args()
    # Integers parsed in will be counted as strings, this changes it back
    int_checked_cameras = [int(camera) for camera in args.camera if camera.isdigit()]
    manager = SecurityManager(int_checked_cameras)
