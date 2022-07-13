import pytest

from scheduler.scheduler import Scheduler
from scheduler.task import TaskBatch
from scheduler.region import Region
from scheduler.constants import REGION_NAMES, REGION_LOCATIONS


def test_carbon_greedy_with_one_scheduler_0_24(df_carbon_intensity, servers_infty):
    max_time = 24
    region = Region(REGION_NAMES[0], REGION_LOCATIONS[0])
    scheduler = Scheduler(servers_infty, region, scheduler="carbon_greedy")

    for dt in range(max_time):
        task = TaskBatch("Task 1", 1, 1, region)
        d = scheduler.schedule(task, dt)
        assert d["carbon_intensity"] == df_carbon_intensity[0:24].iloc[dt].min()
