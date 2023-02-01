import logging
from metrics.saver import save_competitive_exports, save_d_vector
import numpy as np
from pypdevs.DEVS import AtomicDEVS

from configuration.utils import ProductSpaceProps

logger = logging.getLogger(__name__)


class Country(AtomicDEVS):
    def __init__(self, name=None, competitive_exports=None):
        super(Country, self).__init__(name)
        self.state = {"competitive_exports": competitive_exports}
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
        pi = (phi_matrix @ np.diagflat(self.state["competitive_exports"])).max(1)
        self.state["competitive_exports"] = pi > big_omega
