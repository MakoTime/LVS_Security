# LVS Security Application

## Overview
The system as a whole consists of the following modules:
 - security_manager.py
	- The starting point and application manager for the whole security system. It contains the cmd user interface `CommandUI` and manager `SecurityManager`. The CommandUI can show/hide the camera feeds, shut the system down, trigger events directly and run through the security state machine detailed below.
 - security_camera.py
	- The camera specific manager `CameraManager` that can handle multiple cameras and the camera objects themselves `Camera`
 - event_logger.py
	- Handles incoming event triggers and saves the event objects `Event` to the `EventHandler`. Additionally handles the reading and writing to the JSON file.
 - event_notifier.py
	- A subscriber/notifier design pattern used to send events across modules while allowing the objects to be decoupled from eachother.
 - security_states.py
	- A security specific state machine designed to simulate a generic security post, where specific actions generate the events. This is where the specified events are first 'notified' through the event notifier's subscribed functions and sent to the appropriate functions.
 - logging_handler.py
	- Another receiver of the event_notifier events, however these are for Error/Exception driven events. Based on the python loggin module, this allows for errors and warnings to be saved to errors.log and contain additional formatting
 - tests.py
	- Based on the python unittest module, tests for the state machine, event logging and camera captures are run. To run the tests, run `python tests.py`

## Running the system
To ensure the correct packages are installed run the following
```
pip install -r /path/to/requirements.txt
```
To begin the security application run the security manager. This assumes you have a webcam with the camera index at 0
```
python security_manager.py -c 0
```
__Navigating the state machine__
The current state machine has the following layout