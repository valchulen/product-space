import pickle

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from models.product_space import exports_to_phi


class ProductSpaceGraph:
    def __init__(self, file):  # "exports_history.pkl"
        exports_history = pickle.load(open(file, "rb"))
        self.exports_by_generation = pd.DataFrame(exports_history,
                                                  columns=("country", "generation", "exports")) \
                                       .set_index(["generation", "country"]).sort_index()
        self.exports_by_country = pd.DataFrame(exports_history,
                                               columns=("country", "generation", "exports")) \
                                    .set_index(["country", "generation"]).sort_index()

    def X_by_generation(self, generation):
        return np.stack(self.exports_by_generation.loc[generation].unstack().to_numpy()).T

    def product_discovery(self, country):
        # Cambio listas de 0s y 1s por listas de enteros contemplando el numero de generacion
        # De esta forma, despues me quedo con el minimo para cada producto
        number_exports = self.exports_by_country.loc[country].exports * (self.exports_by_country.loc[country].index + 1)
        return pd.DataFrame(number_exports.to_list()).replace({'0': np.nan, 0: np.nan}).min() - 1

    def mst(self):
        phi_0 = exports_to_phi(self.X_by_generation(0))
        return nx.maximum_spanning_tree(nx.from_numpy_array(phi_0))

    def plot(self, country, title):
        plt.figure(figsize=(12, 10))

        # Fue la mejor forma que encontré de poner un color distinto a los NaN (productos que nunca se llegan a desarrollar)
        color_dict = {
            0: "green",
            1: "greenyellow",
            2: "yellow",
            3: "orange",
            4: "red"
        }

        def select_color(value):
            return color_dict.get(value, "black")

        nx.draw_kamada_kawai(self.mst(), node_size=50,
                                     node_color=self.product_discovery(country).apply(select_color))

        for iterations, color in color_dict.items():
            plt.plot([0], [0], 'o', color=color, label=iterations)
        plt.plot([0], [0], 'o', color='white')
        plt.legend(title="Pasos de simulación")
        plt.title(title)
