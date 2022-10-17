import logging
import argparse
import pickle
from metrics.saver import export_metrics, start_metrics
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
    if data.get("phi") is not None:
        logger.info("Using phi matrix from data file")
    X_matrices = data["X_matrices"]

    configuration.base._PARAMETERS = configuration.base.Parameters(
        countries=data["countries"],
        diffusion_parameter=options.big_omega,
        X=X_matrices[options.year],
        PHI=data.get("phi"),
        num_products=X_matrices[options.year].shape[0],
    )
    start_metrics()
    environ = ProductSpace(should_update_phi_matrix=options.phi_matrix_update)
    sim = Simulator(environ)
    sim.setTerminationTime(options.duration)
    sim.setClassicDEVS()
    sim.simulate()
    export_metrics(options.metrics_folder, options.exports_history)


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--duration", "-d", type=int, required=True)
    args.add_argument("--logging-level", "-l", type=str, default="INFO")
    args.add_argument("--X-matrices-file", "-f", type=argparse.FileType("rb"), default="data/stage1_data.pkl")
    args.add_argument("--year", "-y", type=int, default=2000)
    args.add_argument("--big-omega", "-O", type=float, default=0.55)
    args.add_argument("--metrics-folder", "-m", type=str)
    args.add_argument("--phi-matrix-update", "-u", type=bool, default=False)
    args.add_argument("--exports-history", "-e", type=bool, default=False)

    options = args.parse_args()

    logging.basicConfig(level=getattr(logging, options.logging_level.upper()))
    run_single(options)


if __name__ == "__main__":
    main()
