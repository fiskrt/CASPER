class Server:
    """
    An artificial server with a carbon trace,
    latency and capacity.
    """

    def __init__(self, capacity, region, carbon_data):
        """ """
        self.capacity = capacity
        self.region = region
        self.carbon_data = carbon_data
        self.carbon_intensity = carbon_data["carbon_intensity_avg"]

    def __repr__(self) -> str:
        return f"{self.region:<15} capcity: {self.capacity:<6}"
