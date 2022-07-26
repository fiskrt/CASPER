import argparse


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--algorithm",
        choices=["latency_greedy", "carbon_greedy", "carbon_aware"],
        help="The scheduling algorithm to use",
        default="latency_greedy",
    )

    parser.add_argument(
        "-t",
        "--timesteps",
        type=int,
        help="The total number of hours",
        default=24,
    )

    parser.add_argument(
        "-r",
        "--request-update-interval",
        type=int,
        help="The number of minutes between each scheduling",
        choices=range(0, 61),
        metavar="[0-60]",
        default=10,
    )

    parser.add_argument(
        "--load",
        type=str,
        help="Name of file to load and plot",
    )

    parser.add_argument(
        "--save",
        help="Save file to /saved with the following format YYYY-MM-DD_hh:mm:ss",
        action="store_true",
    )

    parser.add_argument(
        "-d",
        "--start-date",
        type=str,
        help="Start date in ISO format (YYYY-MM-DD)",
        default="2021-01-01",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Print information for every timestep",
        action="store_true",
    )

    parser.add_argument(
        "-l",
        "--latency",
        type=int,
        help="Maximum latency allowed",
        default=50,
    )

    parser.add_argument(
        "-m",
        "--max-servers",
        type=int,
        help="Maximum pool of servers",
        default=4,
    )

    parser.add_argument(
        "--rate",
        type=int,
        help="Specify a constant rate",
    )

    parser.add_argument(
        "-c",
        "--server-capacity",
        type=int,
        help="The capacity of each server",
        default=1_000_000,
    )

    return parser.parse_args(argv)
