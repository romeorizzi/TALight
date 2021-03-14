import random

def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]


def dpll(cnf, assignments={}):
    if len(cnf) == 0:
        return True, assignments

    if any([len(c) == 0 for c in cnf]):
        return False, None

    l = __select_literal(cnf)

    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals

    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals

    return False, None

def __to_conj(string):
    conj = string.replace('(','').replace(')','').split("or")
    conj_set = set()
    conj_set.add((conj[0].replace('!',''), (True,False)['!' in conj[0]]))
    for disj in conj[1:]:
        conj_set.add((disj.replace('!',''), (True,False)['!' in disj]))
    return conj_set

def to_cnf(cnf_string):
    """ Given a string that represent a cnf formula it returns an object that represent the given cnf

    Parameters
    ----------
    cnf_string :str
        The cnf formula

    Returns
    -------
    list[set[(string,bool)]]
        The cnf object that represent the given cnf string
    """
    cnf_string = cnf_string.replace(' ','')
    cnf = []
    for conj in cnf_string.split("and"):
        cnf.append(__to_conj(conj))
    return cnf

def __cong_to_string(conj):
    disj_list = list(conj)
    string = "( " + ("!", "")[disj_list[0][1]] + disj_list[0][0] + " "
    for disj in disj_list[1:]:
        string += "or " + ("!", "")[disj[1]] + disj[0] + " "
    return string + ")"

def to_string(cnf):
    """ Given a cnf formulas it returns it in a human readable way
        Ex: [ { ( "x1", True ), ( "x2", True ) }, { ( "x3", True ), ( "x1", False ) } ]
        become "( x1 or x2 ) and ( x3 or !x1 )"

    Parameters
    ----------
    cnf :list[set[(string,bool)]]
        The cnf that we want to return as a string

    Returns
    -------
    str
        The cnf rappresented in a human readable way.
    """
    string = __cong_to_string(cnf[0])

    for conj in cnf[1:]:
        string += " and " + __cong_to_string(conj)
    return string

def get_literals(cnf):
    """Extract the literals from a cnf formula

    Parameters
    ----------
    cnf :list[set[(string,bool)]]
        The cnf from wich we want to extract the literla

    Returns
    -----
    set[str]
        set of the literals in the cnf
    """
    literals = set()
    for conj in cnf:
        for disj in conj:
            literals.add(disj[0])
    return literals


def check_sol(cnf, sol):
    """Check if an assignment is a solution for a cnf

    Parameters
    ----------
    cnf :list[set[(string,bool)]]
        The cnf that we want to solve
    sol :set[(string,bool)]
        The assignment that we want to verify

    Returns
    -------
    bool
        True if the assignment is a solution for the cnf, False otherwise
    """
    return all([bool(disj.intersection(sol)) for disj in cnf])


def random_kcnf(n_literals, n_conjuncts, k=3):
    """Generate a random cnf

        Parameters
        ----------
        n_literals :int
            Number of literals
        n_conjuncts :int
            Number of conjuncts
        k :int
            Indicate the desired k-SAT

        Returns
        -------
        list[set[(string,bool)]]
            A random cnf
        """
    result = []
    for _ in range(n_conjuncts):
        conj = set()
        while (len(conj) < k):
            index = random.randint(1, n_literals)
            conj.add((
                'x' + str(index),
                bool(random.randint(0, 2)),
            ))
        result.append(conj)
    return result