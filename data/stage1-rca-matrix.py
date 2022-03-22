import pickle
import pandas as pd
df = pd.read_csv("stage1_year_product_country_rca.csv")

# TODO: @valen transformar en un apply asi deja de ser feo
# TODO: filtrar los productos que NO tienen 3 o 4 digitos (o 3), o son servicio
df = df.pivot(index='year', columns=['sitc_product_code', 'location_code'], values="export_rca")

products = df.iloc[0].index.unique(0).to_list()
countries = df.iloc[0].index.unique(1).to_list()

matrices = {}
for year in df.index:
    X = df.loc[year].to_frame().unstack().to_numpy()
    X = 1 * (X > 1)
    matrices[year] = X

with open("stage1_data.pkl", "wb") as out:
    pickle.dump({
        "X_matrices": matrices,
        "products": products,
        "countries": countries,
    }, out)
