
# Import code for DEVS model representation:
from asyncio.log import logger
from pypdevs.DEVS import *
from pypdevs.simulator import Simulator
import numpy as np

np.random.seed(100)

# This is a polimorphic class for the enumeration. Do not change.
def enum(**kwargs):
    class Enum(object): pass
    obj = Enum()
    obj.__dict__.update(kwargs)
    return obj


# Model parameters
class Parameters:
    COUNTRIES = ["ARG", "CHL"]
    NUM_PRODUCTS = 100
    DIFFUSION_PARAMETER = 0.45

ActionState = enum(P="PROPAGATING", N="NORMAL")
ProductSpaceProps = enum(PHI_MATRIX="phi_matrix")

INF = float("inf")


class Generator(AtomicDEVS):
    def __init__(self):
        super(Generator, self).__init__("generator")
        self.diffuse_to = {}

    def timeAdvance(self):
        return 1

    def outputFnc(self):
        return {port: Parameters.DIFFUSION_PARAMETER for port in self.diffuse_to.values()}

    def add_port(self, country):
        out_port = self.diffuse_to.get(country)
        if not out_port:
            self.diffuse_to[country] = out_port = self.addOutPort(f"to_{country}")
        return out_port


class Country(AtomicDEVS):
    def __init__(self, name=None):
        super(Country, self).__init__(name)
        self.elapsed = 0
        self.competitive_exports = np.random.randint(0, 2, Parameters.NUM_PRODUCTS)
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
        logger.error(omega.max())
        exports = omega < big_omega
        self.state["competitive_exports"] = self.competitive_exports = exports | self.competitive_exports


class ProductSpace(CoupledDEVS):
    def __init__(self, name=None):
        super(ProductSpace, self).__init__(name)
        self.generator = generator = Generator()
        self.addSubModel(generator)
        self.state = state = {}
        self.countries = countries = [Country(country_name) for country_name in Parameters.COUNTRIES]
        phi_matrix = np.random.rand(Parameters.NUM_PRODUCTS, Parameters.NUM_PRODUCTS)
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
        logger.error(self.state)

    def _calculate_phi_matrix(self):
        pass

    def getContextInformation(self, property, *args, **kwargs):
        if property == ProductSpaceProps.PHI_MATRIX:
            return self.phi_matrix


# Run a single experiment with the parameters configured in Parameters static class
def run_single(duration):
    environ = ProductSpace(name='ProductSpace')
    sim = Simulator(environ)
    sim.setTerminationTime(duration)
    sim.setClassicDEVS()
    sim.simulate()
run_single(3)