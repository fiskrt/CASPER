class RequestBatch:
    def __init__(self, name, load, lifetime, region):
        self.name = name
        self.load = load
        self.region = region
        self.lifetime = lifetime

    def __repr__(self) -> str:
        return f"{self.name:<14} load: {self.load:<6} lifetime: {self.lifetime} region: {self.region:<15}"
