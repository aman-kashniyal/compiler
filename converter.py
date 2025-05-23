def convert_dfa_to_regex(dfa):
    import copy

    print("DEBUG: converter.py received dfa.transitions type:", type(dfa.transitions))
    print("DEBUG: sample item:", list(dfa.transitions.items())[:1])

    # Step 1: Setup GNFA with proper state naming
    states = copy.deepcopy(dfa.states)
    
    # Create unique new start/end states
    new_start = "START"
    new_end = "END"
    while new_start in states or new_end in states:
        new_start += "_"
        new_end += "_"

    states = [new_start] + states + [new_end]
    transitions = {}

    # Initialize all transitions as empty set (∅)
    for s1 in states:
        for s2 in states:
            transitions[(s1, s2)] = "∅"

    # Add original DFA transitions
    for item in dfa.transitions.items():
        print("DEBUG: Item being unpacked in converter.py:", item, "Type:", type(item))
        (from_state, symbol), to_state = item
        key = (from_state, to_state)
        if transitions[key] != "∅":
            transitions[key] = f"({transitions[key]}+{symbol})"
        else:
            transitions[key] = symbol

    # Add ε-transitions
    transitions[(new_start, dfa.start_state)] = "ε"
    for accept_state in dfa.accept_states:
        transitions[(accept_state, new_end)] = "ε"

    # Step 2: State elimination
    for state in dfa.states:  # Only eliminate original states
        # Find all incoming and outgoing transitions
        in_trans = {s: trans for (s, q), trans in transitions.items() 
                   if q == state and s != state}
        out_trans = {q: trans for (q, s), trans in transitions.items() 
                    if q == state and s != state}
        loop = transitions.get((state, state), "∅")

        # Update all possible paths through this state
        for i in in_trans:
            for j in out_trans:
                r1 = in_trans[i]
                r2 = out_trans[j]
                if loop != "∅":
                    new_trans = f"{r1}({loop})*{r2}"
                else:
                    new_trans = f"{r1}{r2}"

                key = (i, j)
                if transitions[key] != "∅":
                    transitions[key] = f"({transitions[key]}+{new_trans})"
                else:
                    transitions[key] = new_trans

        # Remove the state
        for s in states:
            transitions.pop((s, state), None)
            transitions.pop((state, s), None)

    # Final cleanup
    regex = transitions.get((new_start, new_end), "∅")
    regex = regex.replace("(∅+", "(").replace("+∅)", ")")
    return regex if regex != "∅" else "No accepting paths"