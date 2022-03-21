import numpy as np
from pypdevs.DEVS import CoupledDEVS

from configuration.base import get_run_parameters
from configuration.utils import ProductSpaceProps

from models.country import Country
from models.generator import Generator

class ProductSpace(CoupledDEVS):
    def __init__(self, name=None):
        super(ProductSpace, self).__init__(name)
        self.generator = generator = Generator()
        self.addSubModel(generator)
        self.state = state = {}
        self.countries = countries = [Country(country_name) for country_name in get_run_parameters().COUNTRIES]
        phi_matrix = np.random.rand(get_run_parameters().NUM_PRODUCTS, get_run_parameters().NUM_PRODUCTS)
        phi_matrix = phi_matrix @ phi_matrix.T
        self.phi_matrix = phi_matrix
        for country in countries:
            self.addSubModel(country)
            state[country.name] = []
            generator_port = generator.add_port(country.name)
            self.connectPorts(generator_port, country.in_port)


    def globalTransition(self, e_g, x_b_micro, *args, **kwargs):
        for country, competitive_exports in x_b_micro:
            self.state[country] = competitive_exports
        # if v2:
        self._calculate_phi_matrix()
        # logger.error(self.state)

    def _calculate_phi_matrix(self):
        pass

    def getContextInformation(self, property, *args, **kwargs):
        if property == ProductSpaceProps.PHI_MATRIX:
            return self.phi_matrix