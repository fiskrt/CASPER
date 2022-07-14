from scipy.optimize import linprog
import numpy as np
import math


def sched_only_carbon():
    """
        Returns: List with number of request that are scheduled
        at respective server. Ex: 5 requests to server 1, 10 to 
        server 2 and none to server 3 would be [5,10,0]
    """
    raise NotImplementedError
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

def schedule(task, t):
    """

    """
    n_tasks = task
    # In some way (api/database) get the servers' carbon,latency, capacity
    carb_intensity = [2,3,5,5,5]
    latency = np.asarray([5,5,5,3,1])
    cap = 20 
    capacities = [cap]*len(latency)
    return sched_carb_latency(n_tasks, carb_intensity, capacities, latency)


def sched_carb_latency(n_tasks, carb_intensity, capacities, latency, mu=1):
    """
        Takes a number of fungible tasks from a location, and 
        schedules them on servers 1,...,n while considering
        the carbon intensity I_i, latency tau_i and capacity c_i
        of each server i.


        Input: 
        The number of tasks to be scheduled.

        mu is the unit dependent parameter that
        trade-offs carbon and latency. 
    """
    n_servers = len(latency) 

    # The objective function's coefficients
    obj_coef = np.concatenate([carb_intensity, mu*latency])

    # Each server can take [0,inf] tasks
    bnd = [(0, float("inf"))]*(2*n_servers)

    # Capacity constraint. Server i has capacity capacities[i] 
    lhs_ineq = np.concatenate([np.identity(n_servers), np.zeros((n_servers,n_servers))], axis=1)
    rhs_ineq = capacities

    # Make sure all tasks are scheduled somewhere.
    lhs_eq = np.zeros((n_servers, 2*n_servers))
    lhs_eq[0, :n_servers] = 1
    rhs_eq = [n_tasks] + [0]*(n_servers-1) + [0]*n_servers

    lhs_eq2 = np.concatenate([np.eye(n_servers), -np.eye(n_servers)], axis=1)
    lhs_eq = np.concatenate([lhs_eq, lhs_eq2])

    opt = linprog(c=obj_coef, A_ub=lhs_ineq, b_ub=rhs_ineq,
                A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
                method="revised simplex")
    if opt.status == 2:
        print('Warning: No server availible!')
    print(opt.message)
    print(f'Objective value: {opt.fun}')
    return [math.ceil(x) for x in opt.x][:n_servers]

a = schedule(100, t=5)
print(a)