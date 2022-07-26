import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scheduler.constants import REGION_NAMES


class Plot:
    def __init__(self, conf) -> None:
        self.conf = conf
        self.columns = [
            "timestep",
            "mean_latency",
            *[f"{name}_latency" for name in REGION_NAMES],
            "mean_carbon_emissions",
            *[f"{name}_carbon_emissions" for name in REGION_NAMES],
            "total_requests",
            *[f"{name}_requests" for name in REGION_NAMES],
            "total_dropped_requests",
            *[f"{name}_dropped_requests" for name in REGION_NAMES],
            "total_utilization",
            *[f"{name}_utilization" for name in REGION_NAMES],
            "total_servers",
            *[f"{name}_servers" for name in REGION_NAMES],
        ]
        self.data = []

    def add(self, server_manager, latency, carbon_intensity, requests_per_region, dropped_requests_per_region, t):
        total_requests_per_region = np.sum(requests_per_region, axis=0)
        mask = total_requests_per_region != 0

        carbon_emissions = total_requests_per_region * np.array(carbon_intensity)

        percentage = requests_per_region / (total_requests_per_region + (total_requests_per_region == 0))
        latencies = np.sum(percentage * latency, axis=0)

        capacities = server_manager.capacity_per_region()
        utilization_per_region = total_requests_per_region / (capacities + (capacities == 0))

        servers_per_region = server_manager.servers_per_region()

        mean_latency = np.mean(latencies[mask])
        mean_carbon_emissions = np.mean(carbon_emissions[mask])
        total_requests = np.sum(total_requests_per_region)
        total_dropped_requests = np.sum(dropped_requests_per_region)
        total_utilization = np.mean(total_requests / np.sum(server_manager.capacity_per_region()))
        total_servers = np.sum(servers_per_region)

        frame = (
            t,
            mean_latency,
            *latencies,
            mean_carbon_emissions,
            *carbon_emissions,
            total_requests,
            *total_requests_per_region,
            total_dropped_requests,
            *dropped_requests_per_region,
            total_utilization,
            *utilization_per_region,
            total_servers,
            *servers_per_region,
        )
        self.data.append(frame)

    def get(self, dt: int):
        return self.data[dt]

    def build_df(self):
        return pd.DataFrame(self.data, columns=self.columns)

    def plot(self):
        df = self.build_df()
        df = df.groupby("timestep")
        fig = plt.figure(figsize=(18, 14))
        fig.tight_layout()
        dfs = [
            df["mean_latency"].mean(),
            df[[f"{name}_latency" for name in REGION_NAMES]].mean(),
            df["mean_carbon_emissions"].mean(),
            df[[f"{name}_carbon_emissions" for name in REGION_NAMES]].mean(),
            df["total_requests"].sum(),
            df[[f"{name}_requests" for name in REGION_NAMES]].sum(),
            df["total_dropped_requests"].sum(),
            df[[f"{name}_dropped_requests" for name in REGION_NAMES]].sum(),
            df["total_utilization"].mean(),
            df[[f"{name}_utilization" for name in REGION_NAMES]].mean(),
            df["total_servers"].mean(),
            df[[f"{name}_servers" for name in REGION_NAMES]].mean(),
        ]
        titles = [
            "latency",
            "latency",
            "carbon_emissions",
            "carbon_emissions",
            "requests",
            "requests",
            "dropped",
            "dropped",
            "utilization",
            "utilization",
            "servers",
            "servers",
        ]
        i = 0
        for df in dfs:
            ax = plt.subplot(3, 4, i + 1)
            ax = df.plot(ax=ax)
            if len(df.shape) > 1 and df.shape[1] > 0:
                ax.legend(REGION_NAMES)
            ax.set_xlabel("Hours (h)")
            ax.set_title(titles[i])
            i += 1
        plt.show()
