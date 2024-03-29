import pickle

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import math

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
        mst = nx.maximum_spanning_tree(nx.from_numpy_array(phi_0))
        # Hidalgo agrega aristas importantes al MST
        G = nx.compose(mst, nx.from_numpy_array(1* (phi_0 > 0.55)))
        G.remove_edges_from(nx.selfloop_edges(G))
        return G

    def plot(self, country, title=None, legend_title="Pasos de simulación", figsize=(12, 10), node_size=20, show_t0=True):
        plt.figure(figsize=figsize)

        # Fue la mejor forma que encontré de poner un color distinto a los NaN (productos que nunca se llegan a desarrollar)
        color_dict = {
            0: "green" if show_t0 else "gainsboro", #"green",
            1: "greenyellow",
            2: "yellow",
            3: "orange",
            4: "red"
        }

        def select_color(value):
            return color_dict.get(value, "gainsboro")

        G = self.mst()

#        for iterations, color in color_dict.items():
#            plt.plot([0], [0], 'o', color=color, label=iterations)

        nx.draw(G, pos=nx.kamada_kawai_layout(G),
                node_size=node_size, edge_color='gainsboro',
                node_color=self.product_discovery(country).apply(select_color))

        #plt.plot([0], [0], 'o', color='white')
        #plt.legend(title=legend_title)
        if title:
            plt.title(title)
