import random
import logging
from enum import Enum, auto

class State(Enum):
    CALM = auto()
    MUSIC = auto()
    BRAWL = auto()
    CONVERSATION = auto()

class StateMachine:
    def __init__(self):
        self.current_state = State.CALM

    def set_state(self, new_state, ):
        self.current_state = new_state
        logging.info(f"State changed to {new_state.name}")

    def can_transition(self):
        return self.current_state == State.CALM

    def back_to_default(self):
        self.set_state(State.CALM)

    def random_transition(self):
        transition_prob = random.random()

        if self.current_state == State.CALM:
            if transition_prob < 0.5:
                self.set_state(State.MUSIC)
            elif transition_prob < 0.7:
                self.set_state(State.CONVERSATION)
            elif transition_prob < 1:
                self.set_state(State.BRAWL)
