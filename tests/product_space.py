import unittest
import numpy as np
from models.product_space import exports_to_phi


def test_exports_to_phi():
    X = np.array([
        np.array([1, 1, 1, 1, 0, 0, 0]),
        np.array([0, 0, 1, 1, 1, 0, 0]),
        np.array([1, 0, 1, 1, 0, 1, 1]),
    ])
    phi = exports_to_phi(X)

    expected_phi = np.array([
        np.array([1.0, 0.5, 0.6]),
        np.array([0.5, 1.0, 0.4]),
        np.array([0.6, 0.4, 1.0]),
    ])
    np.testing.assert_almost_equal(phi, expected_phi)


def test_exports_to_phi2():
    X = np.array([
        np.array([1, 1, 1, 1, 0, 0, 0]),
        np.array([0, 0, 0, 1, 1, 1, 0]),
        np.array([0, 0, 0, 0, 0, 1, 1]),
    ])
    phi = exports_to_phi(X)

    expected_phi = np.array([
        np.array([1.0, 1/4, 0.0]),
        np.array([1/4, 1.0, 1/3]),
        np.array([0.0, 1/3, 1.0]),
    ])
    np.testing.assert_almost_equal(phi, expected_phi)
