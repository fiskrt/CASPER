import pytest

from scheduler.scheduler import Scheduler
from scheduler.task import TaskBatch
from scheduler.region import Region
from scheduler.constants import REGION_NAMES, REGION_LOCATIONS
from scheduler.plot import Plot
from scheduler.parser import parse_arguments


def test_carbon_greedy_with_one_scheduler_0_24(df_carbon_intensity, servers_infty):
    conf = parse_arguments(["-a", "carbon_greedy"])
    region = Region(REGION_NAMES[0], REGION_LOCATIONS[0])
    scheduler = Scheduler(servers_infty, region, scheduler=conf.algorithm)
    plot = Plot(conf)

    for dt in range(conf.timesteps):
        task = TaskBatch("Task 1", 1, 1, region)
        d = scheduler.schedule(plot, task, dt)
        assert d["carbon_intensity"][dt] == df_carbon_intensity[0:24].iloc[dt].min()
