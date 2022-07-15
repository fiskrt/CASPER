from scheduler.server import build_servers
from scheduler.task import TaskBatch
from scheduler.constants import REGION_LOCATIONS, REGION_NAMES
from scheduler.parser import parse_arguments
from scheduler.region import Region
from scheduler.plot import Plot
from scheduler.lp_sched import schedule
import sys
import random


def main():
    """
    Init the servers. Generate some fake workload.
    Schedule and run the workload. Get the latency
    and carbon footprint summary. Report it.
    """
    random.seed(1234)
    conf = parse_arguments(sys.argv[1:])

    servers = build_servers()
    regions = [Region(name, location) for name, location in zip(REGION_NAMES, REGION_LOCATIONS)]
    plot = Plot(conf)
    id = 0

    for dt in range(conf.timesteps):
        for _ in range(0, conf.tasks_per_timestep):
            # get list of servers for each task batch where the
            # scheduler thinks it is best to place each batch
            for i in range(len(regions)):
                task_batch = TaskBatch(f"Task {id}", 1, 1, regions[i])
                schedule(plot, task_batch, servers, dt, conf.algorithm)
                id += 1

            for s in servers:
                s.step()

    plot.plot()


if __name__ == "__main__":
    main()
