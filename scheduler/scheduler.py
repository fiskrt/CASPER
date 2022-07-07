from typing import List
import numpy as np


class Scheduler:
    def __init__(self, servers, scheduler="latency_greedy") -> None:
        self.servers = servers
        self.alg = self.__get_scheduler(scheduler)

    def __get_scheduler(self, name):
        if name == "latency_greedy":
            return self.__latency_greedy
        elif name == "carbon_greedy":
            return self.__carbon_greedy
        elif name == "carbon_aware":
            return self.__carbon_aware1

    def __latency_greedy(self, tasks, dt):
        """
        Schedule tasks such that the lowest latency
        servers are filled first.
        """
        scheduled_servers = []
        for t in tasks:
            latencies = [t.region.latency(s.region) for s in self.servers]
            indices = np.argsort(latencies)
            data = {
                "task": t,
                "indices": indices,
                "latencies": latencies,
                "carbon_intensities": [self.servers[i].carbon_intensity[dt] for i in indices],
            }
            scheduled_servers.append(data)
        return scheduled_servers

    def __carbon_greedy(self, tasks, dt):
        """
        Schedule tasks such that the lowest latency
        servers are filled first.
        """
        scheduled_servers = []
        for t in tasks:
            carbon_intensities = [s.carbon_intensity[dt] for s in self.servers]
            indices = np.argsort(carbon_intensities)
            data = {
                "task": t,
                "indices": indices,
                "latencies": [t.region.latency(self.servers[i].region) for i in indices],
                "carbon_intensities": carbon_intensities,
            }
            scheduled_servers.append(data)
        return scheduled_servers

    def __carbon_aware1(self, tasks, dt):
        """
        Schedule tasks such that the lowest latency
        servers are filled first.
        """
        scheduled_servers = []
        max_latency = 20

        for t in tasks:
            above = [s.carbon_intensity[dt] for s in self.servers if t.region.latency(s.region) > max_latency]
            below = [s.carbon_intensity[dt] for s in self.servers if t.region.latency(s.region) <= max_latency]

            indices = np.concatenate((np.argsort(below), np.argsort(above)), axis=None)

            data = {
                "task": t,
                "indices": indices,
                "latencies": [t.region.latency(self.servers[i].region) for i in indices],
                "carbon_intensities": above + below,
            }
            scheduled_servers.append(data)
        return scheduled_servers

    def __carbon_aware(self, tasks, ts):
        """
        Input: tasks that want to be run.
        Output: What server each task should be run on
        satisfying the max latency constraint while having the lowest
        carbon footprint.

        List where each entry is (taskbatch, server, latency)

        Does not split taskbatches, i.e if a server does not
        have enough capacity, we just move on to the next
        server.
        """
        max_latency = 50
        servs_by_carbon = sorted(self.servers, key=lambda x: x.carbon_intensity.iloc[ts])
        sched = []
        for t in tasks:
            for s in servs_by_carbon:
                lat = t.region.latency(s.region)
                if lat > max_latency:
                    continue
                if s.update_utilization(t.load):
                    sched.append((t, s, lat))
                    break
                else:
                    continue
            else:
                print("No availible servers")

        return sched

    def schedule(self, tasks, dt):
        scheduled_servers_for_each_task = self.alg(tasks, dt)
        data = {"latency": [], "carbon_intensity": []}

        for scheduled_item in scheduled_servers_for_each_task:
            task = scheduled_item["task"]
            indices = scheduled_item["indices"]
            latencies = scheduled_item["latencies"]
            carbon_intensities = scheduled_item["carbon_intensities"]

            for j in range(len(indices)):
                index = indices[j]
                if self.servers[index].update_utilization(task.load):
                    latency = latencies[index] * task.load
                    carbon_intesity = carbon_intensities[index] * task.load
                    data["latency"].append(latency)
                    data["carbon_intensity"].append(carbon_intesity)
                    task.reduce_load(task.load)
                    break
                else:
                    # send partial batch and update load
                    partial_load = self.servers[index].get_utilization_left()
                    if partial_load == 0:
                        continue
                    task.reduce_load(partial_load)
                    self.servers[index].update_utilization(partial_load)

                    latency = latencies[index] * partial_load
                    carbon_intesity = carbon_intensities[index] * partial_load
                    data["latency"].append(latency)
                    data["carbon_intensity"].append(carbon_intesity)

        data["latency"] = np.mean(data["latency"])
        data["carbon_intensity"] = np.mean(data["carbon_intensity"])
        return data
