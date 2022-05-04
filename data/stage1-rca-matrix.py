import pickle
import pandas as pd
import numpy as np

df = pd.read_csv("stage1_year_product_country_rca.csv", dtype={"sitc_product_code": str})


# TODO: chequear que realmente los grupos de productos sumas lo mismo que sus subgrupos
def filter_product_groups(data):
    prods = data["sitc_product_code"].unique()

    def condition(product):
        # No existe ningún producto que tiene como prefijo a este producto
        return not np.vectorize(
            lambda another_product: another_product != product and another_product.startswith(product)
        )(prods).any()

    base_products = list(filter(condition, prods))

    return data[data["sitc_product_code"].isin(base_products)]


# TODO: @valen transformar en un apply asi deja de ser feo
df = filter_product_groups(df)
df = df.pivot(index="year", columns=["sitc_product_code", "location_code"], values="export_rca")

products = df.iloc[0].index.unique(0).to_list()
countries = df.iloc[0].index.unique(1).to_list()

matrices = {}
for year in df.index:
    X = df.loc[year].to_frame().unstack().to_numpy()
    X = 1 * (X > 1)
    matrices[year] = X

with open("stage1_data.pkl", "wb") as out:
    pickle.dump(
        {
            "X_matrices": matrices,
            "products": products,
            "countries": countries,
        },
        out,
    )
