class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = [s.strip() for s in states]
        self.alphabet = [a.strip() for a in alphabet]
        self.start_state = start_state.strip()
        self.accept_states = [a.strip() for a in accept_states]
        # Only build dict if transitions is a list (of 3-tuples)
        if isinstance(transitions, list):
            self.transitions = self.build_transition_dict(transitions)
        else:
            self.transitions = transitions
        self.validate()

    def build_transition_dict(self, transitions):
        transition_dict = {}
        for from_state, symbol, to_state in transitions:
            from_state = from_state.strip()
            to_state = to_state.strip()
            symbol = symbol.strip()
            if (from_state, symbol) in transition_dict:
                raise ValueError(f"Non-deterministic transition: {from_state} on {symbol}")
            transition_dict[(from_state, symbol)] = to_state
        return transition_dict

    def validate(self):
        import traceback
        print("DEBUG: self.transitions type:", type(self.transitions))
        if isinstance(self.transitions, dict):
            items = self.transitions.items()
            print("DEBUG: sample dict item:", list(self.transitions.items())[:1])
        elif isinstance(self.transitions, list):
            items = [((from_state, symbol), to_state) for from_state, symbol, to_state in self.transitions]
            print("DEBUG: sample list item:", self.transitions[:1])
        else:
            raise ValueError("Unknown transitions type: " + str(type(self.transitions)))
        traceback.print_stack()
        if self.start_state not in self.states:
            raise ValueError(f"Start state {self.start_state} not in states list")
        print("DEBUG: Items iterable in dfa.py validate:", items, "Type:", type(items))
        for state in self.accept_states:
            if state not in self.states:
                raise ValueError(f"Accept state {state} not in states list")
        for item in items:
            print("DEBUG: Attempting to unpack item in dfa.py validate:", item, "Type:", type(item))
            if not isinstance(item, tuple) or len(item) != 2 or not isinstance(item[0], tuple) or len(item[0]) != 2:
                raise ValueError(f"Validation Error: Unexpected transition item structure in dfa.py: {item}. Expected ((state, symbol), next_state)")
            (from_state, symbol), to_state = item
            if from_state not in self.states or to_state not in self.states:
                raise ValueError(f"Transition {from_state}→{to_state} uses undefined states")
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol {symbol} not in alphabet")

    def get_transitions(self):
        return [(from_s, sym, to_s) for (from_s, sym), to_s in self.transitions.items()]