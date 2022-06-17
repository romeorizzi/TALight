#!/usr/bin/env python3

from sys import stderr
from typing import Optional, List, Dict, Callable

from RO_verify_submission_gen_prob_lib import verify_submission_gen

instance_objects_spec = [
    ('Knapsack_Capacity',int),
    ('labels','list_of_str'),
    ('costs','list_of_int'),
    ('vals','list_of_int'),
    ('LB','list_of_int'),
    ('UB','list_of_int'),
    ('forced_out','list_of_str'),
    ('forced_in','list_of_str'),
]
additional_infos_spec=[
    ('partialDPtable','matrix_of_int')
]
answer_objects_spec = {
    'opt_sol':'list_of_str',
    'opt_val':'int',
    'num_opt_sols':'int',
    'list_opt_sols':'list_of_list_of_str',
    'DPtable_opt_val':'matrix_of_int',
    'DPtable_num_opts':'matrix_of_int',
}
answer_objects_implemented = ['opt_sol','opt_val','num_opt_sols','DPtable_opt_val','DPtable_num_opts','list_opt_sols']
request_setups = {'MAX_NUM_SOLS_IN_LIST':10, 'MAX_NUM_OPT_SOLS_IN_LIST':30}

def sum_of_costs_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["costs"], instance["labels"]) if ele in ordered_list_of_elems])

def sum_of_vals_over(instance, ordered_list_of_elems):
    return sum([peso for peso,ele in zip(instance["vals"], instance["labels"]) if ele in ordered_list_of_elems])

def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    n = len(instance["labels"]) 
    if len(instance["costs"]) != n:
        print(f'Errore: len(instance["costs"])={len(instance["costs"])} != {n}=len(instance["labels"])')    
        exit(0)
    if len(instance["vals"]) != n:
        print(f'Errore: len(instance["vals"])={len(instance["vals"])=} != {n}=len(instance["labels"])')    
        exit(0)
    for ele in instance["forced_in"]:
        if ele in instance["forced_in"]:
            print(f'Errore: the element {ele} containd in the list `forced_in` is not contained in the list `labels` = {instance["labels"]}.\nIndeed, `forced_in` = {instance["forced_in"]}.')
            exit(0)
    for ele in instance["forced_out"]:
        if ele not in instance["labels"]:
            print(f'Errore: the element {ele} containd in the list `forced_out` is not contained in the list `labels` = {instance["labels"]}.\nIndeed, `forced_out` = {instance["forced_out"]}.')
            exit(0)
        if ele in instance["forced_in"]:
            print(f'Errore: the element {ele} is containd BOTH in the list `forced_out` and in the list `forced_in` = {instance["forced_in"]}.\nIndeed, `forced_out` = {instance["forced_out"]}.')
            exit(0)
    LB = instance["LB"]
    UB = instance["UB"]
    if len(UB)+len(LB) > 0:
        if len(UB)*len(LB)==0:
            print(f'Errore: delle liste UB ed LB non puoi averne esattamente una vuota. O sono entrambe vuote o entrambe devono essere lunghe quanto la lista `labels`')
            exit(0)
        if len(forced_out)+len(forced_in) > 0:
            print(f'Errore: quando le liste `forced_out` e/o `forced_in` sono impostate a liste NON vuote le liste `UB` e `LB` devono essere lasciate vuote')    
            exit(0)
        if len(UB) != n:
            print(f'Errore: len(instance["UB"])={len(UB)=} != {n}=len(instance["labels"])')    
            exit(0)
        if len(LB) != n:
            print(f'Errore: len(instance["LB"])={len(LB)=} != {n}=len(instance["labels"])')    
            exit(0)
    else:
        LB = [0]*n
        UB = [1]*n        
    cost_forced_in = 0
    for ele,indx in zip(instance["labels"],range(n)):
        if LB[indx] > UB[indx]:
            print(f'Errore: UB[{ele}]= {UB[ele]}>LB{LB[ele]} =LB[{ele}].')
            exit(0)
        if ele in instance["forced_in"]:
            LB[indx] = 1
        if ele in instance["forced_out"]:
            UB[indx] = 0
        cost_forced_in += LB[indx]*instance["costs"][indx]
    if cost_forced_in > instance["Knapsack_Capacity"]:
        if len(instance["forced_in"]) > 0:
            print(f'Errore: il costo/peso complessivo degli elementi obbligati ({cost_forced_in}) già eccede la capacità dello zaino {instance["Knapsack_Capacity"]}')
        else:
            print(f'Errore: il prodotto scalare del vettore `cost` e il vettore dei lower bounds `LB` già eccede la capacità dello zaino {instance["Knapsack_Capacity"]}')
        exit(0)

        
