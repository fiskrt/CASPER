from server import Server
from task import TaskBatch
from util import load, print_items
import random

FILENAMES = ["US-CAL-CISO", "US-MIDA-PJM", "US-MIDW-MISO", "US-TEX-ERCO"]
TIME_STEPS = 365 * 24


def main():
    """
    Init the servers. Generate some fake workload.
    Schedule and run the workload. Get the latency
    and carbon footprint summary. Report it.
    """
    random.seed(1234)
    servers = generate_servers()

    for i in range(TIME_STEPS):
        tasks = generate_tasks()

        print_items(tasks)
        break


def generate_servers():
    servers = []
    for filename in FILENAMES:
        df = load(f"../../electricity_map/{filename}.csv", False)
        s = Server(5, filename, df)
        servers.append(s)

    return servers


def generate_tasks():
    return [TaskBatch(f"Task {i}", 0, 10, name) for i, name in enumerate(FILENAMES)]


if __name__ == "__main__":
    main()
