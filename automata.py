"""
 Automata models
"""

class Automaton:
    def __init__(self):
        self.initial = None
        self.states = set()
        self.final_states = set()
        self.alphabet = set()
        self.transitions = {}
    
    def add_state(self, state, is_initial = False, is_final = False):
        # Base case: state already exists
        if state in self.states:
            return False
        
        self.states.add(state)
        self.transitions[state] = {}
        if is_initial:
            self.initial = state
        elif is_final:
            self.final_states.add(state)

    def is_pool_state(self, state):
        is_pool = True
        for symbol in self.alphabet:
            dest = self.transitions[state].get(symbol, None)
            if (dest == None) or (dest != state):
                is_pool = False
        return is_pool
    

class NFA(Automaton):

    def epsilon_closure(self, state):
        """ TODO: Implement thompson epsilon closure """
        pass

    def move(self, states, symbol):
        """ thompson move function between states """
        target_state = set()
        for state in states:
            destinations = self.transitions[state].get(symbol, [])
            for destiny in destinations:
                target_state.add(destiny)
        return target_state
    
    def initial_thompson(symbol):
        nfa = NFA()
        nfa.add_state(0, True, False)
        nfa.add_state(1, False, True)
        nfa.add_transition(0, symbol, 1)
        return nfa

    def thompson_union(a, b):
        """ TODO: Implement thompson union """
        pass
    
    def thompson_concat(a, b):
        """ TODO: Implement thompson concat """
        pass

    def thompson_kleene_star(a):
        """ TODO: Implement thompson kleene star """
        pass

