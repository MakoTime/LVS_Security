from EventHandler import EventLogger
from statemachine import StateMachine, State

class SecurityObserver(StateMachine):
    idle = State(initial=True)
    detected = State()
    scanning = State()
    # hacking = State()
    allowed = State()
    detained = State()
    
    walk_up = idle.to(detected)
    open = detected.to(scanning)
    # hack = detected.to(hacking)
    identify = (scanning.to(allowed, cond="id_accepted") |
                  scanning.to(scanning, unless="id_accepted") |
                  scanning.to(detained, cond="detainIndividual"))
    # detain = scanning.to(detained, cond="detainIndividual") 
    # catch = hacking.to(detained)
    # ignore = hacking.to(allowed)
    move_on = (detained.to(idle) | allowed.to(idle))
    
    def __init__(self):
        self.maxTries = 3
        self.currentTries = 0
        self.detainIndividual = False
        self.userID = None
        self.allowableIDs = [42, 100, 55]
        
    def id_accepted(self):
        return self.userID in self.allowableIDs
    
    def before_identify(self, user_id):
        self.currentTries += 1
        self.detainIndividual = self.currentTries > self.maxTries
        self.userID = user_id
        
    def on_enter_idle(self):
        self.currentTries = 0
        self.detainIndividual = False
        self.userID = None

if __name__ == "__main__":
    logger = EventLogger()
    logger.load_events()
    print("loaded")
    for event in logger._eventList:
        print(event.eventType)
        
    SO = SecurityObserver()
    SO._graph().write("SecurityObserver")