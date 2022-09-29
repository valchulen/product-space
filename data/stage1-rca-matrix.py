import pickle
import pandas as pd
import numpy as np

df = pd.read_csv("stage1_year_product_country_rca.csv", dtype={"sitc_product_code": str})

df = df.pivot(index="year", columns=["sitc_product_code", "location_code"], values="export_rca")

products = df.iloc[0].index.unique(0).to_list()
countries = [c for _, c in df.iloc[0].to_frame().unstack().columns.to_list()]

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
