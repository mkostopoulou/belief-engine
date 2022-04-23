from sympy import to_cnf
from src.belief_base import Belief, BeliefBase
from src.resolution import pl_resolution
from itertools import combinations

TAUTOLOGY = 's | ~s'
CONTRADICTION = 's & ~s'
TEST_STATEMENTS = [("p", 0.8), ("q", 0.5), ("p & q", 0.1),
                   ("p|q", 0.9), ("p>>q", 0.75)]
TEST_BELIEF_BASE = [Belief(x[0], x[1]) for x in TEST_STATEMENTS]


def success(base, p):
    p = to_cnf(p)
    if not pl_resolution([], p):
        contracted_base = BeliefBase().contract(base, p)
        return pl_resolution(contracted_base, p)


def inclusion(base, p):
    p = to_cnf(p)
    contracted_base = BeliefBase().contract(base, p)

    return set(contracted_base).issubset(base)


def relevance(base, p, q):
    p = to_cnf(p)
    q = to_cnf(q)

    possible_A_primes = BeliefBase().remainders(base, p)

    for A_prime in possible_A_primes:
        if not q in A_prime:
            if pl_resolution(A_prime.append(q), p):
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
        if pl_resolution(subset,q) != pl_resolution(subset,p):
            return False

        q_follows.append(pl_resolution(subset,q))
        p_follows.append(pl_resolution(subset,p))
    
    return (q_follows == p_follows) and (BeliefBase().contract(base, p) == BeliefBase().contract(base, q))