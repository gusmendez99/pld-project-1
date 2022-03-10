# DFA & Graph
from graphviz import Digraph
from pythomata import SimpleDFA
from automata.base import Automaton
from tokenization.regex import EPSILON
# Common
from string import ascii_uppercase
from utils.common import save_file
from utils.visitor import VisitorNode

# Use class conventions for sets: [A-Z]
SET_NAME_STATES = ascii_uppercase
INITIAL_STATE_STR = SET_NAME_STATES[0]
GRAPHVIZ_OUTPUT_PATH = './renders/DFA.gv'


class DFA(Automaton):
    def __init__(self, symbols, regex):
        super(DFA, self).__init__(symbols, regex)
        # States will be generated while parsing NFA -> DFA
        self.states = dict()
        self.nodes = list()
        self.iterations = 0
        self.non_deterministic_final_states = dict()
        self.current_state = INITIAL_STATE_STR

    def from_NFA(self, nfa):
        # Note: transitions === tables, as we seen in past classes
        self.transitions_set_table = nfa.transitions
        self.non_deterministic_final_states = nfa.final_states
        self.generate_d_states()
        self.e_closure([], 0, INITIAL_STATE_STR)

    def move_to(
        self,
        target,
        symbol=EPSILON, 
        states_list=[],
        append_init_node=False, 
        single_move=False
    ):
        """ Move between nodes, use Visitor pattern """
        temp_states_list = states_list
        node = self.nodes[target]
        if not node.has_been_visited and symbol in node.next_states:
            node.has_been_visited = True
            next_states = [int(s) for s in node.next_states[symbol]]
            temp_states_list = [*next_states]
            if append_init_node:
                temp_states_list = [*next_states, target]

            # Move multiple times
            if not single_move:
                for new_node_id in node.next_states[symbol]:
                    future_states = self.move_to(int(new_node_id), symbol, temp_states_list)
                    temp_states_list += [*future_states]

        unique_states = set(temp_states_list)
        return list(unique_states)

    def uncheck_nodes(self):
        for node in self.nodes:
            # Uncheck visited node
            node.has_been_visited = False

    def e_closure(self, closure, node, current_state):
        if not closure:
            closure = self.move_to(0, append_init_node=True)
            closure.append(0)
            self.states[current_state] = closure
            if self.non_deterministic_final_states in closure:
                self.final_states.append(current_state)

        for symbol in self.symbols:
            symbol_closure = list()
            new_set = list()

            # Closure: state & symbol
            for value in closure:
                symbol_closure += self.move_to(
                    value,
                    symbol,
                    single_move=True
                )
                self.uncheck_nodes()

            # Closure: state & ɛ (epsilon) 
            if symbol_closure:
                e_closure = list()
                for e_value in symbol_closure:
                    e_closure += self.move_to(e_value)
                    self.uncheck_nodes()

                new_set += list(set([*symbol_closure, *e_closure]))

                # Case 1: State does not exists
                if not new_set in self.states.values():
                    self.iterations += 1
                    new_state = SET_NAME_STATES[self.iterations]

                    try:
                        curr_dict = self.transitions[current_state]
                        curr_dict[symbol] = new_state
                    except:
                        self.transitions[current_state] = {symbol: new_state}

                    try:
                        self.transitions[new_state]
                    except:
                        self.transitions[new_state] = {}

                    # Add set-entry to states
                    self.states[new_state] = new_set

                    # Add NFA final state if exists on set.
                    #   Then, test closure with the new set
                    if self.non_deterministic_final_states in new_set:
                        self.final_states.append(new_state)

                    self.e_closure(new_set, value, new_state)

                # Case 1: State exists, we need to add transition
                else:
                    for existing_state, existing_set in self.states.items():
                        if new_set == existing_set:
                            try:
                                curr_dict = self.transitions[current_state]
                            except:
                                self.transitions[current_state] = {}
                                curr_dict = self.transitions[current_state]

                            curr_dict[symbol] = existing_state
                            self.transitions[current_state] = curr_dict
                            break

    def generate_d_states(self):
        for state, values in self.transitions_set_table.items():
            new_visitor = VisitorNode(int(state), values)
            self.nodes.append(new_visitor)


    def simulate(self):
        current_state = INITIAL_STATE_STR
        for symbol in self.regex:
            if symbol not in self.symbols:
                self.regex_accept_status = False
            
            # Make transition between states
            try:
                current_state = self.transitions[current_state][symbol]
            except:
                # Validate acceptance state
                is_acceptance_state = current_state in self.final_states
                has_transition = symbol in self.transitions[INITIAL_STATE_STR]

                if is_acceptance_state and has_transition:
                    current_state = self.transitions[INITIAL_STATE_STR][symbol]
                else:
                    self.regex_accept_status = False
        
        # Final check for acceptance
        self.regex_accept_status = current_state in self.final_states

    def render_digraph(self):
        states = set(self.transitions.keys())
        final_states = set(self.final_states)
        symbols = set(self.symbols)

        dfa_digraph = SimpleDFA(
            states,
            symbols,
            INITIAL_STATE_STR,
            final_states,
            self.transitions
        )

        graph = dfa_digraph.trim().to_graphviz()
        graph.attr(rankdir='LR')

        save_file(GRAPHVIZ_OUTPUT_PATH, graph.source)
        graph.render(GRAPHVIZ_OUTPUT_PATH, format='pdf', view=True)
    