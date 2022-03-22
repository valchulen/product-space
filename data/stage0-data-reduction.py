# Este script toma la información descargada del dataverse y la reduce para poder agregarla al repositorio
import pandas as pd

df = pd.read_csv("country_sitcproduct4digit_year.csv")

desired_columns = ['year', 'sitc_product_code', 'location_code', 'export_value', 'export_rca']
df = df[desired_columns]
df.fillna(0.0)

export_totals_by_product = df[["year", "sitc_product_code", "export_value"]].groupby(["year", "sitc_product_code"]).sum()
export_totals_by_country = df[["year", "location_code", "export_value"]].groupby(["year", "location_code"]).sum()
export_totals_by_year = df[["year", "export_value"]].groupby("year").sum()

df.set_index(desired_columns[:3], inplace=True)
df = df.merge(export_totals_by_product, how="left", left_index=True, right_index=True, suffixes=(None, "_product_total"), copy=False)
df = df.merge(export_totals_by_country, how="left", left_index=True, right_index=True, suffixes=(None, "_country_total"), copy=False)
df = df.merge(export_totals_by_year, how="left", left_index=True, right_index=True, suffixes=(None, "_year_total"), copy=False)


df["rca"] = (df.export_value / df.export_value_country_total) / (df.export_value_product_total / df.export_value_year_total)
((df.export_rca - df.rca) / df.export_rca).abs().describe()
# Calculamos el RCA para poder compararlo, dio error pero tampoco imposible, decidimos usar el RCA provisto por el dataset
df = df.reset_index()[['year', 'sitc_product_code', 'location_code', 'export_rca']]
df.to_csv("stage1_year_product_country_rca.csv", index=False)