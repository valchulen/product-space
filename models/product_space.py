import logging
import numpy as np
from pypdevs.DEVS import CoupledDEVS

from configuration.base import get_run_parameters
from configuration.utils import ProductSpaceProps

from models.country import Country
from models.generator import Generator

logger = logging.getLogger(__name__)


def exports_to_phi(X):
    phi = X @ X.T
    # cantidad de paises que exportan cada producto
    S = phi.diagonal()
    # matriz que en cada fila tiene a S
    M = np.reshape(np.ones_like(S), (-1, 1)) @ np.reshape(S, (1, -1))
    # M[i,j] = max(sumatoria_c Xci, sumatoria_c Xcj)
    # dividir por el maximo me va a dar el minimo
    M = (M * (M >= M.T)) + (M.T * (M < M.T))
    # cuenta final,out y where hacen que la probabilidad sea 0 cuando se intenta dividir por 0
    # esto pasa cuando ninguno de los dos productos se exportan en ningun pais
    return np.divide(phi, M, out=np.zeros_like(phi, dtype=np.float64), where=(M != 0))


class ProductSpace(CoupledDEVS):
    def __init__(self, should_update_phi_matrix=False):
        name = "ProductSpace"
        super(ProductSpace, self).__init__(name)
        self.generator = generator = Generator()
        self.addSubModel(generator)
        self.update_phi_matrix = should_update_phi_matrix
        self.state = state = {}
        self.competitive_exports_matrix = competitive_exports_matrix = get_run_parameters().X.copy()
        self.countries = countries = [
            Country(country_name, competitive_exports_matrix[:, c])
            for c, country_name in enumerate(get_run_parameters().COUNTRIES)
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
            self.competitive_exports_matrix[:, get_run_parameters().COUNTRIES.index(country)] = competitive_exports
        if self.update_phi_matrix:
            self._calculate_phi_matrix(self.competitive_exports_matrix)

    def _calculate_phi_matrix(self, X):
        # phi[i,j] = sumatoria_c (Xci * Xcj)
        # cantidad de paises que exportan tanto i como j
        self.state["phi_matrix"] = self.phi_matrix = exports_to_phi(X)

    def getContextInformation(self, property, *args, **kwargs):
        if property == ProductSpaceProps.PHI_MATRIX:
            return self.phi_matrix
