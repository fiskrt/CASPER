class TaskBatch:
    def __init__(self, name, start_time, ex_time, region):
        self.name = name
        self.load = 0
        self.start_time = start_time
        self.ex_time = ex_time
        self.region = region

    def __repr__(self) -> str:
        return f"{self.name:<10} load: {self.load:<6} start: {self.start_time:<6} end: {self.start_time + self.ex_time:<6} region: {self.region:<15}"
