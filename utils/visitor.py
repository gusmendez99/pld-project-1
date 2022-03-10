class VisitorNode:
    def __init__(self, state, next_states):
        self.state = state
        self.has_been_visited = False
        self.next_states = next_states

    def __repr__(self):
        return f"""
            State: {self.state}
            Visited?: {self.has_been_visited}
            -> Next States: {self.next_states}'
        """