def solver(input_to_oracle):
    #print(f"input_to_oracle={input_to_oracle}",file=stderr)
    I = input_to_oracle["input_data_assigned"]
    #print(f"Instance={I}",file=stderr)
    n = len(I["labels"])
    LB = I["LB"]
    UB = I["UB"]
    if len(UB)==0:
        LB = [0]*n
        UB = [1]*n

    DPtable_opt_val = [[0 for j in range(I["Knapsack_Capacity"]+1)] for i in range(n+1)]
    DPtable_num_opts = [[1 for j in range(I["Knapsack_Capacity"]+1)] for i in range(n+1)]
    for obj_label,i in zip(I["labels"],range(1,1+n)): # i=object index, but also i=row_index (row_indexes of the DP table start from zero, the first row is already computed as a base case, before entering this for loop)
        obj_cost = I["costs"][i-1]; obj_val = I["vals"][i-1]
        if obj_label in I["forced_in"]:
            LB[i-1] = 1
        if obj_label in I["forced_out"]:
            UB[i-1] = 0
        obj_LB = LB[i-1]; obj_UB = UB[i-1]
        for j in range(I["Knapsack_Capacity"]+1): # j=column_index of the DP table 
            DPtable_opt_val[i][j] = DPtable_opt_val[i-1][j]
            DPtable_num_opts[i][j] = DPtable_num_opts[i-1][j]
            obj_times = 1
            while obj_times <= obj_UB and obj_times*obj_cost <= j:
                #print(f"i={i}, obj_label={obj_label}, obj_cost={obj_cost}, obj_val={obj_val}, j={j}, obj_times={obj_times}",file=stderr)
                if DPtable_opt_val[i][j] == obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                    DPtable_num_opts[i][j] += DPtable_num_opts[i-1][j-obj_times*obj_cost]
                elif DPtable_opt_val[i][j] < obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                    DPtable_opt_val[i][j] = obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]
                    DPtable_num_opts[i][j] = DPtable_num_opts[i-1][j]
                obj_times += 1
        #print(f"DPtable_opt_val={DPtable_opt_val}",file=stderr)
        #print(f"DPtable_num_opts={DPtable_num_opts}",file=stderr)
        
    #print(f"DPtable_opt_val={DPtable_opt_val}",file=stderr)
    #print(f"DPtable_num_opts={DPtable_num_opts}",file=stderr)

    def yield_opt_sols_list(i,j,promise,num_opt_sols_MAX):
        assert promise >= 0 and j >= 0 and i >= 0   
        if i == 0:
            assert promise == 0
            yield []
            return
        obj_label = I["labels"][i-1]
        obj_cost = I["costs"][i-1]; obj_val = I["vals"][i-1]
        obj_LB = LB[i-1]; obj_UB = UB[i-1]
        #print(f'\ni={i}\nj={j}\npromise={promise}\nobj_label={obj_label}\nobj_cost={obj_cost}\nobj_val={obj_val}\nopt_sol={opt_sol}', file=stderr)
        for obj_times in range(obj_UB+1):
            if obj_times*obj_cost > j:
                break
            if promise <= obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]:
                assert promise == obj_times*obj_val + DPtable_opt_val[i-1][j-obj_times*obj_cost]
                for opt_sol in yield_opt_sols_list(i-1,j-obj_times*obj_cost,promise-obj_times*obj_val,num_opt_sols_MAX):
                    if num_opt_sols_MAX > 0:
                        yield opt_sol + [obj_label]*obj_times
                        num_opt_sols_MAX -= 1

    if n == 0:
        opt_val = 0; num_opt_sols = 1; list_opt_sols = [[]]
    else:
        opt_val=DPtable_opt_val[i][j]; num_opt_sols=DPtable_num_opts[i][j]
    num_opt_sols_MAX=input_to_oracle["request_setups"]['MAX_NUM_OPT_SOLS_IN_LIST']
    #print(f"num_opt_sols_MAX={num_opt_sols_MAX}")
    list_opt_sols = list(yield_opt_sols_list(i,j,promise=opt_val,num_opt_sols_MAX=num_opt_sols_MAX))
    opt_sol = list_opt_sols[0]
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nnum_opt_sols={num_opt_sols}\nDPtable_opt_val={DPtable_opt_val}\nDPtable_num_opts={DPtable_num_opts}\nlist_opt_sols={list_opt_sols}", file=stderr)

    
from dataclasses import dataclass
from sys import stderr


