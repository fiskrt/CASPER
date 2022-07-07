from server import Server
from task import TaskBatch
from util import load, print_items
from scheduler import Scheduler
from region import Region
import random
import pandas as pd
import matplotlib.pyplot as plt

FILENAMES = ["US-CAL-CISO", "US-MIDA-PJM", "US-MIDW-MISO", "US-TEX-ERCO"]
LOCATIONS = [(0, 0), (10, 10), (-10, 0), (0, 10)]
TIME_STEPS = 365 * 24


def main():
    """
    Init the servers. Generate some fake workload.
    Schedule and run the workload. Get the latency
    and carbon footprint summary. Report it.
    """
    random.seed(1234)
    servers = generate_servers()
    scheduler = Scheduler(servers)
    mean_latencies = []
    mean_carbon_intensity = []

    for dt in range(TIME_STEPS):
        tasks = generate_tasks()
        latencies = scheduler.schedule(tasks)
        servers = list(map(lambda x: x[1], latencies))
        d = {
            "task_batch": list(map(lambda x: x.name, tasks)),
            "task_region": list(map(lambda x: x.region.name, tasks)),
            "latency": list(map(lambda x: x[0], latencies)),
            "server_region": list(map(lambda x: x.region.name, servers)),
            "server_carbon_intensity": list(map(lambda x: x.carbon_intensity[dt], servers)),
        }
        df = pd.DataFrame(data=d)
        latency = df["latency"].mean()
        carbon_intensity = df["server_carbon_intensity"].mean()
        mean_latencies.append(latency)
        mean_carbon_intensity.append(carbon_intensity)
    plot(mean_latencies, mean_carbon_intensity)


def generate_servers():
    servers = []
    for filename, location in zip(FILENAMES, LOCATIONS):
        df = load(f"../../electricity_map/{filename}.csv", False)
        r = Region(filename, location)
        s = Server(5, r, df)
        servers.append(s)

    return servers


def generate_tasks():
    return [
        TaskBatch(f"TaskBatch {i}", random.randint(0, 40), Region(name, location))
        for i, (name, location) in enumerate(zip(FILENAMES, LOCATIONS))
    ]


def plot(mean_latencies, mean_carbon_intensity):
    plt.plot(mean_latencies, label="Latency")
    plt.plot(mean_carbon_intensity, label="Carbon intensity")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
