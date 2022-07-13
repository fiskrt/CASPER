import numpy as np
from scheduler.region import Region
from scheduler.constants import TASK_LIFETIME_MEAN, TASK_LIFETIME_STD, REGION_NAMES, REGION_LOCATIONS


class TaskBatch:
    def __init__(self, name, load, lifetime, region):
        self.name = name
        self.load = load
        self.region = region
        self.lifetime = lifetime

    def __repr__(self) -> str:
        return f"{self.name:<14} load: {self.load:<6} lifetime: {self.lifetime} region: {self.region:<15}"

    def reduce_load(self, load):
        # this should not go beneath 0
        self.load -= load
        assert self.load >= 0


def build_tasks():
    load = 1

    return [
        TaskBatch(
            f"TaskBatch {i}",
            load,
            int(np.random.normal(TASK_LIFETIME_MEAN, TASK_LIFETIME_STD)),
            Region(name, location),
        )
        for i, (name, location) in enumerate(zip(REGION_NAMES, REGION_LOCATIONS))
    ]
