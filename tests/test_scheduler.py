import pytest

from scheduler.scheduler import Scheduler
from scheduler.task import TaskBatch
from scheduler.region import Region
from scheduler.constants import REGION_NAMES, REGION_LOCATIONS
from scheduler.plot import Plot
from scheduler.parser import parse_arguments
from scheduler.lp_sched import schedule

import numpy as np


def test_carbon_greedy_with_one_scheduler_0_24(df_carbon_intensity, servers_infty):
    conf = parse_arguments(["-a", "carbon_greedy"])
    region = Region(REGION_NAMES[0], REGION_LOCATIONS[0])
    plot = Plot(conf)

    for dt in range(conf.timesteps):
        task_batch = TaskBatch("Task 1", 1, 1, region)
        schedule(plot, task_batch, servers_infty, dt, conf.algorithm)
        emissions = np.mean(list(map(lambda x: x["carbon_emissions"], plot.get(dt))))
        assert emissions == df_carbon_intensity[0:24].iloc[dt].min()


def test_latency_greedy_with_one_scheduler_0_24(servers_infty):
    conf = parse_arguments(["-a", "latency_greedy"])
    region = Region(REGION_NAMES[0], REGION_LOCATIONS[0])
    plot = Plot(conf)

    for dt in range(conf.timesteps):
        task_batch = TaskBatch("Task 1", 1, 1, region)
        schedule(plot, task_batch, servers_infty, dt, conf.algorithm)
        emissions = np.mean(list(map(lambda x: x["latency"], plot.get(dt))))
        assert emissions == 0