Cell = tuple[int, int]
Field = list[list[int]]


def parse_cell(cell: str) -> Cell:
    # remove parenthesis
    cell = cell[1:-1]
    row, col = cell.split(",")
    row, col = ord(row.lower()) - ord("a"), int(col)
    return (row, col)


def free(field: Field, row: int, col: int) -> bool:
    """Checks whether a cell is free or forbidden."""
    return field[row][col] != -1


def check_matrix_shape(f: Field) -> bool:
    cols = len(f[0])
    for row in f:
        if len(row) != cols:
            return False
    return True


def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    instance_objects = ['field', 'diag', 'partialDP_to',
                        'partialDP_from', 'cell_from', 'cell_to', 'cell_through']

    field = instance['field']
    rows, cols = len(field), len(field[0])
    # TODO: ask whether this check is necessary for the type 'matrix_of_int'
    if not check_matrix_shape(field):
        print(f"Error: field must be a matrix")
        exit(0)

    for row in range(field):
        for col in range(row):
            if (c := field[row][col]) < -1:
                print(f"Error: value {c} in ({row},{col}) is not allowed")
                exit(0)

    if field[0][0] == -1 or field[-1][-1] == -1:
        print(f"Error")
        exit(0)

    # TODO: validate cells coordinates
    cell_from = parse_cell(instance['cell_from'])
    cell_to = parse_cell(instance['cell_to'])
    cell_through = parse_cell(instance['cell_through'])


def dptable_num_to_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for counting the number of paths.
    Construction starts from the cell in the top-left corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]
    # NOTE: cells default to zero, in some cases there is no need to assing values
    t[0][0] = 1
    for i in range(1, cols):
        if free(f, 0, i):
            t[0][i] = t[0][i - 1]

    for i in range(1, rows):
        if free(f, i, 0):
            t[i][0] = t[i - 1][0]

    if diag:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    t[i][j] = t[i][j - 1] + t[i - 1][j] + t[i - 1][j - 1]

    else:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    t[i][j] = t[i][j - 1] + t[i - 1][j]

    return t


def dptable_num_from_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for counting the number of paths.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]

    # NOTE: cells default to zero, in some cases there is no need to assing values
    t[-1][-1] = 1
    for i in reversed(range(cols - 1)):
        if free(f, -1, i):
            t[-1][i] = t[-1][i + 1]

    for i in reversed(range(rows - 1)):
        if free(f, i, -1):
            t[i][-1] = t[i + 1][-1]

    if diag:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = t[i][j + 1] + t[i + 1][j] + t[i + 1][j + 1]

    else:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = t[i][j + 1] + t[i + 1][j]

    return t


def dptable_opt_to_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]

    t[0][0] = f[0][0]
    for i in range(1, cols):
        if free(f, 0, i):
            t[0][i] = f[0][i] + t[0][i - 1]

    for i in range(1, rows):
        if free(f, i, 0):
            t[i][0] = f[i][0] + t[i - 1][0]

    if diag:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    t[i][j] = f[i][j] + \
                        max([t[i][j - 1], t[i - 1][j], t[i - 1][j - 1]])

    else:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    t[i][j] = f[i][j] + max(t[i][j - 1], t[i - 1][j])

    return t


def dptable_opt_from_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]

    t[-1][-1] = f[-1][-1]
    for i in reversed(range(cols - 1)):
        if free(f, -1, i):
            t[-1][i] = f[-1][i] + t[-1][i + 1]

    for i in reversed(range(rows - 1)):
        if free(f, i, -1):
            t[i][-1] = f[i][-1] + t[i + 1][-1]

    if diag:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = f[i][j] + \
                        max([t[i][j + 1], t[i + 1][j], t[i + 1][j + 1]])

    else:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = f[i][j] + max(t[i][j + 1], t[i + 1][j])

    return t


