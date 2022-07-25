# Carbon Aware Scheduler and ProvisionER (CASPER)

Using predictions of request during the next hour we calculate how the servers should be placed to handle
the requests while minimizing carbon and satsifying latency constraint.

Once servers are placed, the scheduler distributes the request between the regions such that carbon is minimized.


## Installation
Install all required packages specified in requirements.txt
```
pip install -r requirements.py
```

## Usage
To run the scheduler, make sure the working directory is the root folder of the repository and run the following

```
python -m scheduler --help
```

```
usage: __main__.py [-h] [-a {latency_greedy,carbon_greedy,carbon_aware}]
                   [-dt TIMESTEPS] [-ds TASKS_PER_TIMESTEP]

optional arguments:
  -h, --help            show this help message and exit
  -a {latency_greedy,carbon_greedy,carbon_aware}, --algorithm {latency_greedy,carbon_greedy,carbon_aware}
                        The scheduling algorithm to use
  -dt TIMESTEPS, --timesteps TIMESTEPS
                        The total number of hours
  -ds TASKS_PER_TIMESTEP, --tasks-per-timestep TASKS_PER_TIMESTEP
                        The number of times per timestep that task batches are
                        generated
```

## Testing ![Test](https://github.com/Zonotora/umass/workflows/Test/badge.svg?branch=main&event=push)

To run all the tests `pytest` is required
```
pip install pytest
```

Run the following command in the root folder

```
pytest -v
```