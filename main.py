import numpy as np
from pypdevs.simulator import Simulator

import configuration.base

from models.product_space import ProductSpace

np.random.seed(100)

INF = float("inf")

# Run a single experiment with the parameters configured in Parameters static class
def run_single(duration):
    configuration.base._PARAMETERS = configuration.base.Parameters(
        countries=["ARG"],
        num_products=100,
        difussion_parameter=0.45
    )
    environ = ProductSpace(name='ProductSpace')
    sim = Simulator(environ)
    sim.setTerminationTime(duration)
    sim.setClassicDEVS()
    sim.simulate()
run_single(3)