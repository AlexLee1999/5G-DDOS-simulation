import cvxpy as cp
from mpo import *
from const import *


def convex_solve(mpo):
    res_lst = []
    x_lst = []
    for i in range(len(mpo.asp_response)):
        if mpo.asp_response[i] == ['z', 'z', 'z', 'z', 'z']:
            break
        sqrt_c = 0
        linear_c = 0
        for j in range(len(mpo.asp_response[i])):
            if mpo.asp_response[i][j] == 'e1':
                sqrt_c += mpo.asp_lst[j].sqrt_coff_1
                linear_c += mpo.asp_lst[j].coff_1
            elif mpo.asp_response[i][j] == 'e2':
                sqrt_c += mpo.asp_lst[j].sqrt_coff_2
                linear_c += mpo.asp_lst[j].coff_2
            elif mpo.asp_response[i][j] == 'e3':
                sqrt_c += mpo.asp_lst[j].sqrt_coff_3
                linear_c += mpo.asp_lst[j].coff_3
            elif mpo.asp_response[i][j] == 'q':
                linear_c += mpo.asp_lst[j].queue_coff
        res, x = convex_opt(sqrt_c, linear_c, mpo.bound[i] - EPSILON, mpo.bound[i + 1] - EPSILON)
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
    obj = cp.Maximize(cp.sqrt(x) * sqrt_c + x * linear_c - (0.01 *
                      cp.power(sqrt_c * cp.inv_pos(cp.sqrt(x)) + linear_c, 2)))
    constraint = [lower <= x, x <= upper]
    prob = cp.Problem(obj, constraint)
    try:
        res = prob.solve(solver=CVX_SOLVER)
    except cp.error.SolverError:
        try:
            res = prob.solve(solver=ALTER_CVX_SOLVER)
        except:
            raise ArithmeticError("Solver Error")

    # if prob.status != OPTIMAL:
    #     print(prob.status)
    #     raise ArithmeticError("Not Optimal")
    return res, x.value[0]
