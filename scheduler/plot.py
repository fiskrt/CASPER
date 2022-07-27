import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scheduler.constants import REGION_NAMES


class Plot:
    def __init__(self, conf) -> None:
        self.conf = conf
        self.columns = [
            "timestep",
            "interval",
            "total_requests",
            *[f"{name}_requests_from" for name in REGION_NAMES],
            *[f"{name}_requests_to" for name in REGION_NAMES],
            *[f"{name}_carbon_intensity" for name in REGION_NAMES],
            "total_carbon_emissions",
            *[f"{name}_carbon_emissions" for name in REGION_NAMES],
            "mean_latency",
            *[f"{name}_latency" for name in REGION_NAMES],
            "total_dropped_requests",
            *[f"{name}_dropped_requests" for name in REGION_NAMES],
            "total_utilization",
            *[f"{name}_utilization" for name in REGION_NAMES],
            "total_servers",
            *[f"{name}_servers" for name in REGION_NAMES],
        ]
        self.data = []

    def add(
        self, server_manager, latency, carbon_intensity, requests_per_region, dropped_requests_per_region, t, interval
    ):
        total_requests_to_region = np.sum(requests_per_region, axis=0)
        total_requests_from_region = np.sum(requests_per_region, axis=1)

        assert sum(total_requests_from_region) == sum(total_requests_to_region)

        mask = total_requests_to_region != 0

        carbon_emissions = total_requests_to_region * np.array(carbon_intensity)

        percentage = requests_per_region / (total_requests_to_region + (total_requests_to_region == 0))
        latencies = np.sum(percentage * latency, axis=0)

        capacities = server_manager.capacity_per_region()
        utilization_per_region = total_requests_to_region / (capacities + (capacities == 0))

        servers_per_region = server_manager.servers_per_region()

        mean_latency = np.mean(latencies[mask])
        total_carbon_emissions = np.sum(carbon_emissions[mask])
        total_requests = np.sum(total_requests_to_region)
        total_dropped_requests = np.sum(dropped_requests_per_region)
        total_utilization = np.mean(total_requests / np.sum(capacities + (capacities == 0)))
        total_servers = np.sum(servers_per_region)

        frame = (
            t,
            interval,
            total_requests,
            *total_requests_from_region,
            *total_requests_to_region,
            *carbon_intensity,
            total_carbon_emissions,
            *carbon_emissions,
            mean_latency,
            *latencies,
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

    def plot(self, df=None):
        if df is None:
            df = self.build_df()
        df = df.groupby("timestep")
        fig = plt.figure(figsize=(14, 9))
        fig.tight_layout()
        fig.suptitle(
            [
                "latency:",
                self.conf.latency,
                "max_servers:",
                self.conf.max_servers,
                "server_capacity:",
                self.conf.server_capacity,
            ]
        )
        dfs = [
            df["total_requests"].sum(),
            df[[f"{name}_requests_from" for name in REGION_NAMES]].sum(),
            df[[f"{name}_requests_to" for name in REGION_NAMES]].sum(),
            df[[f"{name}_carbon_intensity" for name in REGION_NAMES]].mean(),
            df["total_carbon_emissions"].sum(),
            df[[f"{name}_carbon_emissions" for name in REGION_NAMES]].sum(),
            df["mean_latency"].mean(),
            df[[f"{name}_latency" for name in REGION_NAMES]].mean(),
            df["total_dropped_requests"].sum(),
            df[[f"{name}_dropped_requests" for name in REGION_NAMES]].sum(),
            df["total_utilization"].mean(),
            df[[f"{name}_utilization" for name in REGION_NAMES]].mean(),
            df["total_servers"].mean(),
            df[[f"{name}_servers" for name in REGION_NAMES]].mean(),
        ]
        titles = [
            "total_requests",
            "requests_from",
            "requests_to",
            "carbon_intensity",
            "total_carbon_emissions",
            "carbon_emissions",
            "mean_latency",
            "latency",
            "total_dropped",
            "dropped",
            "mean_utilization",
            "utilization",
            "total_servers",
            "servers",
        ]
        i = 0
        for df in dfs:
            ax = plt.subplot(5, 3, i + 1)
            if len(df.shape) > 1 and df.shape[1] > 0:
                ax = df.plot(ax=ax)
            else:
                ax = df.plot(ax=ax, color="black")
            ax.set_xlabel("")
            ax.set_title(titles[i])
            ax.legend().remove()
            ax.set_xticks([])
            i += 1

        fig.legend(["Mean/Total"] + REGION_NAMES, loc="upper center", bbox_to_anchor=(0.5, 0.07), ncol=3)
        plt.show()
