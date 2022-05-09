import os
import pandas as pd

OMEGA = None
COMPETETIVE_EXPORTS = None


def start_metrics():
    global OMEGA, COMPETETIVE_EXPORTS
    OMEGA = []
    COMPETETIVE_EXPORTS = []


def export_metrics(metrics_folder=None):
    metrics_folder = metrics_folder or "metrics"
    max_omega = pd.DataFrame(
        data=[(country, generation, omega.max(), omega.min(), omega.mean()) for (country, generation, omega) in OMEGA],
        columns=("country", "generation", "max_omega", "min_omega", "mean_omega"),
    )
    max_omega.to_csv(os.path.join(metrics_folder, "omega.csv"), index=False)
    exports = pd.DataFrame(
        data=[(country, generation, exports.sum()) for (country, generation, exports) in COMPETETIVE_EXPORTS],
        columns=("country", "generation", "count_exports"),
    )
    exports.to_csv(os.path.join(metrics_folder, "exports.csv"), index=False)


def save_omega(omega, country, generation):
    global OMEGA
    OMEGA.append((country, generation, omega))


def save_competitive_exports(exports, country, generation):
    global COMPETETIVE_EXPORTS
    COMPETETIVE_EXPORTS.append((country, generation, exports))
