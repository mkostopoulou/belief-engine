from sympy import *

from src.belief_base import BeliefBase
from argparse import ArgumentParser
from argparse import BooleanOptionalAction
def get_args():
    parser = ArgumentParser(description="Evaluation argument parser")

    parser.add_argument(
        "--confidence",
        help="Value function to use: rank/confidence",
        default= False,
        action=BooleanOptionalAction,
    )

    return parser.parse_args()

PROMPT = ">>> "

ACTIONS = [
    "ACTIONS",
    100 * "-",
    "1 : Add belief to belief base",
    "2 : Check if a given belief follows the belief base",
    "3 : Check contraction of the belief base with a belief",
    "4 : Print belief base",
    "5 : Reset belief base",
    "6 : Quit",
]


def request_action(engine: BeliefBase, confidence:bool = False):
    print("Select action:")
    while True:
        print(100 * "=")

        # Request action
        for a in ACTIONS:
            print(a)
        action_input = input(PROMPT)
        if int(action_input) not in range(1, len(ACTIONS) - 1):
            print("* Chose an available action! *")
            continue

        # ...
        handle_action(engine, action_input, confidence)


def handle_action(engine: BeliefBase, action, confidence:bool = False):
    print(100 * "_")
    if action == "1":
        formula_input = request_formula()
        if confidence:
            confidence_input = request_confidence()
        else:
            confidence_input = None
        print("Adding new belief...")
        engine.add_belief(formula_input, confidence_input)
        print(engine)
    elif action == "2":
        if not base_exists(engine.beliefs):
            return
        formula_input = to_cnf(request_formula())
        print("Checking entailment...")
        if engine.entails(engine.beliefs, formula_input):
            print(f"{formula_input} entails from the current belief base!")
        else:
            print(f"{formula_input} does not entail from the current belief base!")
    elif action == "3":
        if not base_exists(engine.beliefs):
            return
        formula_input = to_cnf(request_formula())
        print(f"Contracting with formula {formula_input}...")
        base = engine.contract(engine.beliefs, formula_input)
        print(f"The result of contraction would be a belief base consisting of {base}")
    elif action == "4":
        if not base_exists(engine.beliefs):
            return
        print(f"Belief Base consists of {engine}")
    elif action == "5":
        engine.beliefs = []
        print(f"Belief Base consists of {engine}")
    elif action == "6":
        print("Thanks, Bye!")
        exit()


def request_formula():
    formula_input = None
    while formula_input is None:
        print("Provide a belief formula")
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
    args = get_args()

    engine = BeliefBase()

    request_action(engine, args.confidence)

    print(100 * "=")
    print("PROCESS TERMINATED")
