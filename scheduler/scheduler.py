from typing import List
import sys


class Scheduler:
    """At what level should the scheduler be at?"""

    def __init__(self, servers, scheduler="latency_greedy") -> None:
        self.servers = servers
        self.alg = self.__get_scheduler(scheduler)

    def __get_scheduler(self, name):
        if name == "latency_greedy":
            return self.__latency_greedy
        elif name == "carbon_aware":
            return self.__carbon_aware

    def __latency_greedy(self, tasks):
        """
        Schedule tasks such that the lowest latency
        servers are filled first.
        """
        return self.compute_latencies(tasks)

    def __carbon_aware(self, tasks):
        """
        Input: tasks that want to be run.
        Output: What server each task should be run on
        with a trade-off between carbon and latency.
        """
        pass

    def schedule(self, tasks):
        return self.alg(tasks)

    def compute_latencies(self, tasks) -> List:
        latencies = []
        for t in tasks:
            min_latency = sys.maxsize
            index = 0
            for i, s in enumerate(self.servers):
                latency = t.region.latency(s.region)
                if latency < min_latency:
                    min_latency = latency
                    index = i
            latencies.append((min_latency, self.servers[index]))
        return latencies
