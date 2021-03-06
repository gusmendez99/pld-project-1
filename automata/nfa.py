from automata.base import Automaton
from graphviz import Digraph
from utils.common import save_file
from tokenization.regex import EPSILON
from tree.node import *

GRAPHVIZ_EDGE = '->'
GRAPHVIZ_EQUAL = '='
GRAPHVIZ_TAB = '\t'
GRAPHVIZ_OUTPUT_PATH = './renders/NFA.gv'

# Init state
INITIAL_STATE = 1
INITIAL_STATE_STR = '0'

class NFA(Automaton):
    def __init__(self, parsed_tree, symbols, regex):
        super(NFA, self).__init__(symbols, regex)
        self.parsed_tree = parsed_tree
        self.current_state = INITIAL_STATE
        # Graph repr
        self.digraph = Digraph(strict=True)
        self.digraph.attr(rankdir='LR')
        self.digraph.attr('node', shape='circle')

        # Parsing tree to NFA
        self.render_node(parsed_tree)
        self.generate_transitions()
        self.generate_acceptance_state()

    def simulate(self):
        try:
            init_symbol = self.regex[0]
            self.simulate_regex_symbol(
                init_symbol,
                INITIAL_STATE_STR,
                self.regex
            )
            print('NFA simulation done!')
        except RecursionError:
            final_existing_symbol = self.regex[0]
            # Set bool acceptance status
            self.regex_accept_status = final_existing_symbol in self.symbols and final_existing_symbol != EPSILON
            print('NFA simulation done!')

    
    def simulate_regex_symbol(self, regex_symbol, state, regex):
        if self.regex_accept_status:
            return

        transitions = self.transitions[state]
        for symbol in transitions:
            if symbol == EPSILON:
                if not regex and str(self.final_states) in transitions[EPSILON]:
                    self.regex_accept_status = True
                    return

                for epsilon_status in transitions[EPSILON]:
                    if self.regex_accept_status:
                        break
                    self.simulate_regex_symbol(regex_symbol, epsilon_status, regex)
            
            elif symbol == regex_symbol:
                next_regex = regex[1:]
                try:
                    next_symbol = next_regex[0]
                except:
                    next_symbol = None

                if not next_symbol:
                    if str(self.final_states) in transitions[symbol]:
                        self.regex_accept_status = True
                        return

                    elif str(self.final_states) != state:
                        for symbol_state in transitions[symbol]:
                            self.simulate_regex_symbol(EPSILON, symbol_state, None)
                        if self.regex_accept_status:
                            return

                if self.regex_accept_status:
                    return

                for symbol_state in transitions[symbol]:
                    if not next_symbol and str(symbol_state) == self.final_states:
                        self.regex_accept_status = True
                        return

                    self.simulate_regex_symbol(next_symbol, symbol_state, next_regex)


    def render_node(self, tree_node):
        self.prev_state = self.current_state
        node_classname = tree_node.__class__.__name__
        return self.render_thompson_node_children(node_classname, tree_node)

    def generate_transitions(self):
        graphviz_str_repr = self.digraph.source.split('\n')
        graphviz_states = [
            item.replace(GRAPHVIZ_TAB, '') for item in graphviz_str_repr \
                if GRAPHVIZ_EDGE in item and GRAPHVIZ_EQUAL in item
        ]

        generated_states = [str(gen_state) for gen_state in range(self.current_state + 1)]
        self.transitions = dict.fromkeys(generated_states)

        # Initialize init transitions dict for current state
        self.transitions[str(self.current_state)] = dict()

        for graphviz_state in graphviz_states:
            splitted = graphviz_state.split(' ')
            init, _, final, dest = splitted
            symbol_index = dest.index(GRAPHVIZ_EQUAL)
            symbol = dest[symbol_index + 1]

            try:
                self.transitions[init][symbol].append(final)
            except:
                self.transitions[init] = {symbol: [final]}
        
    def generate_acceptance_state(self):
        self.digraph.node(str(self.current_state), shape='doublecircle')
        self.final_states.append(self.current_state)
        self.final_states = self.current_state

    def render_digraph(self, filename = None, view = True):
        save_file(filename if filename else GRAPHVIZ_OUTPUT_PATH, self.digraph.source)
        self.digraph.render(filename if filename else GRAPHVIZ_OUTPUT_PATH, view=view)
    
    # For Thompson node representation inside digraph
    def render_thompson_node_children(
        self,
        node_type=SymbolNode.__name__,
        node=None
    ):
        if node_type == SymbolNode.__name__:
            return node.symbol
        elif node_type == ConcatNode.__name__:
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                self.render_node(node.x)
            )
            self.current_state += 1
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                self.render_node(node.y)
            )
        elif node_type == OrNode.__name__:
            init_node, mid_node = self.current_state - 1, None
            # Init -> IN Epsilon 1
            self.digraph.edge(
                str(init_node),
                str(self.current_state),
                EPSILON
            )
            self.current_state += 1
            # IN Epsilon 1 -> First Node (X)
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                self.render_node(node.x)
            )

            mid_node = self.current_state
            self.current_state += 1

            # Init -> IN Epsilon 2
            self.digraph.edge(
                str(init_node),
                str(self.current_state),
                EPSILON
            )

            self.current_state += 1

            # IN Epsilon 2 -> Second Node (Y)
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                self.render_node(node.y)
            )

            self.current_state += 1

            # First Node (X) -> OUT Epsilon 1
            self.digraph.edge(
                str(mid_node),
                str(self.current_state),
                EPSILON
            )

            # Second Node (Y) -> OUT Epsilon 1
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                EPSILON
            )

        elif node_type == KleeneNode.__name__:
            # IN Epsilon
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                EPSILON
            )

            first_node = self.current_state - 1
            self.current_state += 1

            # Node (X)
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                self.render_node(node.x)
            )

            # Node (X) -> IN Epsilon (like looped edge on Node)
            self.digraph.edge(
                str(self.current_state),
                str(first_node + 1),
                EPSILON
            )

            self.current_state += 1

            # OUT Epsilon
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                'e'
            )

            # IN Epsilon -> OUT Epsilon
            self.digraph.edge(
                str(first_node),
                str(self.current_state),
                EPSILON
            )

        elif node_type == PlusNode.__name__:
            # REPLACING RULE: r+ = r*r = rr*
            self.render_thompson_node_children(KleeneNode.__name__, node)
            self.current_state += 1

            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                self.render_node(node.x)
            )
            
        elif node_type == NullableNode.__name__:
            # REPLACING RULE: r?  = r|??
            # Copy the same code from OR Node, 
            #   but set the second Node (Y) fixed: y = ??
            init_node, mid_node = self.current_state - 1, None
            # Init -> IN Epsilon 1
            self.digraph.edge(
                str(init_node),
                str(self.current_state),
                EPSILON
            )
            self.current_state += 1
            # IN Epsilon 1 -> First Node (X)
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                self.render_node(node.x)
            )

            mid_node = self.current_state
            self.current_state += 1

            # Init -> IN Epsilon 2
            self.digraph.edge(
                str(init_node),
                str(self.current_state),
                EPSILON
            )

            self.current_state += 1

            # IN Epsilon 2 -> Second Node (Y = ??)
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                EPSILON
            )

            self.current_state += 1

            # First Node (X) -> OUT Epsilon 1
            self.digraph.edge(
                str(mid_node),
                str(self.current_state),
                EPSILON
            )

            # Second Node (Y = ??) -> OUT Epsilon 1
            self.digraph.edge(
                str(self.current_state - 1),
                str(self.current_state),
                EPSILON
            )
        

    def __repr__(self):
        return f"""
            --- NFA ---
            -> Symbols: {self.symbols}
            -> Final State(s): {self.final_states}
            -> Transitions: {self.transitions}
        """
