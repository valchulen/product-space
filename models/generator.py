from pypdevs.DEVS import AtomicDEVS

from configuration.base import get_run_parameters

class Generator(AtomicDEVS):
    def __init__(self):
        super(Generator, self).__init__("generator")
        self.diffuse_to = {}

    def timeAdvance(self):
        return 1

    def outputFnc(self):
        return {port: get_run_parameters().DIFFUSION_PARAMETER for port in self.diffuse_to.values()}

    def add_port(self, country):
        out_port = self.diffuse_to.get(country)
        if not out_port:
            self.diffuse_to[country] = out_port = self.addOutPort(f"to_{country}")
        return out_port