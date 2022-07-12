import pandas as pd
import pytest

from scheduler.scheduler import Scheduler
from scheduler.task import TaskBatch
from scheduler.region import Region
from scheduler.constants import REGION_NAMES, LOCATIONS


def test_carbon_greedy_day_0_24(df_carbon_intensity_0_24, servers_0_24):
    max_time = 24
    scheduler = Scheduler(servers_0_24)
    region = Region(REGION_NAMES[0], LOCATIONS[0])

    for dt in range(max_time):
        task = TaskBatch("Task 1", 1, 1, region)
        d = scheduler.schedule([task], dt)
        assert d["carbon_intensity"] == df_carbon_intensity_0_24.iloc[dt].min()
