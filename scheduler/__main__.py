from scheduler.server import ServerManager
from scheduler.request import RequestBatch
from scheduler.parser import parse_arguments
from scheduler.plot import Plot
from scheduler.util import save_file, ui
from scheduler.milp_sched import schedule_requests, schedule_servers
import sys
import random


def main():
    """
    Init the servers. Generate some fake workload.
    Schedule and run the workload. Get the latency
    and carbon footprint summary. Report it.
    """
    random.seed(1234)
    conf = parse_arguments(sys.argv[1:])

    # if conf.load:
    #     data = load_file(conf.load)
    #     plot = Plot(conf, data=data)
    #     plot.plot()
    #     exit()

    plot = Plot(conf)
    server_manager = ServerManager(conf)

    request_update_interval = 60 // conf.request_update_interval

    for t in range(conf.timesteps + 1):
        move(conf, server_manager, t)
        for _ in range(request_update_interval):
            # get number of requests for timeframe
            # TODO: Change this to dynamic requests
            batches = []
            for region in server_manager.regions:
                rate = region.get_requests_per_hour(t) // request_update_interval
                if conf.rate:
                    rate = conf.rate
                batch = RequestBatch("", rate, region)
                batches.append(batch)

            # call the scheduling algorithm
            latency, carbon_intensity, requests_per_region = schedule_requests(
                conf, batches, server_manager, t, max_latency=conf.latency
            )
            # send requests to servers
            dropped_requests_per_region = server_manager.send(requests_per_region)
            # update_plot(plot, t, latency, carbon_intensity, requests_per_region)
            plot.add(server_manager, latency, carbon_intensity, requests_per_region, dropped_requests_per_region, t)

            # reset server utilization for every server before scheduling requests again
            # we can do this as requests are managed instantaneously for each server
            server_manager.reset()

        if conf.verbose:
            ui(t, requests_per_region, server_manager.servers, server_manager.servers_per_region())

    if conf.save:
        save_file(plot)

    plot.plot()


def move(conf, server_manager, t):
    batches = []
    for region in server_manager.regions:
        rate = region.get_requests_per_hour(t)
        batch = RequestBatch("", rate, region)
        batches.append(batch)

    servers_per_region = schedule_servers(
        conf, batches, server_manager, t, max_latency=conf.latency, max_servers=conf.max_servers
    )
    # move servers to regions according to scheduling estimation the next hour
    server_manager.move(servers_per_region)


if __name__ == "__main__":
    main()
