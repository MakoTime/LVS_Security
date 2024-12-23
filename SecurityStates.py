from statemachine import StateMachine, State
from EventPattern import EventSubscriber
from EventLogger import EventTypes

class SecurityStateMachine(StateMachine):
    idle = State(initial=True)
    detected = State()
    scanning = State()
    hacking = State()
    allowed = State()
    detained = State()
    
    walk_up = idle.to(detected)
    open = detected.to(scanning)
    hack = detected.to(hacking)
    identify = (scanning.to(allowed, cond="id_accepted") |
                  scanning.to(scanning, unless="id_accepted"))
    detain = scanning.to(detained, cond="detain_individual") 
    catch = hacking.to(detained)
    ignore = hacking.to(allowed)
    move_on = (detained.to(idle) | allowed.to(idle))

    
    
    def __init__(self):
        self.maxTries = 3
        self.currentTries = 0
        self.detain_individual = False
        self.id_accepted = False
        self.userID = 0
        self.allowableIDs = [42, 100, 55]
        super(SecurityStateMachine, self).__init__()
    
    def before_identify(self):
        self.currentTries += 1
        self.detain_individual = (self.currentTries >= self.maxTries)
        
    def before_open(self, user_id):
        self.userID = user_id
        self.id_accepted = self.userID in self.allowableIDs
        
    def on_enter_idle(self):
        self.currentTries = 0
        self.detainIndividual = False
        self.id_accepted = False
        self.userID = None
        
    def on_transition(self, event_data, event):
        print(
            f"Moving from {event_data.transition.source.id} to "
            f"{event_data.transition.target.id}"
        )

if __name__ == "__main__":
    '''Generate the state machine png if run as is'''
    sm = SecurityStateMachine()
    # sm._graph().write_png("SecurityStateMachine.png")
    sm.walk_up()
    sm.open(42)
    sm.identify()
    sm.move_on()
    
    sm.walk_up()
    sm.open(69)
    sm.identify()
    sm.identify()
    sm.identify()
    sm.detain()
    
    