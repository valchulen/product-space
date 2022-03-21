import logging
import argparse
import numpy as np
from pypdevs.simulator import Simulator

import configuration.base

from models.product_space import ProductSpace

np.random.seed(100)

logger = logging.getLogger(__name__)

# Run a single experiment with the parameters configured in Parameters static class
def run_single(options):
    # TODO: @tobi hacer que esto ande con info :)
    logger.warning("Starting simulation with duration %d", options.duration)
    configuration.base._PARAMETERS = configuration.base.Parameters(
        countries=["ARG"], num_products=100, difussion_parameter=0.45
    )
    environ = ProductSpace()
    sim = Simulator(environ)
    sim.setTerminationTime(options.duration)
    sim.setClassicDEVS()
    sim.simulate()


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--duration", "-d", type=int, required=True)
    args.add_argument("--logging-level", "-l", type=str, default="INFO")

    options = args.parse_args()

    logger.setLevel(getattr(logging, options.logging_level.upper()))
    run_single(options)


if __name__ == "__main__":
    main()
