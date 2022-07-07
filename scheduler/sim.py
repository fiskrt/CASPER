from server import Server
from task import TaskBatch
from util import load, print_items
from scheduler import Scheduler
from region import Region
import random
import pandas as pd
import matplotlib.pyplot as plt

FILENAMES = ["US-CAL-CISO", "US-MIDA-PJM", "US-MIDW-MISO", "US-TEX-ERCO"]
LOCATIONS = [(-120, 30), (-75, 40), (-80, 40), (-95, 30)]
TIME_STEPS = 1 * 24


def main():
    """
    Init the servers. Generate some fake workload.
    Schedule and run the workload. Get the latency
    and carbon footprint summary. Report it.
    """
    random.seed(1234)
    servers = generate_servers()
    tasks = []
    # scheduler = Scheduler(servers, scheduler="carbon_greedy")
    scheduler = Scheduler(servers, scheduler="carbon_aware")
    # scheduler = Scheduler(servers, scheduler="latency_greedy")
    mean_latencies = []
    mean_carbon_intensity = []

    for dt in range(TIME_STEPS):
        # reset server utilization
        # assumption:
        for s in servers:
            s.reset_utilization()

        # generate a new set of tasks
        task_batch = generate_tasks()
        tasks.extend(task_batch)

        # get list of servers for each task batch where the
        # scheduler thinks it is best to place each batch
        data = scheduler.schedule(tasks, dt)

        # remove any task batch that has a load of 0
        tasks = [task for task in tasks if task.load != 0]

        # extract information used for plotting
        mean_latencies.append(data["latency"])
        mean_carbon_intensity.append(data["carbon_intensity"])
    plot(mean_latencies, mean_carbon_intensity)


def generate_servers():
    servers = []
    for filename, location in zip(FILENAMES, LOCATIONS):
        df = load(f"../electricity_map/{filename}.csv", False)
        r = Region(filename, location)
        s = Server(10, r, df)
        servers.append(s)

    return servers


def generate_tasks():
    # return [
    #     TaskBatch(f"TaskBatch {i}", random.randint(0, 40), Region(name, location))
    #     for i, (name, location) in enumerate(zip(FILENAMES, LOCATIONS))
    # ]
    return [
        TaskBatch(f"TaskBatch {i}", 1, Region(name, location))
        for i, (name, location) in enumerate(zip(FILENAMES, LOCATIONS))
    ]


def plot(mean_latencies, mean_carbon_intensity):
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.plot(mean_latencies, label="Latency")
    plt.subplot(1, 2, 2)
    plt.plot(mean_carbon_intensity, label="Carbon")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
