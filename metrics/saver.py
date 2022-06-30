import os
import pandas as pd
import numpy as np
import pickle

D_VECTOR = None
COMPETITIVE_EXPORTS = None


def start_metrics():
    global D_VECTOR, COMPETITIVE_EXPORTS
    D_VECTOR = []
    COMPETITIVE_EXPORTS = []


def export_metrics(metrics_folder=None, exports_history=False):
    metrics_folder = metrics_folder or "metrics"
    d_vector_stats_df = pd.DataFrame(
        data=[(country, generation, np.percentile(d, 25), np.percentile(d, 75), d.mean()) for (country, generation, d) in D_VECTOR],
        columns=("country", "generation", "p25", "p75", "mean_d"),
    )
    d_vector_stats_df.to_csv(os.path.join(metrics_folder, "d_vector.csv"), index=False)

    exports = pd.DataFrame(
        data=[(country, generation, exports.sum()) for (country, generation, exports) in COMPETITIVE_EXPORTS],
        columns=("country", "generation", "count_exports"),
    )
    exports.to_csv(os.path.join(metrics_folder, "exports.csv"), index=False)

    if exports_history:
        with open(os.path.join(metrics_folder, "exports_history.pkl"), "wb") as out:
            pickle.dump(COMPETITIVE_EXPORTS, out)


def save_d_vector(d, country, generation):
    global D_VECTOR
    D_VECTOR.append((country, generation, d))


def save_competitive_exports(exports, country, generation):
    global COMPETITIVE_EXPORTS
    COMPETITIVE_EXPORTS.append((country, generation, exports.copy()))
