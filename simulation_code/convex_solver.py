from math import sqrt
from typing import Optional
import cvxpy as cp
from cvxpy.settings import CONVEX, OPTIMAL
from mpo import *
from const import *
import pickle

def convex_solve(mpo):
    res_lst = []
    x_lst = []
    for i in range(len(mpo.asp_response)):
        if mpo.asp_response[i] == ['z', 'z', 'z', 'z', 'z']:
            break
        sqrt_c = 0
        linear_c = 0
        for j in range(len(mpo.asp_response[i])):
            if mpo.asp_response[i][j] == 'e':
                sqrt_c += mpo.asp_lst[j].sqrt_coff
                linear_c += mpo.asp_lst[j].coff
            elif mpo.asp_response[i][j] == 'q':
                linear_c += mpo.asp_lst[j].queue_coff
        res, x = convex_opt(sqrt_c, linear_c, mpo.bound[i], mpo.bound[i+1])
        res_lst.append(res)
        x_lst.append(x)
    max_res = 0
    max_phi = 0
    for i in range(len(res_lst)):
        if res_lst[i] > max_res:
            max_res = res_lst[i]
            max_phi = x_lst[i]
    return max_res, max_phi

    
def convex_opt(sq, li, low, up):
    sqrt_c = cp.Parameter(1)
    linear_c = cp.Parameter(1)
    upper = cp.Parameter(1)
    lower = cp.Parameter(1)
    x = cp.Variable(1)
    sqrt_c = sq
    linear_c = li
    upper = up
    lower = low
    obj = cp.Maximize(cp.sqrt(x) * sqrt_c + x * linear_c - (0.01 * cp.power(sqrt_c *cp.inv_pos(cp.sqrt(x)) + linear_c, 2)))
    constraint = [lower <= x, x <= upper]
    prob = cp.Problem(obj, constraint)
    try:
        res = prob.solve(solver=CVX_SLOVER)
    except cp.error.SolverError:
        raise ArithmeticError("Solver Error")

    if prob.status != OPTIMAL:
        raise ArithmeticError("Not Optimal")
    return res, x.value[0]