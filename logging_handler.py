#!/usr/bin/env python
"""
File:             logging_handler.py
Date:             4/01/2025
Description:      Logging handler using logging
                  Adds the logging module to the event handler and adds
				  some extra formatting and commands
"""
import logging
import event_notifier as en

__author__ = "Benjamin Vernon-Bosley"
__copyright__ = "Livestock Visibility Solutions"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Benjamin Vernon-Bosley"
__email__ = "ben.vernon.bosley@gmail.com"
__status__ = "Prototype"

logger = logging.getLogger(__name__)
logging.basicConfig(filename='errors.log',
					encoding='utf-8',
					level=logging.DEBUG,
					format='%(asctime)s %(message)s',
					datefmt='%m/%d/%Y %I:%M:%S %p')

def handle_error(logging_level, error_location, description):
	"""Classifies the log type and runs the appropriate type, used as an
		event subscriber"""
	log_type = None
	match logging_level:
		case en.LoggingLevel.DEBUG:
			log_type = logger.debug
		case en.LoggingLevel.INFO:
			log_type = logger.info
		case en.LoggingLevel.WARNING:
			log_type = logger.warning
		case en.LoggingLevel.ERROR:
			log_type = logger.error
		case _:
			en.notify(en.SubscribedEventType.ERROR_EVENT,
						logging_level=en.LoggingLevel.ERROR,
			 			error_location=handle_error.__name__,
						description=f"Invalid Logging Level supplied {logging_level}")
			return
	log_msg = f"{description} at {error_location}"
	log_type(log_msg)

def purge_logs():
	"""Erases the contents of the log file, for use in unit tests"""
	with open('errors.log','w'):
		pass

def logging_init():
	"""Enables logging to add itself to the subscribers"""
	en.subscribe(en.SubscribedEventType.ERROR_EVENT, handle_error)
