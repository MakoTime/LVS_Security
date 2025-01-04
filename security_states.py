#!/usr/bin/env python
"""
File:           security_states.py
Date:           3/01/2025
Description:    Security state machine designed to trigger specific events.
                To view state machine diagram run the script as is and open
                the SecurityStateMachine.png image.
"""

from statemachine import StateMachine, State
import event_notifier as en

__author__ = "Benjamin Vernon-Bosley"
__copyright__ = "Livestock Visibility Solutions"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Benjamin Vernon-Bosley"
__email__ = "ben.vernon.bosley@gmail.com"
__status__ = "Prototype"

class SecurityStateMachine(StateMachine):
    """An example state machine that simulates a basic security system using the
        StateMachine module"""
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

    def __init__(self, allowable_ids=[42, 50], print_actions=True):
        """Initialises the prameters for the state machine"""
        self.max_tries = 3
        self.current_tries = 0
        self.detain_individual = False
        self.id_accepted = False
        self.allowable_ids = allowable_ids
        self.user_id = None
        self.print_actions = print_actions
        super(SecurityStateMachine, self).__init__()


    def before_identify(self):
        """At the start of the identify action, determines if tried too many times"""
        self.current_tries += 1
        self.detain_individual = (self.current_tries >= self.max_tries)
        en.notify(en.SubscribedEventType.SECURITY_EVENT,
                  event_id=en.EventTypes.PERSON_ID_ATTEMPT)
        if self.id_accepted:
            en.notify(en.SubscribedEventType.SECURITY_EVENT,
                  event_id=en.EventTypes.PERSON_ID_SUCCESS)
        else:
            en.notify(en.SubscribedEventType.SECURITY_EVENT,
                    event_id=en.EventTypes.PERSON_ID_FAIL)

    def before_open(self, user_id):
        """At the start of the open action, reads and compares the given id"""
        self.user_id = user_id
        self.id_accepted = self.user_id in self.allowable_ids
        en.notify(en.SubscribedEventType.SECURITY_EVENT,
                  event_id=en.EventTypes.PERSON_DETECTED)

    def on_enter_allowed(self):
        """On entry to the allowed state, notify"""
        en.notify(en.SubscribedEventType.SECURITY_EVENT,
                  event_id=en.EventTypes.PERSON_ENTER)

    def on_enter_detained(self):
        """On entry to the detained state, notify"""
        en.notify(en.SubscribedEventType.SECURITY_EVENT,
                  event_id=en.EventTypes.PERSON_DETAINED)

    def on_enter_idle(self):
        """On entry to the idle state, reset the person variables"""
        self.current_tries = 0
        self.detain_individual = False
        self.id_accepted = False
        self.user_id = None

    def on_transition(self, event_data):
        """Unless specified, all actions will be detailed in stdout"""
        if self.print_actions:
            print(
                f"Moving from {event_data.transition.source.id} to "
                f"{event_data.transition.target.id}"
            )

if __name__ == "__main__":
    # Generate the state machine png if run "python security_states.py"
    # Requires pydot to generate
    sm = SecurityStateMachine(allowable_ids=[42, 100, 55])
    sm._graph().write_png("SecurityStateMachine.png")

