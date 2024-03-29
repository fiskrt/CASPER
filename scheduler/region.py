from fnmatch import translate
import os
import pandas as pd
from scheduler.util import load_carbon_intensity, load_request_rate
from scheduler.constants import REGION_LOCATIONS, REGION_OFFSETS
from scheduler.util import get_regions



class Region:
    def __init__(self, name, location, carbon_intensity, requests_per_hour) -> None:
        self.name = name
        self.location = location
        self.requests_per_hour = requests_per_hour
        self.carbon_intensity = carbon_intensity
        self.latency_df = pd.read_csv("api/cloudping/latency.csv")

    def get_requests_per_hour(self, t):
        return self.requests_per_hour.iloc[t]

    # def latency(self, other):
    #     (x1, y1) = self.location
    #     (x2, y2) = other.location
    #     return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def name_translator(self, name):
        name_translator_dic = { "US-CAL-CISO" : "US-West-N.-California",
                                "US-MIDA-PJM" : "US-East-Ohio",
                                "US-MIDW-MISO" : "US-East-N.-Virginia",
                                "US-TEX-ERCO" : "US-East-N.-Virginia",
                                "DE" : "EU-Frankfurt",
                                "FR" : "EU-Paris",
                                "IE" : "EU-Ireland",
                                "IT-NO" : "EU-Milan",
                                "SE" : "EU-Stockholm" }
        return name_translator_dic[name]

    def latency(self, other):
        '''
        Gathered as listed in the readme.
        Cali = Cali
        Mid atlantic = Ohio
        Mid west = Virginia
        Texas = ????????
        '''
        #path = os.join.path("api", )

        i = self.name_translator(self.name)
        j = self.name_translator(other.name)

        df = self.latency_df
        print(df)
        i_index = df.columns.get_loc(i)
        j_index = df.columns.get_loc(j)
        return df.iloc[i_index, j_index]

    def __repr__(self) -> str:
        return self.name

    def __format__(self, __format_spec: str) -> str:
        return format(self.name, __format_spec)


def load_regions(conf):
    date = conf.start_date
    regions = []
    d = "api"
    kind = ""
    if conf.region_kind == "original":
        kind = "original"
    elif conf.region_kind == "europe":
        kind = "europe"
    elif conf.region_kind == "north_america":
        kind = "north_america"
    d = os.path.join(d, kind)

    for name in get_regions(conf):
        file = f"{name}.csv"
        path = os.path.join(d, file)
        location = REGION_LOCATIONS[name]
        # hardcoded offsets
        offset = REGION_OFFSETS[name]

        request_path = "api/requests.csv"
        requests_per_hour = load_request_rate(request_path, offset, conf, date)
        carbon_intensity = load_carbon_intensity(path, offset, conf, date)
        region = Region(name, location, carbon_intensity, requests_per_hour)
        regions.append(region)
    return regions
