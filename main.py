import logging
import argparse
import pickle
import numpy as np
from pypdevs.simulator import Simulator

import configuration.base

from models.product_space import ProductSpace

np.random.seed(100)

logger = logging.getLogger(__name__)


# Run a single experiment with the parameters configured in Parameters static class
def run_single(options):
    logger.info("Starting simulation with duration %d", options.duration)
    data = pickle.load(options.X_matrices_file)
    X_matrices = data["X_matrices"]

    configuration.base._PARAMETERS = configuration.base.Parameters(
        countries=["ARG", "CHL"], difussion_parameter=0.45,
        X=X_matrices[options.year], num_products=X_matrices[options.year].shape[0]
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
    args.add_argument("--X-matrices-file", "-f", type=argparse.FileType("rb"), default="data/stage1_data.pkl")
    args.add_argument("--year", "-y", type=int, default=2000)

    options = args.parse_args()

    logging.basicConfig(level=getattr(logging, options.logging_level.upper()))
    run_single(options)


if __name__ == "__main__":
    main()
