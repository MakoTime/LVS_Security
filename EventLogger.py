import datetime
import enum
import json
import uuid

#----------------------------------------#
#   Event handler
#   Collects, reads and saves events to 
#   event_log.json
#----------------------------------------#

class EventData:
    def __init__(self, eventType, imagePath, eventID="", eventTime="", **kwargs) -> None:
        if eventTime != "":
            self.eventTime = eventTime
        else:
            self.eventTime = datetime.datetime.now()
        
        if eventID != "":
            self.eventID = eventID
        else:
            self.eventID = uuid.uuid4()
        
        self.eventType = eventType
        self.imagePath = imagePath
        self.eventID = eventID
        
        # Populate compulsary arguments in an event
        self.eventDict = {
            "eventType" : eventType,
            "imagePath" : imagePath,
            "eventID"   : eventID,
            "eventTime" : self.eventTime
        }
        
        # Populate optional arguments in an event
        for arg_name, arg_value in kwargs.items():
            self.eventDict.update({arg_name : arg_value})
        
class EventTypes(enum.Enum):
    INVALID = 0
    PERSON_DETECTED = 1
    PERSON_ID_ATTEMPT = 2
    PERSON_ID_SUCCESS = 3
    PERSON_ID_FAIL = 4
    PERSON_ENTER = 5
    PERSON_DETAINED = 6    
    
class EventLogger:
    def __init__(self):
        self._eventList = []
    
    def load_events(self):
        with open('sample.json', 'r') as openfile:
            eventData = json.load(openfile)
        for eventItem in eventData["events"]:
            event = EventData(**eventItem)
            self._eventList.append(event)
            
    def update_event_file(self):
        jsonDict = {"events" : self._eventList}
        jsonObject = json.dumps(jsonDict, indent=4)
        with open("sample.json", "w") as outfile:
            outfile.write(jsonObject)
            
    def purge_events(self):
        self._eventList = []
            
    def log_event(self, **kwargs):
        #assert event type and file location
        self.eventList.append(EventData(**kwargs))