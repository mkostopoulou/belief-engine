from bs import BeliefBase
from agm_postulates import Postulates
from sympy import *

engine = BeliefBase()
agm_postulates = Postulates(engine)

PROMPT = ">>> "

ACTIONS = [
    'ACTIONS',
    100*"-",
    '1 : Add belief to belief base',
    '2 : Check belief follows the belief base',
    '3 : Contract belief base with a belief',
    '4 : Expand belief base with a belief',
    '5 : Revise belief base with a belief',
    '6 : Print belief base',
    '7 : Reset belief base',
    '8 : Check AGM postulates',
]

REVISION_POSTULATES = [
    'REVISION POSTULATES',
    100*"-",
    '1 : Closure',
    '2 : Success',
    '3 : Inclusion',
    '4 : Vacuity',
    '5 : Consistency',
    '6 : Extensionality',
]

CONTRACTION_POSTULATES = [
    'CONTRACTION POSTULATES',
    100*"-",
    '1 : Closure',
    '2 : Success',
    '3 : Inclusion',
    '4 : Vacuity',
    '5 : Recovery',
    '6 : Extensionality',
]

def request_action(engine: BeliefBase):
    print('Select action:')
    while True:
        print(100 * "=")

        # Request action
        for a in ACTIONS:
            print(a)
        action_input = input(PROMPT)
        if int(action_input) not in range(1, len(ACTIONS) - 1):
            print('* Chose an available action! *')
            continue

        # ...
        handle_action(engine, action_input)

        # Request termination
        print("Do you want to perform more actions? : Type 'n' (stop) | Press Enter (continue)")
        continue_input = input(PROMPT) or 'y'
        if continue_input != 'y':
            break

def handle_action(engine: BeliefBase, action):
    print(100 * "_")
    if action == '1':
        formula_input = request_formula()
        confidence_input = request_confidence()
        print('Adding new belief...')
        engine.add_belief(formula_input, confidence_input)
        print(engine)
    elif action == '2':
        if not base_exists(engine.beliefs):
            return
        formula_input = to_cnf(request_formula())
        print('Checking consistency...')
        base = engine.entails(engine.beliefs, formula_input)
        engine.beliefs = base
        print(engine)
    elif action == '3':
        if not base_exists(engine.beliefs):
            return
        formula_input = to_cnf(request_formula())
        print("Contracting with formula {0}...".format(formula_input))
        base = engine.contract(engine.beliefs, formula_input)
        engine.beliefs = base
        print(engine)
    elif action == '4':
        if not base_exists(engine.beliefs):
            return
        formula_input = to_cnf(request_formula())
        confidence_input = request_confidence()
        print("Expanding with formula {0}...".format(formula_input))
        base = engine.expand(engine.beliefs, formula_input, confidence_input)
        engine.beliefs = base
        print(engine)
    elif action == '5':
        if not base_exists(engine.beliefs):
            return
        formula_input = to_cnf(request_formula())
        confidence_input = request_confidence()
        print("Revising with formula {0}...".format(formula_input))
        base = engine.revise(engine.beliefs, formula_input, confidence_input)
        engine.beliefs = base
        print(engine)
    elif action == '6':
        if not base_exists(engine.beliefs):
            return
        print("Belief Base: {0}".format(engine.beliefs))
    elif action == '7':
        engine.beliefs = []
        print("Belief Base: {0}".format(engine.beliefs))
    elif action == '8':
        if not base_exists(engine.beliefs):
            return
        print('1: Check a revision postulate')
        print('2: Check a contraction postulate')
        type_input = input(PROMPT) or 1

        print('TBA...')
        return  # TODO
        # ...
        request_postulate(type_input)

def request_postulate(type_input):
    print('Select which postulate to check:')
    POSTULATES = REVISION_POSTULATES if type_input == '1' else CONTRACTION_POSTULATES
    while True:
        print(100 * "=")
        # Request action
        for p in POSTULATES:
            print(p)
        postulate_input = input(PROMPT)
        if int(postulate_input) not in range(1, len(POSTULATES)-1):
            print('* Chose an available postulate! *')
            continue
        else:
            print("Type a belief for postulate check")
            print(agm_postulates.check_postulate(postulate_input, type_input))

        # Request termination
        print("Do you want to check more postulates? : Type 'n' (stop) | Press Enter (continue)")
        continue_input = input(PROMPT) or 'y'
        if continue_input != 'y':
            break

def request_formula():
    formula_input = None
    while formula_input is None:
        print("Provide belief formula")
        formula_input = input(PROMPT) or None
    return formula_input

def request_confidence():
    confidence_input = None
    while confidence_input is None:
        print("Provide belief confidence in range (0,1], ex: 0.2")
        confidence_input = float(input(PROMPT)) or None
    return confidence_input

def base_exists(beliefs):
    if not len(beliefs) > 0:
        print("No belief base found. Set up belief(s) first.")
        return False
    return True

if __name__ == "__main__":
    # Request action
    request_action(engine)

    print(100 * "=")
    print("PROCESS TERMINATED")