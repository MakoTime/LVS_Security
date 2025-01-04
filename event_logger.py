#!/usr/bin/env python
"""
File:             event_logger.py
Date:             3/01/2025
Description:      Formats and reads/writes all security events to events.json
"""

import json

__author__ = "Benjamin Vernon-Bosley"
__copyright__ = "Livestock Visibility Solutions"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Benjamin Vernon-Bosley"
__email__ = "ben.vernon.bosley@gmail.com"
__status__ = "Prototype"

class EventData:
    """The object an event is created as, mostly represented as a single dictionary"""
    def __init__(self, event_type, image_path, event_time, **kwargs) -> None:

        # Have these variables accessable for down the line polling
        self.event_type = str(event_type)
        self.image_path = image_path
        self.event_time = event_time

        # Populate compulsary arguments in an event
        self.event_dict = {
            "event_type" : str(event_type),
            "image_path" : image_path,
            "event_time" : self.event_time
        }

        # Populate optional arguments in an event
        for arg_name, arg_value in kwargs.items():
            self.event_dict.update({arg_name : str(arg_value)})

class EventLogger:
    """The handler for reading and writing the events, either from loading or saving from
        file, or logging them from function calls"""
    def __init__(self):
        self._event_list = []
        self.load_events()

    def load_events(self):
        """Reads and appends all events from a json file, called primarily through startup
            so no _event_list reinitialisation is included in this function"""
        with open('events.json', 'r') as openfile:
            event_data = json.load(openfile)
        for event_item in event_data["events"]:
            event = EventData(**event_item)
            self._event_list.append(event)

    def update_event_file(self):
        """Writes all events into events"""
        event_dict = self.events_as_dictionaries()
        json_dict = {"events" : event_dict}
        json_object = json.dumps(json_dict, indent=4)
        with open("events.json", "w") as outfile:
            outfile.write(json_object)

    def purge_file(self):
        """Erases the json file contents"""
        # with open('events.json','w'):
        #     pass
        self.clear_events()
        self.update_event_file()

    def clear_events(self):
        """Clears the logger object list of events"""
        self._event_list = []

    def log_event(self, **kwargs):
        """Called every event trigger, appends the event to the list and updates the file"""
        self._event_list.append(EventData(**kwargs))
        self.update_event_file()

    def events_as_dictionaries(self):
        """Returns the list of events objects as a list of the object dictionaries"""
        return [event.event_dict for event in self._event_list]

    def retrieve_events(self):
        """Reloads the saved events in file and returns event list"""
        self.clear_events()
        self.load_events()
        return self.events_as_dictionaries()
