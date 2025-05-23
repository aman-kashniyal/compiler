from dfa import DFA

def parse_dfa_file(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]

    states = []
    alphabet = []
    start_state = ""
    accept_states = []
    transitions = []

    for line in lines:
        if line.startswith("states:"):
            states = [s.strip() for s in line.split(":")[1].split(",") if s.strip()]
        elif line.startswith("alphabet:"):
            alphabet = [a.strip() for a in line.split(":")[1].split(",") if a.strip()]
        elif line.startswith("start:"):
            start_state = line.split(":")[1].strip()
        elif line.startswith("accept:"):
            accept_states = [a.strip() for a in line.split(":")[1].split(",") if a.strip()]
        elif line.startswith("transitions:"):
            continue
        else:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                raise ValueError(f"Invalid transition format: {line}")
            transitions.append((parts[0], parts[1], parts[2]))

    return DFA(states, alphabet, transitions, start_state, accept_states)