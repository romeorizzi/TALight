import random
import re

def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]


def __dpll(cnf, assignments={}):
    if len(cnf) == 0:
        return True, assignments

    if any([len(c) == 0 for c in cnf]):
        return False, None

    l = __select_literal(cnf)

    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = __dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals

    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = __dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals

    return False, None


def solve(cnf):
    """ Given a cnf, try to find a possible solution.

    Parameters
    ----------
    cnf :list[set[(string,bool)]]
        The cnf formula

    Returns
    -------
    (bool, set[(string,bool)])
        A tuple where the first element is a boolean and tells if the cnf is solvable
        and the second element is an assignment that satisfy the formula if the cnf is solvable, a empty set otherwise.
    """
    (solvable, solution) = __dpll(cnf)
    if not solvable:
        return solvable, {}

    literals = get_literals(cnf)
    for literal in literals:
        if not literal in solution:
            solution[literal] = False
    sol_set = {(k, values) for k, values in solution.items()}
    return solvable, sol_set


def __to_conj(string):
    conj = string.replace('(', '').replace(')', '').split("or")
    conj_set = set()
    conj_set.add((conj[0].replace('!', ''), (True, False)['!' in conj[0]]))
    for disj in conj[1:]:
        conj_set.add((disj.replace('!', ''), (True, False)['!' in disj]))
    return conj_set


def to_cnf(cnf_string):
    """ Given a cnf in the form of a string, returns it as an object

    Parameters
    ----------
    cnf_string :str
        The cnf formula

    Returns
    -------
    list[set[(string,bool)]]
        The cnf object that represent the given cnf string
    """
    cnf_string = cnf_string.replace(' ', '')
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


def random_kcnf(n_literals, k=3):
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
    literals = []
    for n in range(1, n_literals + 1):
        literals.append('x' + str(n))

    n = 0
    while (n + 2 * k < n_literals * 3):
        values = [bool(random.randint(0, 1)) for _ in range(0, k)]
        conj = set(zip(random.sample(literals, k), values))
        result.append(conj)
        n += k

    return result

def dimacs_file_to_cnf(file_path):
    """ Load a cnf from a dimacs file

        Parameters
        ----------
        file_path :string
            Path of the file that contains the cnf wirtten in dimacs format

        Returns
        -------
        list[set[(string,bool)]]
            The object that represents the loaded cnf
        """
    cnf = []
    f = open(file_path, "r")
    for line in f:
        if line[0] != 'c' and line[0] != 'p':
            conj = set()
            for disj in line.split(" ")[:-1]:
                if (disj[0] == '-'):
                    to_add = ('x' + disj[1:], False)
                else:
                    to_add = ('x' + disj, True)
                conj.add(to_add)
            cnf.append(conj)
    f.close()
    return cnf

def saved_certificate_to_cnf(file_path):
    """ Load a certificate from file

        Parameters
        ----------
        file_path :string
            Path of the file that contains the certificate fo a cnf

        Returns
        -------
        set[(string,bool)]
            The object that represents the loaded certificate
        """
    cert = set()
    f = open(file_path, "r")
    for line in f:
        if line[0] == 'v' and line[2] != '0':
            for leterals in line.split(' ')[1:]:
                numeric_leterals =int(leterals)
                cert.add(('x{}'.format(abs(numeric_leterals)),True if numeric_leterals > 0 else False))
    return cert


def parse_certificate(cert_string):
    """
    Given a certificate in the form of a string, returns it as an object

    Parameters
    ----------
    cert_string :str
        The certificate formula

    Returns
    -------
    set[(string,bool)]
        The certificate object that represent the given cnf certificate
    """
    ass = set()
    cert_string = cert_string.replace(' ','')
    for x in cert_string.split('),('):
        x = x.replace(')','').replace('(','').replace('{','').replace('}','').replace('\'','')
        tmp = x.split(',')
        ass.add(((tmp[0],tmp[1] == 'True')))
    return ass
