from typing import Tuple
from sympy.logic.boolalg import to_cnf
from sympy import Not, Or
from itertools import combinations
from .utils import associate, disjuncts, conjuncts


def pl_resolution(beliefs: list, formula, verbose: bool = False):
    """
    Take a `BeliefBase` and check if a `formula` follows from it.

    Arguments:
        bb: (obj: BeliefBase) A valid BeliefBase
        formula: (obj: sympy.basic) A CNF representation of the formula we want to check
    """

    neg_formula = [formula for formula in conjuncts(to_cnf(Not(formula)))]

    clauses = set(
        [formula for b in beliefs for formula in conjuncts(b.sentence)] + neg_formula
    )

    if verbose:
        print(f"Starting with {clauses}")

    new_clauses = set()

    while True:
        pairs = combinations(list(clauses), 2)
        for pair in pairs:
            if verbose:
                print(f">> Resolving {pair[0]} and {pair[1]}")
            resolvents, contradiction = pl_resolve(pair)
            if len(resolvents) > 0:
                if verbose:
                    print(f"> Resolvents are: {resolvents}")
            else:
                if verbose:
                    print("> No resolvement")
            if contradiction:
                return True
            if len(resolvents) > 0:
                new_clauses = new_clauses.union(resolvents)
        if new_clauses.issubset(clauses):
            return False

        clauses = clauses.union(new_clauses)


def pl_resolve(pair: Tuple):

    ci = pair[0]
    cj = pair[1]

    comp_ci = disjuncts(ci)
    comp_cj = disjuncts(cj)

    new_clause = []

    for ci in comp_ci:
        for cj in comp_cj:
            if ci == Not(cj):
                output = list(
                    set(
                        [frml for frml in comp_cj if frml != cj]
                        + [frml for frml in comp_ci if frml != ci]
                    )
                )
                new_clause.append(associate(Or, output))

    contradiction = False in new_clause

    return set(new_clause), contradiction
