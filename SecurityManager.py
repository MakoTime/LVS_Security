from EventLogger import EventLogger, EventTypes
from SecurityCamera import CameraViewer
from SecurityStates import SecurityStateMachine
import cmd, sys

class SecurityManager():
    try:
        camera = CameraViewer(0)
    except:
        print("Unable To Open Camera")
        camera = None
        
    logger = EventLogger()
    simulator = SecurityStateMachine()
        
    @classmethod
    def security_action(cls, action, arguments):
        function = getattr(cls.simulator, action)
        function(arguments)
        
    
class SecurityUI(cmd.Cmd):
    intro = 'Welcome to the LVS Security system. Type help or ? to list commands.\n'
    prompt = "> "
    file = None
    
    def __init__(self) -> None:
        super().__init__(completekey = "tab")
    
    def do_actions(self, args):
        print("Tried")
        # for action in args:
        #     try:
        #         SecurityManager.security_action(action)
        #     except Exception as e:
        #         print(f"{e} is not a possible action")
            
    def do_quit(self, args):
        return True
        

if __name__ == "__main__":
    securityUi = SecurityUI()
    securityUi.cmdloop()