from collections.abc import Iterable, Sequence
from typing import TypeVar, cast

import numpy as np
import pysindy as ps
from gen_experiments.data import _signal_avg_power
from gen_experiments.gridsearch.typing import (
    GridLocator,
    SeriesDef,
    SeriesList,
    SkinnySpecs,
)
from gen_experiments.plotting import _PlotPrefs
from gen_experiments.typing import NestedDict
from gen_experiments.utils import FullSINDyTrialData
from numpy.typing import NDArray

T = TypeVar("T", bound=str)
U = TypeVar("U")


def ND(d: dict[T, U]) -> NestedDict[T, U]:
    return NestedDict(**d)


def _convert_abs_rel_noise(
    scan_grid: dict[str, NDArray[np.floating]],
    recent_results: FullSINDyTrialData,
) -> dict[str, Sequence[np.floating]]:
    """Convert abs_noise grid_vals to rel_noise"""
    signal = np.stack(recent_results["x_true"], axis=-1)
    signal_power = _signal_avg_power(signal)
    plot_grid = scan_grid.copy()
    new_vals = plot_grid["sim_params.noise_abs"] / signal_power
    plot_grid["sim_params.noise_rel"] = new_vals
    plot_grid.pop("sim_params.noise_abs")
    return cast(dict[str, Sequence[np.floating]], plot_grid)


# To allow pickling
def identity(x):
    return x


def quadratic(x):
    return x * x


def addn(x):
    return x + x


plot_prefs = {
    "absrel-newloc": _PlotPrefs(
        True,
        False,
        GridLocator(
            ["coeff_mse", "coeff_f1"],
            (..., (2, 3, 4)),
            (
                {"diff_params.kind": "kalman", "diff_params.alpha": "gcv"},
                {
                    "diff_params.kind": "kalman",
                    "diff_params.alpha": lambda a: isinstance(a, float | int),
                },
                {"diff_params.kind": "trend_filtered"},
                {"diff_params.diffcls": "SmoothedFiniteDifference"},
            ),
        ),
    ),
    "all-kernel": _PlotPrefs(
        True,
        False,
        GridLocator(..., (..., ...), ({"diff_params.kind": "kernel"},)),
    ),
}
sim_params = {
    "debug": ND({"n_trajectories": 1, "dt": 0.1, "t_end": 1, "noise_abs": 0.0}),
    "test": ND({"n_trajectories": 2}),
    "test-r1": ND({"n_trajectories": 2, "noise_rel": 0.01}),
    "test-r2": ND({"n_trajectories": 2, "noise_rel": 0.1}),
    "test-r3": ND({"n_trajectories": 2, "noise_rel": 0.3}),
    "10x": ND({"n_trajectories": 10}),
    "10x-plot-noise": ND({"n_trajectories": 10, "noise_rel": 0.1, "t_end": 8}),
}
diff_params = {
    "test": ND({"diffcls": "FiniteDifference"}),
    "autoks": ND({"diffcls": "sindy", "kind": "kalman", "alpha": "gcv"}),
    "tv": ND({"diffcls": "sindy", "kind": "trend_filtered", "order": 0, "alpha": 1}),
    "sfd-ps": ND({"diffcls": "SmoothedFiniteDifference"}),
    "kalman": ND({"diffcls": "sindy", "kind": "kalman", "alpha": 0.000055}),
    "kalman-empty2": ND({"diffcls": "sindy", "kind": "kalman", "alpha": None}),
    "kalman-auto": ND(
        {"diffcls": "sindy", "kind": "kalman", "alpha": None, "meas_var": 0.8}
    ),
    "kernel-default": ND({"diffcls": "sindy", "kind": "kernel"}),
}
feat_params = {
    "test": ND({"featcls": "Polynomial"}),
    "test2": ND({"featcls": "Fourier"}),
    "cubic": ND({"featcls": "Polynomial", "degree": 3}),
    "quadratic": ND({"featcls": "Polynomial", "degree": 2}),
    "quadratic-noconst": ND(
        {"featcls": "Polynomial", "degree": 2, "include_bias": False}
    ),
    "testweak": ND({"featcls": "weak"}),
}
opt_params = {
    "test": ND({"optcls": "STLSQ"}),
    "test_low": ND({"optcls": "STLSQ", "threshold": 0.09}),
    "miosr": ND({"optcls": "MIOSR"}),
    "enslsq": ND(
        {"optcls": "ensemble", "opt": ps.STLSQ(), "bagging": True, "n_models": 20}
    ),
    "ensmio-ho-vdp-lv-duff": ND(
        {
            "optcls": "ensemble",
            "opt": ps.MIOSR(target_sparsity=4, unbias=True),
            "bagging": True,
            "n_models": 20,
        }
    ),
    "ensmio-hopf": ND(
        {
            "optcls": "ensemble",
            "opt": ps.MIOSR(target_sparsity=8, unbias=True),
            "bagging": True,
            "n_models": 20,
        }
    ),
    "ensmio-lorenz-ross": ND(
        {
            "optcls": "ensemble",
            "opt": ps.MIOSR(target_sparsity=7, unbias=True),
            "bagging": True,
            "n_models": 20,
        }
    ),
    "mio-lorenz-ross": ND({"optcls": "MIOSR", "target_sparsity": 7, "unbias": True}),
    "miosr-vdp-quad": ND({"optcls": "MIOSR", "target_sparsity": 3, "unbias": True}),
    "miosr-vdp-cub": ND({"optcls": "MIOSR", "target_sparsity": 4, "unbias": True}),
}

