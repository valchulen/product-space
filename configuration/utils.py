

# This is a polimorphic class for the enumeration. Do not change.
def enum(**kwargs):
    class Enum(object): pass
    obj = Enum()
    obj.__dict__.update(kwargs)
    return obj


ActionState = enum(P="PROPAGATING", N="NORMAL")
ProductSpaceProps = enum(PHI_MATRIX="phi_matrix")