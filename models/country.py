import logging
from metrics.saver import save_competitive_exports, save_d_vector
import numpy as np
from pypdevs.DEVS import AtomicDEVS

logger = logging.getLogger(__name__)


from configuration.base import get_run_parameters
from configuration.utils import ProductSpaceProps


class Country(AtomicDEVS):
    def __init__(self, name=None, competitive_exports=None):
        super(Country, self).__init__(name)
        # logger.error("%s: %s", name, competitive_exports)
        self.elapsed = 0
        self.year_elapsed = 0
        self.competitive_exports = competitive_exports
        save_competitive_exports(competitive_exports, self.name, self.year_elapsed)
        self.state = {"competitive_exports": competitive_exports}
        self.in_port = self.addInPort("diffusion")

    def __lt__(self, other):
        return self.name < other.name

    def extTransition(self, inputs):
        for port, value in inputs.items():
            if port.name == "diffusion":
                self.diffuse(value, self.parent.getContextInformation(ProductSpaceProps.PHI_MATRIX))
                self.y_up = (self.name, self.state["competitive_exports"])
                self.year_elapsed += 1
        return self.state

    def diffuse(self, big_omega, phi_matrix):
        d = (phi_matrix @ np.diagflat(self.competitive_exports)).max(1)
        save_d_vector(d, self.name, self.year_elapsed)
        exports = d > big_omega
        if (exports & ~self.competitive_exports).sum() > 0:
            logger.error("%s discovered %d new products", self.name, (exports & ~self.competitive_exports).sum())
        self.state["competitive_exports"] = self.competitive_exports = exports | self.competitive_exports
        save_competitive_exports(self.competitive_exports, self.name, self.year_elapsed + 1)
