"""
 Automata models
"""

class Automaton:
    def __init__(self, symbols, regex):
        self.initial = None
        self.states = []
        self.final_states = []
        self.transitions = dict()
        self.current_state = None
        self.prev_state = None
        # Regex params
        self.symbols = symbols
        self.regex = regex
        self.regex_accept_status = False
    
    def add_state(self, state, is_initial = False, is_final = False):
        # Base case: state already exists
        if state in self.states:
            return False
        
        self.states.append(state)
        self.transitions[state] = dict()
        if is_initial:
            self.initial = state
        elif is_final:
            self.final_states.append(state)
    
