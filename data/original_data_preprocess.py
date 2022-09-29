import pandas as pd
import numpy as np
import pickle

years = ["98", "99", "00"]
columns = ["Year", "Exporter", "sitc4", "Value"]

# Cargo datos originales
dfs = {
    year: pd.read_sas(f"wtf_data/wtf{year}.sas7bdat")
    for year in years
}

# Filtro y tipo
for year, df in dfs.items():
    cond = (
        dfs[year].sitc4.notnull() &
        (dfs[year].Importer == b"World") &
        (dfs[year].Exporter != b"World") &
        (dfs[year][dfs[year].sitc4.notnull()].sitc4.apply(lambda s: not (s.endswith(b"X") or s.endswith(b"A"))))
    )
    dfs[year] = dfs[year][cond]
    dfs[year] = dfs[year][columns].copy()
    dfs[year]["Exporter"] = dfs[year].Exporter.apply(lambda s: s.decode())
    dfs[year]["sitc4"] = dfs[year].sitc4.apply(lambda s: s.decode())

df = pd.concat(dfs.values())
# Unifico filas que tenian informacion de distintas unidades
# Ver FAQ: https://cid.econ.ucdavis.edu/data/undata/FAQ_on_NBER-UN_data.pdf
exports = df.groupby(["Year", "Exporter", "sitc4"]).sum().reset_index()

# Calculo marginales
total_country = exports[["Year", "Exporter", "Value"]].groupby(["Year", "Exporter"]).sum().rename(columns={"Value": "TotalCountry"})
total_product = exports[["Year", "sitc4", "Value"]].groupby(["Year", "sitc4"]).sum().rename(columns={"Value": "TotalProduct"})
total = exports.groupby("Year")["Value"].sum().rename("Total")
exports_totals = exports.join(total_country, on=["Year", "Exporter"]).join(total_product, on=["Year", "sitc4"]).join(total, on="Year")

# Calculo RCA
exports_totals["RCA"] = (exports_totals.Value / exports_totals.TotalCountry) / (exports_totals.TotalProduct / exports_totals.Total)

# Paso a matriz binaria anual
pivots = exports_totals.pivot(index="Year", columns=["sitc4", "Exporter"], values="RCA")
products = pivots.iloc[0].index.unique(0).to_list()
countries = [c for _, c in pivots.iloc[0].to_frame().unstack().columns.to_list()]
matrices = {}
for year in pivots.index:
    X = pivots.loc[year].to_frame().unstack().to_numpy()
    X = 1 * (X > 1)
    matrices[year] = X

def exports_to_phi(X):
    phi = X @ X.T
    # cantidad de paises que exportan cada producto
    S = phi.diagonal()
    # matriz que en cada fila tiene a S
    M = np.reshape(np.ones_like(S), (-1, 1)) @ np.reshape(S, (1, -1))
    # M[i,j] = max(sumatoria_c Xci, sumatoria_c Xcj)
    # dividir por el maximo me va a dar el minimo
    M = (M * (M >= M.T)) + (M.T * (M < M.T))
    # cuenta final,out y where hacen que la probabilidad sea 0 cuando se intenta dividir por 0
    # esto pasa cuando ninguno de los dos productos se exportan en ningun pais
    return np.divide(phi, M, out=np.zeros_like(phi, dtype=np.float64), where=(M != 0))

phis = {
    year: exports_to_phi(X)
    for year, X in matrices.items()
}

phi = (phis[1998] + phis[1999] + phis[2000]) / 3

with open("original_data.pkl", "wb") as out:
    pickle.dump(
        {
            "X_matrices": matrices,
            "phi": phi,
            "products": products,
            "countries": countries,
        },
        out,
    )
