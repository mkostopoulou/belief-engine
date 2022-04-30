from sympy import to_cnf, Not
from belief_base import Belief, BeliefBase
from resolution import pl_resolution
from itertools import combinations

TAUTOLOGY = "s | ~s"
CONTRADICTION = "s & ~s"
TEST_STATEMENTS = [
    ("p", 0.8),
    ("q", 0.5),
    ("p & q", 0.1),
    ("p|q", 0.9),
    ("p>>q", 0.75),
    ("q>>p", 0.75),
]
TEST_BELIEF_BASE = [Belief(to_cnf(x[0]), x[1]) for x in TEST_STATEMENTS]
TEST_BELIEF_BASE_UN = [Belief(to_cnf("p & q"), 0.1)]


def success(base, p):
    p = to_cnf(p)
    if not pl_resolution([], p):
        base = BeliefBase(TEST_BELIEF_BASE)
        contracted_base = base.contract(base.beliefs, p)

        return not pl_resolution(contracted_base, p, verbose=False)


def inclusion(base, p):
    p = to_cnf(p)
    contracted_base = BeliefBase().contract(base, p)

    return set(contracted_base).issubset(base)


def relevance(base, p, q):
    p = to_cnf(p)
    q = Belief(to_cnf(q), 0.95)

    possible_A_primes = BeliefBase().remainders(base, p)
    for A_prime in possible_A_primes:
        if not q in A_prime:
            A_prime.add(q)
            if pl_resolution(A_prime, p):
                return True
    return False


def uniformity(base, p, q):
    q = to_cnf(q)
    p = to_cnf(p)

    A_primes = []
    for L in range(0, len(base) + 1):
        for subset in combinations(base, L):
            if len(subset) > 0:
                A_primes.append(list(subset))

    q_follows = []
    p_follows = []

    for subset in A_primes:
        if pl_resolution(subset, q) != pl_resolution(subset, p):
            return False

        q_follows.append(pl_resolution(subset, q))
        p_follows.append(pl_resolution(subset, p))

    return (q_follows == p_follows) and (
        BeliefBase().contract(base, p) == BeliefBase().contract(base, q)
    )


def consistency(base, p):
    p = to_cnf(p)

    if pl_resolution([],Not(p)):
        print("p is a contradiction")
        return False

    if pl_resolution(base, to_cnf("b")):
        print("There is a contradiction in the belief base")

        test_base = BeliefBase(base)
        new_base = test_base.revise(base,p)

        print("Something wrong is going to happen here")
        return False
    
    return True
    


def vacuity(base, p):
    p = to_cnf(p)
    notp = Not(p)

    if not pl_resolution(base, notp):
        revised = base.append(p)
    
    revised_auto = BeliefBase.revise(base, p)

    return revised == revised_auto

def extensionality(base,p):
    pass


if __name__ == "__main__":

    print(success(TEST_BELIEF_BASE, "q"))
    print(inclusion(TEST_BELIEF_BASE, "q"))
    print(relevance(TEST_BELIEF_BASE, "p", "p & q"))
    print(uniformity(TEST_BELIEF_BASE_UN, "p", "q"))
