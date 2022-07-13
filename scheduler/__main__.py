from scheduler.server import build_servers
from scheduler.task import build_tasks
from scheduler.util import plot
from scheduler.scheduler import Scheduler
from scheduler.constants import TIMESTEPS, TASK_PER_TIMESTEP
from scheduler.parser import parse_arguments
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
    tasks = []
    scheduler = Scheduler(servers, scheduler=conf.algorithm)
    mean_latencies = []
    mean_carbon_intensity = []

    for dt in range(TIMESTEPS):
        # reset server utilization
        # assumption:

        for _ in range(0, TASK_PER_TIMESTEP):
            task_batch = build_tasks()
            tasks.extend(task_batch)

            # get list of servers for each task batch where the
            # scheduler thinks it is best to place each batch
            data = scheduler.schedule(tasks, dt)

            # remove any task batch that has a load of 0
            for task in tasks:
                task.lifetime -= 1

            tasks = [task for task in tasks if task.load != 0 and task.lifetime > 0]

            # extract information used for plotting
            mean_latencies.append(data["latency"])
            mean_carbon_intensity.append(data["carbon_intensity"])

    plot(mean_latencies, mean_carbon_intensity)


if __name__ == "__main__":
    main()
