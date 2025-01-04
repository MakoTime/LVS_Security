#!/usr/bin/env python
"""
File:           event_notifier.py
Date:           3/01/2025
Description:    Adds a subscriber observer pattern to the security system.
                Currently used for general events and Error logging
"""

import enum

__author__ = "Benjamin Vernon-Bosley"
__copyright__ = "Livestock Visibility Solutions"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Benjamin Vernon-Bosley"
__email__ = "ben.vernon.bosley@gmail.com"
__status__ = "Prototype"

class SubscribedEventType(enum.Enum):
    SECURITY_EVENT = 0
    ERROR_EVENT = 1

class LoggingLevel(enum.Enum):
	DEBUG = 0
	INFO = 1
	WARNING = 2
	ERROR = 3

class EventTypes(enum.Enum):
    INVALID = 0
    PERSON_DETECTED = 1
    PERSON_ID_ATTEMPT = 2
    PERSON_ID_SUCCESS = 3
    PERSON_ID_FAIL = 4
    PERSON_ENTER = 5
    PERSON_DETAINED = 6

subscribers = {}

def subscribe(event_type, function):
    """Add a function to be called once an event type of SubscribedEventType is triggered"""
    if not event_type in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(function)

def unsubscribe(event_type, function):
    """Removes a function linked to a SubscribedEventType event"""
    if not event_type in subscribers:
        print("Cannot remove events that dont exist")
        return
    subscribers[event_type].remove(function)

def notify(event_type, **kwargs):
    """Calls all SubscribedEventType subscribed functions with the arguments provided"""
    if not event_type in subscribers:
        print("Trying to call event with no subscibers")
        return
    for function in subscribers[event_type]:
        function(**kwargs)