# Grid search parameters
metrics = {
    "test": ["coeff_f1", "coeff_mae"],
    "all-coeffs": ["coeff_f1", "coeff_mae", "coeff_mse"],
    "all": ["coeff_f1", "coeff_precision", "coeff_recall", "coeff_mae", "coeff_mse"],
    "lorenzk": ["coeff_f1", "coeff_precision", "coeff_recall", "coeff_mae"],
    "1": ["coeff_f1", "coeff_precision", "coeff_mse", "coeff_mae"],
}
other_params = {
    "debug": ND(
        {
            "sim_params": sim_params["debug"],
            "diff_params": diff_params["kernel-default"],
            "feat_params": feat_params["test"],
            "opt_params": opt_params["test"],
        }
    ),
    "test": ND(
        {
            "sim_params": sim_params["test"],
            "diff_params": diff_params["test"],
            "feat_params": feat_params["test"],
            "opt_params": opt_params["test"],
        }
    ),
    "rel-exp3-lorenz": ND(
        {
            "sim_params": sim_params["10x"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["ensmio-lorenz-ross"],
        }
    ),
    "lor-ross-cubic": ND(
        {
            "sim_params": sim_params["10x"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["ensmio-lorenz-ross"],
        }
    ),
    "lor-ross-kernel": ND(
        {
            "diff_params": diff_params["kernel-default"],
            "sim_params": sim_params["10x-plot-noise"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["ensmio-lorenz-ross"],
        }
    ),
    "lor-ross-cubic-fast": ND(
        {
            "sim_params": sim_params["test"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["mio-lorenz-ross"],
        }
    ),
    "4nonzero-cubic": ND(
        {
            "sim_params": sim_params["10x"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["ensmio-ho-vdp-lv-duff"],
        }
    ),
    "4nonzero-kernel": ND(
        {
            "diff_params": diff_params["kernel-default"],
            "sim_params": sim_params["10x-plot-noise"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["ensmio-ho-vdp-lv-duff"],
        }
    ),
    "hopf-cubic": ND(
        {
            "sim_params": sim_params["10x"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["ensmio-hopf"],
        }
    ),
    "hopf-kernel": ND(
        {
            "diff_params": diff_params["kernel-default"],
            "sim_params": sim_params["10x-plot-noise"],
            "feat_params": feat_params["cubic"],
            "opt_params": opt_params["ensmio-hopf"],
        }
    ),
}
grid_params = {
    "rel_noise": ["sim_params.t_end", "sim_params.noise_rel"],
    "kernel_noise": ["diff_params.lmbd"],
    "kernel_noise_scale": ["diff_params.lmbd", "diff_params.sigma"],
}
grid_vals: dict[str, list[Iterable]] = {
    "small_even": [np.logspace(-2, 2, 5)],
    "small_even2": [np.logspace(-2, 2, 5), np.logspace(-2, 2, 5)],
    "duration-absnoise": [[0.5, 1, 2, 4, 8, 16], [0.1, 0.5, 1, 2, 4, 8]],
    "rel_noise": [[0.5, 1, 2, 4, 8, 16], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]],
}
grid_decisions = {
    "test": ["plot"],
    "plot2": ["plot", "plot"],
    "noplot": ["max", "max"],
}
diff_series: dict[str, SeriesDef] = {}
series_params: dict[str, SeriesList] = {}


skinny_specs: dict[str, SkinnySpecs] = {}

lu = {
    "plot_prefs": plot_prefs,
    "sim_params": sim_params,
    "diff_params": diff_params,
    "feat_params": feat_params,
    "opt_params": opt_params,
    "metrics": metrics,
    "other_params": other_params,
    "grid_params": grid_params,
    "grid_vals": grid_vals,
    "grid_decisions": grid_decisions,
    "diff_series": diff_series,
    "series_params": series_params,
    "skinny_specs": skinny_specs,
}
