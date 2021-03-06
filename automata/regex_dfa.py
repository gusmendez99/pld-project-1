# DFA & Graph
from graphviz import Digraph
from pythomata import SimpleDFA
from automata.dfa import DFA
from tokenization.regex import EPSILON
# Common
from string import ascii_uppercase
from utils.common import save_file
from tree.node import *

# Use class conventions for sets: [A-Z]
SET_NAME_STATES = ascii_uppercase
INITIAL_STATE_STR = SET_NAME_STATES[0]
GRAPHVIZ_OUTPUT_PATH = './renders/RegexDFA.gv'


class RegexDFA(DFA):
    def __init__(self, tree, symbols, regex):
        super(RegexDFA, self).__init__(symbols, regex)
        
        # Specific params
        self.states = list()
        self.final_states = set()
        self.tree = tree
        self.augmented_state = None
        self.iterations = 1
        self.current_state = INITIAL_STATE_STR
        self.subset_states = iter(SET_NAME_STATES)

        # Initialize dfa construction
        self.render_node(self.tree)
        self.calculate_follow_pos()

    def calculate_follow_pos(self):
        for node in self.nodes:
            if node.value == OperatorRepr.KLEENE:
                for i in node.last_pos:
                    child_node = next(filter(lambda x: x.id == i, self.nodes))
                    child_node.follow_pos += node.first_pos
            elif node.value == OperatorRepr.CONCAT:
                for i in node.c1.last_pos:
                    child_node = next(filter(lambda x: x.id == i, self.nodes))
                    child_node.follow_pos += node.c2.first_pos

        # Init state & filter nodes with symbols only
        entry_node = self.nodes[-1]
        init_state = entry_node.first_pos
        
        self.nodes = list(filter(lambda x: x.id, self.nodes))
        new_entry_node = self.nodes[-1]
        self.augmented_state = new_entry_node.id
        # Recursion
        val = next(self.subset_states)
        self.calculate_new_states(init_state, val)

    def calculate_new_states(self, state, current_state):
        if not self.states:
            self.states.append(set(state))
            if self.augmented_state in state:
                self.final_states.update(current_state)

        for symbol in self.symbols:
            # Nodes with same symbol in follow_pos
            same_symbols = list(
                filter(lambda x: x.value == symbol and x.id in state, self.nodes)
            )

            # New state with current nodes
            new_state = set()
            for node in same_symbols:
                new_state.update(node.follow_pos)

            if new_state not in self.states and new_state:
                # Extract new state's subset letter
                self.states.append(new_state)
                next_state = next(self.subset_states)

                try:
                    self.transitions[next_state]
                except:
                    self.transitions[next_state] = dict()

                try:
                    existing_states = self.transitions[current_state]
                except:
                    self.transitions[current_state] = dict()
                    existing_states = self.transitions[current_state]

                # Add new state on current symbol
                existing_states[symbol] = next_state
                self.transitions[current_state] = existing_states

                if self.augmented_state in new_state:
                    self.final_states.update(next_state)

                # Recursion
                self.calculate_new_states(new_state, next_state)

            elif new_state:
                # New state already exists
                for i in range(0, len(self.states)):
                    if self.states[i] == new_state:
                        state_ref = SET_NAME_STATES[i]
                        break

                try:
                    existing_states = self.transitions[current_state]
                except:
                    self.transitions[current_state] = dict()
                    existing_states = self.transitions[current_state]

                existing_states[symbol] = state_ref
                self.transitions[current_state] = existing_states

    def render_node(self, tree_node):
        node_classname = tree_node.__class__.__name__
        return self.render_node_children(node_classname, tree_node)

    def render_node_children(
        self,
        node_type=SymbolNode.__name__,
        node=None
    ):
        if node_type == SymbolNode.__name__:
            new_node = RegexDFANode(self.iterations, [self.iterations], [self.iterations], value=node.symbol, nullable=False)
            self.nodes.append(new_node)
            return new_node
        
        elif node_type == OrNode.__name__:
            node_x = self.render_node(node.x)
            self.iterations += 1
            node_y = self.render_node(node.y)

            is_nullable = node_x.nullable or node_y.nullable
            first_pos = node_x.first_pos + node_y.first_pos
            last_pos = node_x.last_pos + node_y.last_pos

            new_node = RegexDFANode(None, first_pos, last_pos, is_nullable, OperatorRepr.OR, node_x, node_y)
            self.nodes.append(new_node)
            return new_node
        
        elif node_type == ConcatNode.__name__:
            node_x = self.render_node(node.x)
            self.iterations += 1
            node_y = self.render_node(node.y)

            is_nullable = node_x.nullable and node_y.nullable
            first_pos = node_x.first_pos + node_y.first_pos if node_x.nullable else node_x.first_pos
            last_pos = node_y.last_pos + node_x.last_pos if node_y.nullable else node_y.last_pos

            new_node = RegexDFANode(None, first_pos, last_pos, is_nullable, OperatorRepr.CONCAT, node_x, node_y)
            self.nodes.append(new_node)
            return new_node

        elif node_type == KleeneNode.__name__:
            node_x = self.render_node(node.x)

            is_nullable = True
            first_pos = node_x.first_pos
            last_pos = node_x.last_pos
            
            new_node = RegexDFANode(None, first_pos, last_pos, is_nullable, OperatorRepr.KLEENE, node_x)
            self.nodes.append(new_node)
            return new_node

        elif node_type == PlusNode.__name__:
            # REPLACING RULE: r+ = r*r = rr*
            node_x = self.render_node(node.x)
            self.iterations += 1
            node_y = self.render_node_children(KleeneNode.__name__, node)

            is_nullable = node_x.nullable and node_y.nullable
            first_pos = node_x.first_pos + node_y.first_pos if node_x.nullable else node_x.first_pos
            last_pos = node_y.last_pos + node_x.last_pos if node_y.nullable else node_y.last_pos

            new_node = RegexDFANode(None, first_pos, last_pos, is_nullable, OperatorRepr.CONCAT, node_x, node_y)
            self.nodes.append(new_node)
            return new_node

        elif node_type == NullableNode.__name__:
            # REPLACING RULE: r?  = r|??
            node_x = RegexDFANode(None, list(), list(), True)
            self.iterations += 1
            node_y = self.render_node(node.x)

            is_nullable = node_x.nullable or node_y.nullable
            first_pos = node_x.first_pos + node_y.first_pos
            last_pos = node_x.last_pos + node_y.last_pos

            new_node = RegexDFANode(None, first_pos, last_pos, is_nullable, OperatorRepr.OR, node_x, node_y)
            self.nodes.append(new_node)
            return new_node
    
    def simulate(self):
        current_state = INITIAL_STATE_STR
        for symbol in self.regex:
            if not symbol in self.symbols:
                self.regex_accept_status = False
                return
            
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
                    return
        
        # Final check for acceptance
        self.regex_accept_status = current_state in self.final_states

    def render_digraph(self, filename = None, view = True):
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

        save_file(filename if filename else GRAPHVIZ_OUTPUT_PATH, graph.source)
        graph.render(filename if filename else GRAPHVIZ_OUTPUT_PATH, format='pdf', view=view)
    
