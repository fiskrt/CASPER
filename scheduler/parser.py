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

    return parser.parse_args(argv)
