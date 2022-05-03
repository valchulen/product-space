import logging
import numpy as np
from pypdevs.DEVS import CoupledDEVS

from configuration.base import get_run_parameters
from configuration.utils import ProductSpaceProps

from models.country import Country
from models.generator import Generator
logger = logging.getLogger(__name__)


class ProductSpace(CoupledDEVS):
    def __init__(self):
        name = "ProductSpace"
        super(ProductSpace, self).__init__(name)
        self.generator = generator = Generator()
        self.addSubModel(generator)
        self.state = state = {}
        competitive_exports_matrix = get_run_parameters().X
        self.countries = countries = [
            Country(country_name, competitive_exports_matrix[:, c]) for c, country_name in enumerate(get_run_parameters().COUNTRIES)
        ]
        self._calculate_phi_matrix(competitive_exports_matrix)
        for country in countries:
            self.addSubModel(country)
            state[country.name] = []
            generator_port = generator.add_port(country.name)
            self.connectPorts(generator_port, country.in_port)

    def globalTransition(self, e_g, x_b_micro, *args, **kwargs):
        for country, competitive_exports in x_b_micro:
            self.state[country] = competitive_exports
        # if v2:
        self._calculate_phi_matrix(get_run_parameters().X)
        # logger.info(self.state)
# 
    def _calculate_phi_matrix(self, X):
        phi = X @ X.T / (X.shape[1] ** 2)
        S = np.sum(X, axis=1)
        M = np.ones_like(S) @ S.T
        M = (M * (M <= M.T)) + (M.T * (M > M.T))
        self.state["phi_matrix"] = self.phi_matrix = phi * M
        print(self.phi_matrix)

    def getContextInformation(self, property, *args, **kwargs):
        if property == ProductSpaceProps.PHI_MATRIX:
            return self.phi_matrix
