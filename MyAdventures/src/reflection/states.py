from enum import Enum

"""
    STATES that an AGENT can be in
"""

class State(Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    WAITING = "WAITING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


def validate_transition(current_state: State, new_state: State):
    """Validate if an agent can transition from current_state to new_state."""
    valid_transitions = {
        State.IDLE: [],
        State.RUNNING: [],
        State.PAUSED: [],
        State.WAITING: [],
        State.STOPPED: [],
        State.ERROR: []
    }

    return new_state in valid_transitions.get(current_state, [])