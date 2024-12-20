from SecurityCamera import CameraViewer
from EventPattern import EventSubscriber
import datetime

class EventGenerator:
    def __init__(self, camera):
        self.camera = camera
        
    def trigger_event(eventType, **kwargs):
        time = datetime.datetime.now()
        image_name = "event_{}_{}.png".format(eventType, time)
        