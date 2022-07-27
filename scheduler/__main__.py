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
        # Move all the servers given the next hour's requests rates
        move(conf, server_manager, t)

        for i in range(request_update_interval):
            # get number of requests for timeframe
            batches = build_batches(conf, server_manager, t, request_update_interval=request_update_interval)

            # call the scheduling algorithm
            latency, carbon_intensity, requests_per_region = schedule_requests(
                conf, batches, server_manager, t, request_update_interval, max_latency=conf.latency
            )

            # send requests to servers
            server_manager.send(requests_per_region)

            # dropped requests
            dropped_requests_per_region = [0, 0, 0, 0]
            if len(server_manager.servers) == 0:
                for i in range(len(batches)):
                    dropped_requests_per_region[i] = batches[i].load

            # update_plot(plot, t, latency, carbon_intensity, requests_per_region)
            plot.add(server_manager, latency, carbon_intensity, requests_per_region, dropped_requests_per_region, t, i)

            # reset server utilization for every server before scheduling requests again
            # we can do this as requests are managed instantaneously for each server
            server_manager.reset()

        if conf.verbose:
            ui(t, requests_per_region, server_manager.servers, server_manager.servers_per_region())

    if conf.save:
        save_file(conf, plot)

    plot.plot()


def build_batches(conf, server_manager, t, request_update_interval=None):
    batches = []
    for region in server_manager.regions:
        rate = region.get_requests_per_hour(t)
        if conf.rate:
            rate = conf.rate
        if request_update_interval:
            rate //= request_update_interval
        # TODO: Add id to request batch
        batch = RequestBatch("", rate, region)
        batches.append(batch)
    return batches


def move(conf, server_manager, t):
    batches = build_batches(conf, server_manager, t)
    servers_per_region = schedule_servers(
        conf, batches, server_manager, t, max_latency=conf.latency, max_servers=conf.max_servers
    )
    # move servers to regions according to scheduling estimation the next hour
    server_manager.move(servers_per_region)


if __name__ == "__main__":
    main()