@dataclass
class NumOptCell:
    count: int  # the count of optimal paths ending at this cell
    value: int  # the optimal value of a path ending at this cell


def dptable_num_opt_to_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    # NOTE: store (num_of_paths, opt_value) for each cell
    t = [[NumOptCell(count=0, value=0) for _ in range(cols)]
         for _ in range(rows)]

    t[0][0].count = 1
    t[0][0].value = f[0][0]
    for i in range(1, cols):  # fill first row
        if free(f, 0, i):
            t[0][i].count = t[0][i - 1].count
            t[0][i].value = f[0][i] + t[0][i - 1].value

    for i in range(1, rows):  # fill first column
        if free(f, i, 0):
            t[i][0].count = t[i - 1][0].count
            t[i][0].value = f[i][0] + t[i - 1][0].value

    if diag:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    neighbors = [t[i][j - 1], t[i - 1][j], t[i - 1][j - 1]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    else:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    neighbors = [t[i][j - 1], t[i - 1][j]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    return as_tuple_matrix(t)


def dptable_num_opt_from_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    # NOTE: store (num_of_paths, opt_value) for each cell
    t = [[NumOptCell(count=0, value=0) for _ in range(cols)]
         for _ in range(rows)]

    t[-1][-1].count = 1
    t[-1][-1].value = f[-1][-1]
    for i in reversed(range(cols - 1)):  # fill last row
        if free(f, -1, i):
            t[-1][i].count = t[-1][i + 1].count
            t[-1][i].value = f[-1][i] + t[-1][i + 1].value

    for i in reversed(range(rows - 1)):  # fill last column
        if free(f, i, -1):
            t[i][-1].count = t[i + 1][-1].count
            t[i][-1].value = f[i][-1] + t[i + 1][-1].value

    if diag:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    neighbors = [t[i][j + 1], t[i + 1][j], t[i + 1][j + 1]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    else:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    neighbors = [t[i][j + 1], t[i + 1][j]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    return as_tuple_matrix(t)


def as_tuple_matrix(table: list[list[NumOptCell]]) -> list[list[Cell]]:
    return [[(x.count, x.value) for x in row] for row in table]


def build_opt_path(dptable: Field, diag: bool = False) -> list[Cell]:
    rows, cols = len(dptable), len(dptable[0])
    row, col = 0, 0
    path = []
    if diag:
        while ():
            pass

    else:
        while ():
            pass

    return path


def build_all_opt_path(f: Field, dptable: Field, diag: bool = False) -> list[list[Cell]]:
    rows, cols = len(f), len(f[0])
    paths = []
    
    def _build_exclude_diag(path: list[Cell]):
        if (cell:= path[-1]) != (rows - 1, cols -1): # not last cell
            row, col = cell
            value_on_opt_path = dptable[row][col] - f[row][col]
            if row < (rows - 1): # check the cell in the next row
                if dptable[row + 1][col] == value_on_opt_path:
                    _build_exclude_diag(path + [(row + 1, col)])

            if col < (cols - 1): # check the cell in the next column
                if dptable[row][col + 1] == value_on_opt_path:
                    _build_exclude_diag(path + [(row, col + 1)])
        else:
            paths.append(path)

    def _build_include_diag(path: list[Cell]):
        if (cell:= path[-1]) != (rows - 1, cols -1): # not last cell
            row, col = cell
            value_on_opt_path = dptable[row][col] - f[row][col]
            if row < (rows - 1): # check the cell in the next row
                if dptable[row + 1][col] == value_on_opt_path:
                    _build_include_diag(path + [(row + 1, col)])

            if col < (cols - 1): # check the cell in the next column
                if dptable[row][col + 1] == value_on_opt_path:
                    _build_include_diag(path + [(row, col + 1)])

            if row < (rows - 1) and col < (cols - 1):
                if dptable[row + 1][col + 1] == value_on_opt_path:
                    _build_include_diag(path + [(row + 1, col + 1)])
        else:
            paths.append(path)

    if diag:
        _build_include_diag([(0,0)])
    else:
        _build_exclude_diag([(0,0)])
    return paths


def conceal(dptable: Field):
    """
    Conceals some cells of the table
    """
    # TODO: discuss how to select the cells to obfuscate
    cells = []
    for row, col in cells:
        dptable[row][col] = -1


def solver(input_to_oracle):
    I = input_to_oracle["instance"]

    # extract and parse inputs
    field = I["field"]
    diag = I["diag"]
    cell_to = (0, 0)
    cell_from = (0, 0)
    cell_through = (0, 0)

    # compute tables
    DPtable_num_to = dptable_num_to_cell(field, diag=diag)
    DPtable_num_from = dptable_num_from_cell(field, diag=diag)

    DPtable_opt_to = dptable_opt_to_cell(field, diag=diag)
    DPtable_opt_from = dptable_opt_from_cell(field, diag=diag)

    DPtable_num_opt_to = dptable_num_opt_to_cell(field, diag=diag)
    DPtable_num_opt_from = dptable_num_opt_from_cell(field, diag=diag)

    # retrieve and format outputs
    # TODO: adapt solutions to different 'from' and 'to' cells
    num_paths = DPtable_num_to[-1][-1]
    num_opt_paths = DPtable_num_opt_to[-1][-1]
    opt_val = DPtable_opt_to[-1][-1]
    list_opt_path = build_all_opt_path(field, DPtable_opt_from, diag=diag)
    opt_path = list_opt_path[0]


    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers



class verify_submission_problem_specific(verify_submission_gen):
    def __init__(self, SEF,input_data_assigned:Dict, long_answer_dict:Dict, request_setups:str):
        super().__init__(SEF,input_data_assigned, long_answer_dict, request_setups)

    def verify_format(self, SEF):
        if not super().verify_format(SEF):
            return False
        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'num_opt_sols' in self.goals:
            g = self.goals['num_opt_sols']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            if type(g.answ) != list:
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di oggetti (esempio ['{self.I.labels[0]}','{self.I.labels[2]}']). Hai invece immesso `{g.answ}`.")
            for ele in g.answ:
                if ele not in self.I.labels:
                    return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista `{g.alias}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {self.I.labels}.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ammissibilità di `{g.alias}`")
        return True
                
    def set_up_and_cash_handy_data(self):
        if 'opt_sol' in self.goals:
            self.sum_vals = sum([val for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in self.goals['opt_sol'].answ])
            self.sum_costs = sum([cost for ele,cost,val in zip(self.I.labels,self.I.costs,self.I.vals) if ele in self.goals['opt_sol'].answ])
            
    def verify_feasibility(self, SEF):
        if not super().verify_feasibility(SEF):
            return False
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            for ele in g.answ:
                if ele in self.I.forced_out:
                    return SEF.feasibility_NO(g, f"L'oggetto `{ele}` da tè inserito nella lista `{g.alias}` è tra quelli proibiti. Gli oggetti proibiti per la Richiesta {str(SEF.task_number)}, sono {self.I.forced_out}.")
            for ele in self.I.forced_in:
                if ele not in g.answ:
                    return SEF.feasibility_NO(g, f"Nella lista `{g.alias}` hai dimenticato di inserire l'oggetto `{ele}` che invece è forzato. Gli oggetti forzati per la Richiesta {str(SEF.task_number)} sono {self.I.forced_in}.")
            if self.sum_costs > self.I.Knapsack_Capacity:
                return SEF.feasibility_NO(g, f"La tua soluzione in `{g.alias}` ha costo {self.sum_costs} > Knapsack_Capacity e quindi NON è ammissibile in quanto fora il budget per la Richiesta {str(SEF.task_number)}. La soluzione da tè inserita ricomprende il sottoinsieme di oggetti `{g.alias}`= {g.answ}.")
            SEF.feasibility_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale", f"resta da stabilire l'ottimalità di `{g.alias}`")
        return True
                
    def verify_consistency(self, SEF):
        if not super().verify_consistency(SEF):
            return False
        if 'opt_val' in self.goals and 'opt_sol' in self.goals:
            g_val = self.goals['opt_val']; g_sol = self.goals['opt_sol'];
            if self.sum_vals != g_val.answ:
                return SEF.consistency_NO(['opt_val','opt_sol'], f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {self.sum_vals}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            SEF.consistency_OK(['opt_val','opt_sol'], f"{g_val.alias}={g_val.answ} = somma dei valori sugli oggetti in `{g_sol.alias}`.", "")
        return True
      
