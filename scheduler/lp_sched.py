from scipy.optimize import linprog
import numpy as np


def sched_only_carbon():
    """
        Returns: List with number of request that are scheduled
        at respective server. Ex: 5 requests to server 1, 10 to 
        server 2 and none to server 3 would be [5,10,0]
    """
    n_servers = 10
    carb_intensity = list(range(1,n_servers+1))
    capacities = [50]*n_servers
    num_reqs = 100


    obj = carb_intensity
    bnd = [(0, float("inf"))]*n_servers
    lhs_ineq = np.identity(n_servers)
    rhs_ineq = capacities


    lhs_eq = np.zeros((n_servers, n_servers))
    lhs_eq[0] = 1
    rhs_eq = [num_reqs] + [0]*(n_servers-1)

    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
                A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
                method="revised simplex")

    return [math.ceil(x) for x in opt.x]

def sched_carb_latency():
    """
        Considers carbon, latency and capacity.

        mu is the unit dependent parameter that
        trade-offs carbon and latency. 
    """
    mu = 0.5 


    n_servers = 10
    carb_intensity = list(range(1,n_servers+1))
    latency = list(range(1,n_servers+1))
    c = carb_intensity + latency
    capacities = [50]*n_servers
    num_reqs = 100


    obj = carb_intensity
    bnd = [(0, float("inf"))]*n_servers
    lhs_ineq = np.identity(n_servers)
    rhs_ineq = capacities


    lhs_eq = np.zeros((n_servers, n_servers))
    lhs_eq[0] = 1
    rhs_eq = [num_reqs] + [0]*(n_servers-1)

    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
                A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
                method="revised simplex")

    return [math.ceil(x) for x in opt.x]
