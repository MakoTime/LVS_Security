from EventLogger import EventLogger, EventTypes
from SecurityCamera import CameraManager
from SecurityStates import SecurityStateMachine
import cmd, sys
import threading   
    
class CommandUI(cmd.Cmd):
    intro = 'Welcome to the LVS Security system. Type help or ? to list commands.\n'
    prompt = "> "
    file = None
    
    def __init__(self, manager) -> None:
        super().__init__(completekey = "tab")
        self.manager:SecurityManager = manager

    def run(self):
        self.cmdloop()

    def get_all_actions(self):
        print(f"Events: {self.manager.get_events()}")
        print(f"State: {self.manager.get_state()}")
        print(f"Transitions: {self.manager.get_transitions()}")
    
    def do_actions(self, args):
        self.get_all_actions()

    def do_sim(self, action):
        try:
            self.manager.security_action(action)
        except Exception as e:
            print(f"{e} is not a possible action")
            
    def do_quit(self, args):
        self.manager.quit()
    
class SecurityManager():
    def __init__(self, cameraFeed=None):
        self.camera_manager = CameraManager(cameraFeed)
            
        self.logger = EventLogger()
        self.simulator = SecurityStateMachine()
        self.ui = CommandUI(self)

        self.threads = []
        self.setup_camera_threads()
        self.threads.append(threading.Thread(target=self.ui.run))

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    def setup_camera_threads(self):
        for camera_name, camera in self.camera_manager.cameras.items():
            print(f"Adding {camera_name}")
            self.threads.append(threading.Thread(target=camera.display_feed))

    def get_state(self):
        return self.simulator.current_state.name
    
    def get_transitions(self):
        return self.simulator.current_state.transitions
    
    def get_events(self):
        return self.simulator.events

    def security_action(self, action, arguments=None):
        print(f"Action: {action}")
        function = getattr(self.simulator, action)
        function(arguments)

    def quit(self):
        self.camera_manager.quit_all()

if __name__ == "__main__":
    manager = SecurityManager()
