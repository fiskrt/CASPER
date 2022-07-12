import pytest
import pandas as pd

from scheduler.util import load
from scheduler.region import Region
from scheduler.server import Server
from scheduler.constants import REGION_NAMES, LOCATIONS


@pytest.fixture
def df_carbon_intensity():
    return pd.read_csv("data/carbon_intensity_avg.csv")


@pytest.fixture
def servers_infty():
    servers = []
    df_all = pd.read_csv("data/carbon_intensity_avg.csv")
    for name, location in zip(df_all.columns, LOCATIONS):
        df = pd.DataFrame(data={"carbon_intensity_avg": df_all[name]})
        r = Region(name, location)
        s = Server(999999, r, df)
        servers.append(s)

    return servers
