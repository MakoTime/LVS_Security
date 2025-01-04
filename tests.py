#!/usr/bin/env python
"""
File:           tests.py
Date:           4/01/2025
Description:    Runs unit tests on the state machine, event logger,
                and camera capture functionality.
                To use run: python tests.py
"""

import os
import unittest
import random
import time
from string import ascii_lowercase
from security_states import SecurityStateMachine
from event_logger import EventLogger
from security_camera import Camera
import event_notifier as en

__author__ = "Benjamin Vernon-Bosley"
__copyright__ = "Livestock Visibility Solutions"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Benjamin Vernon-Bosley"
__email__ = "ben.vernon.bosley@gmail.com"
__status__ = "Prototype"

class StateMachineTests(unittest.TestCase):
    """Tests for the functionality of the State machine and the event notifier around it"""
    def setUp(self):
        self.state_machine = SecurityStateMachine(allowable_ids=[42, 100, 55], print_actions=False)
        self.events = []
        en.subscribe(en.SubscribedEventType.SECURITY_EVENT, self.collect_event)

    def tearDown(self):
        en.unsubscribe(en.SubscribedEventType.SECURITY_EVENT, self.collect_event)
        EventLogger().purge_file()

    def collect_event(self, event_id):
        """Called from every security event, collects received event ids"""
        self.events.append(event_id)

    def test_detained_trigger_events(self):
        """Run through events that result in getting detained and test for events"""
        expected_events = [en.EventTypes.PERSON_DETECTED,
                        en.EventTypes.PERSON_ID_ATTEMPT,
                        en.EventTypes.PERSON_ID_FAIL,
                        en.EventTypes.PERSON_ID_ATTEMPT,
                        en.EventTypes.PERSON_ID_FAIL,
                        en.EventTypes.PERSON_ID_ATTEMPT,
                        en.EventTypes.PERSON_ID_FAIL,
                        en.EventTypes.PERSON_DETAINED]
        self.state_machine.walk_up()
        self.state_machine.open(random.choice(list(range(0,42))))
        self.state_machine.identify()
        self.state_machine.identify()
        self.state_machine.identify()
        self.state_machine.detain()
        self.state_machine.move_on()
        self.assertListEqual(self.events,
                             expected_events,
                             f"Expected {self.events} to match {expected_events}")

    def test_entry_trigger_events(self):
        """Run through all possible states and test for events"""
        expected_events = [en.EventTypes.PERSON_DETECTED,
                        en.EventTypes.PERSON_ID_ATTEMPT,
                        en.EventTypes.PERSON_ID_SUCCESS,
                        en.EventTypes.PERSON_ENTER]
        self.state_machine.walk_up()
        self.state_machine.open(random.choice([42, 100, 55]))
        self.state_machine.identify()
        self.state_machine.move_on()
        self.assertListEqual(self.events,
                             expected_events,
                             f"Expected {self.events} to match {expected_events}")

class EventLoggingTests(unittest.TestCase):
    """Tests for the event logger to correctly write, read and erase events from a file"""
    def setUp(self):
        self.logger = EventLogger()
        self.logger.purge_file()
        self.time = None
        self.file_location = None
        en.subscribe(en.SubscribedEventType.SECURITY_EVENT, self.trigger_event_log)

    def tearDown(self):
        en.unsubscribe(en.SubscribedEventType.SECURITY_EVENT, self.trigger_event_log)
        EventLogger().purge_file()

    def trigger_event_log(self, event_id):
        """Called from every security event, sends event code, file location and timestamp to event logger"""
        self.logger.log_event(event_type=str(event_id),
                              image_path=self.file_location,
                              event_time=self.time)

    def test_event_log(self):
        """Generates random variables to be written to the event logger and tests
            whether they are written"""
        event_count = random.randint(2,5)
        event_count = 2
        random_events = []

        for _ in range(event_count):
            event_dict = {"event_type" : str(random.choice(list(en.EventTypes))),
                        "image_path" : ''.join(random.choice(ascii_lowercase) for _ in range(10)),
                        "event_time" : time.time()}
            self.file_location = event_dict["image_path"]
            self.time = event_dict["event_time"]
            random_events.append(event_dict)
            en.notify(en.SubscribedEventType.SECURITY_EVENT, event_id=event_dict["event_type"])
            time.sleep(0.1)

        read_events = self.logger.retrieve_events()
        self.assertListEqual(random_events, read_events, "Events generated does not match events read")


class CameraTests(unittest.TestCase):
    """Tests the camera functionality of the security system"""
    def setUp(self):
        self.camera = None
        self.path = os.path.dirname(os.path.realpath('__file__')) + "\\test_captures"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.clear_captures()

    def tearDown(self):
        self.camera.quit()

    def clear_captures(self):
        """Deletes any previous test's images"""
        for file in os.listdir(self.path):
            if file.endswith(".png"):
                os.remove(self.path + "\\" + file)

    def test_camera_capture(self):
        """Takes an image and asserts that it is generated"""
        camera_id = 0
        self.camera = Camera(camera_id)
        self.camera.start()

        # Wait for camera to start up
        time.sleep(5)
        path = os.path.dirname(os.path.realpath('__file__')) + "\\test_captures"
        self.assertTrue(os.path.exists(path), "Folder does not exist")
        path_to_image = path + "\\camera-" + str(camera_id) + ".png"

        self.camera.capture(path)
        self.assertTrue(os.path.exists(path_to_image))

if __name__ == "__main__":
    unittest.main(verbosity=2)