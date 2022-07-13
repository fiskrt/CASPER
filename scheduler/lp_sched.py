from scipy.optimize import linprog
import numpy as np
import math


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
    mu = 1.2 

    #carb_intensity = np.arange(1, n_servers+1) 
    #latency = np.arange(1, n_servers+1) 
    carb_intensity = [2,3,5,5,5]
    latency = np.asarray([5,5,5,3,1])
    obj_coef = np.concatenate([carb_intensity, mu*latency])
    num_reqs = 100
    n_servers = len(latency) 

    # Each server can take [0,inf] tasks
    bnd = [(0, float("inf"))]*(2*n_servers)

    # Capacity constraint. Server i has capacity capacities[i] 
    cap = 50
    capacities = [cap]*n_servers 
    lhs_ineq = np.concatenate([np.identity(n_servers), np.zeros((n_servers,n_servers))], axis=1)
    rhs_ineq = capacities

    # Make sure all tasks are scheduled somewhere.
    lhs_eq = np.zeros((n_servers, 2*n_servers))
    lhs_eq[0, :n_servers] = 1
    rhs_eq = [num_reqs] + [0]*(n_servers-1) + [0]*n_servers

    lhs_eq2 = np.concatenate([np.eye(n_servers), -np.eye(n_servers)], axis=1)
    lhs_eq = np.concatenate([lhs_eq, lhs_eq2])

    opt = linprog(c=obj_coef, A_ub=lhs_ineq, b_ub=rhs_ineq,
                A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
                method="revised simplex")
    print(opt.message)
    print(f'Objective value: {opt.fun}')
    return [math.ceil(x) for x in opt.x][:n_servers]

a = sched_carb_latency()
print(a)