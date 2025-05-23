# test_imports.py
try:
    from utils import parse_dfa_file
    from dfa import DFA
    print("All imports successful!")
    print("parse_dfa_file function:", parse_dfa_file)
    print("DFA class:", DFA)
except ImportError as e:
    print("IMPORT ERROR:", e)
except Exception as e:
    print("OTHER ERROR:", e)