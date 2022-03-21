import numpy as np
from pypdevs.DEVS import AtomicDEVS


from configuration.base import get_run_parameters
from configuration.utils import ProductSpaceProps


class Country(AtomicDEVS):
    def __init__(self, name=None):
        super(Country, self).__init__(name)
        self.elapsed = 0
        self.competitive_exports = np.random.randint(0, 2, get_run_parameters().NUM_PRODUCTS)
        self.state = {"competitive_exports": self.competitive_exports}
        self.y_up = self.competitive_exports
        self.in_port = self.addInPort("diffusion")

    def __lt__(self, other):
        return self.name < other.name

    def extTransition(self, inputs):
        for port, value in inputs.items():
            if port.name == "diffusion":
                self.diffuse(value, self.parent.getContextInformation(ProductSpaceProps.PHI_MATRIX))
                self.y_up = (self.name, self.state["competitive_exports"])
        return self.state

    def diffuse(self, big_omega, phi_matrix):
        omega = self.competitive_exports @ phi_matrix
        phi_sum = phi_matrix @ np.ones_like(omega)
        omega = omega / phi_sum
        # logger.error(omega.max())
        exports = omega < big_omega
        self.state["competitive_exports"] = self.competitive_exports = exports | self.competitive_exports
