
_PARAMETERS = None

def get_run_parameters():
    return _PARAMETERS

class Parameters:
    COUNTRIES = []
    NUM_PRODUCTS = 0
    DIFFUSION_PARAMETER = 0.0

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            k = k.upper()
            setattr(self, k, v)
