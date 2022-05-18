import os
import pandas as pd
import numpy as np

D_VECTOR = None
COMPETETIVE_EXPORTS = None


def start_metrics():
    global D_VECTOR, COMPETETIVE_EXPORTS
    D_VECTOR = []
    COMPETETIVE_EXPORTS = []


def export_metrics(metrics_folder=None):
    metrics_folder = metrics_folder or "metrics"
    d_vector_df = pd.DataFrame(
        data=[(country, generation, np.percentile(d, 25), np.percentile(d, 75), d.mean()) for (country, generation, d) in D_VECTOR],
        columns=("country", "generation", "p25", "p75", "mean_d"),
    )
    d_vector_df.to_csv(os.path.join(metrics_folder, "d_vector.csv"), index=False)
    exports = pd.DataFrame(
        data=[(country, generation, exports.sum()) for (country, generation, exports) in COMPETETIVE_EXPORTS],
        columns=("country", "generation", "count_exports"),
    )
    exports.to_csv(os.path.join(metrics_folder, "exports.csv"), index=False)


def save_d_vector(d, country, generation):
    global D_VECTOR
    D_VECTOR.append((country, generation, d))


def save_competitive_exports(exports, country, generation):
    global COMPETETIVE_EXPORTS
    COMPETETIVE_EXPORTS.append((country, generation, exports.copy()))
