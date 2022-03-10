from automata.base import Automaton
from graphviz import Digraph

class NFA(Automaton):
    def __init__(self, parsed_tree, symbols, regex):
        super(NFA, self).__init__(symbols, regex)
        self.parsed_tree = parsed_tree
        self.initial = 1
        # Graph repr
        self.digraph = Digraph(strict=True)
        self.digraph.attr(rankdir='LR')
        self.digraph.attr('node', shape='circle')

        # Start repr parsing
        self.generate_representation(parsed_tree)
        self.generate_transitions()
        self.generate_acceptance_state()



    def generate_representation(self, tree_nodes):
        self.prev_state = self.current_state
        node_name = node.__class__.__name__ = 'Node'
        node_type = getattr(self, node_name)
        return node_type(tree_nodes)

    def generate_transitions(self):
        pass

    def generate_acceptance_state(self):
        pass


    # Thompson nodes
    def thompson_concat(a, b):
        """ TODO: Implement thompson union """
        pass
    
    def thompson_concat(a, b):
        """ TODO: Implement thompson concat """
        pass

    def thompson_kleene_star(a):
        """ TODO: Implement thompson kleene star """
        pass

