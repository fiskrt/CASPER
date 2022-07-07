class TaskBatch:
    def __init__(self, name, load, region):
        self.name = name
        self.load = load
        self.start_time = 0
        self.ex_time = 0
        self.region = region

    def __repr__(self) -> str:
        return f"{self.name:<14} load: {self.load:<6} start: {self.start_time:<6} end: {self.start_time + self.ex_time:<6} region: {self.region:<15}"
