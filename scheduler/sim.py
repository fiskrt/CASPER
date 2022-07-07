from server import Server
from task import TaskBatch
from util import load, print_items
from scheduler import Scheduler
from region import Region
import random

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

    for i in range(TIME_STEPS):
        tasks = generate_tasks()
        scheduler.schedule(tasks)

        print_items(tasks)
        break


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


if __name__ == "__main__":
    main()
