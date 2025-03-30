# %%
from pathlib import Path
from typing import NewType

import matplotlib.pyplot as plt
from gen_experiments.plotting import (
    _plot_training_trajectory,
    plot_coefficients,
    _plot_test_sim_data_2d,
    _plot_test_sim_data_3d,
    compare_coefficient_plots,
    plot_training_1d
)
from gen_experiments.odes import FullSINDyTrialData
from mitosis import load_trial_data

ExpKey = NewType("ExpKey", str)
TRIAL_DIR = Path(__file__).parents[1] / "trials/intro"
fig12_hexes = {
    "True": ExpKey("c357c6"),
    "Noisy": ExpKey("b57cb8"),
    "Long Interval": ExpKey("a07648"),
    "Forced": ExpKey("50ac0e"),
}
fig13_hexes = {
    "trial_quad_vdp": ExpKey("7a772b"),
    "trial_vdp": ExpKey("6c3a64"),
    "trial_pendulum": ExpKey("c92104"),
}
fig14_hexes = {
    # "trial_lor": ExpKey("4a20e3"),
    "trial_lor_ablate": ExpKey("9788eb"),
    "trial_kinem": ExpKey("c5cc66"),
    "trial_kinem_bad": ExpKey("c02e59"),
}

# %% Fig 1.2
def compare_noise(
    **trials: FullSINDyTrialData,
):
    """Show the effects of measurement/noise on SINDy

    First row: Training data
    Second row: Coefficients
    Third row: Simulations
    """
    fig = plt.figure(figsize=[8, 12])
    n_trials = len(trials)
    gs = plt.GridSpec(3, n_trials, height_ratios=[1, 2, 1])
    for col_ind, (name, trial) in enumerate(trials.items()):
        model = trial["model"]
        ax_training = fig.add_subplot(gs[col_ind], projection="3d")
        _plot_training_trajectory(
            ax_training,
            trial["x_train"],
            trial["x_true"],
            model.differentiation_method.smoothed_x_
        )
        ax_training.set_title(name)

        ax_coef = fig.add_subplot(gs[n_trials + col_ind])
        plot_coefficients(
            trial["coeff_fit"],
            trial["input_features"],
            trial["feature_names"],
            ax_coef,
            cbar=False
        )
        ax_sim = fig.add_subplot(gs[2 * n_trials + col_ind], projection="3d")
        _plot_test_sim_data_3d(ax_sim, trial["x_test"], "True Trajectory", "k")
        _plot_test_sim_data_3d(ax_sim, trial["x_sim"], "Simulation", "r--")
        fig.tight_layout()

lor_clean = {
    exp: load_trial_data(key, trials_folder=TRIAL_DIR)[1]["data"]
    for exp, key in fig12_hexes.items()
}
compare_noise(**lor_clean)


# %% Fig 1.3
def compare_features(
    trial_quad_vdp: FullSINDyTrialData,
    trial_vdp: FullSINDyTrialData,
    trial_pendulum: FullSINDyTrialData,
):
    """Show the effects of bad library on SINDy

    First row: Van der pol training data, 1d (L) cubic and quadratic libraries coef (R)
    Second row: training for nonlinear oscillator 1D (L) coefficient recovery  (R)
    """
    fig = plt.figure(figsize=[12, 12])
    gs = plt.GridSpec(4, 4)
    # VdP experiments
    
    for coord_ind in range(2):
        ax_train = fig.add_subplot(gs[coord_ind, :2])
        plot_training_1d(
            ax_train,
            coord_ind,
            trial_vdp["x_train"],
            trial_vdp["x_true"],
            trial_vdp["smooth_train"]
        )

    axs_coef = [fig.add_subplot(gs[:2, 2]), fig.add_subplot(gs[:2, 3])]
    compare_coefficient_plots(
        trial_quad_vdp["coeff_fit"],
        trial_vdp["coeff_fit"],
        trial_vdp["input_features"],
        trial_vdp["feature_names"],
        axs=axs_coef,
    )

    for coord_ind in range(2):
        ax_train = fig.add_subplot(gs[2 + coord_ind, :2])
        plot_training_1d(
            ax_train,
            coord_ind,
            trial_pendulum["x_train"],
            trial_pendulum["x_true"],
            trial_pendulum["smooth_train"]
        )

    axs_coef_p = [fig.add_subplot(gs[2:, 2]), fig.add_subplot(gs[2:, 3])]
    compare_coefficient_plots(
        trial_pendulum["coeff_fit"],
        trial_pendulum["coeff_true"],
        trial_pendulum["input_features"],
        trial_pendulum["feature_names"],
        axs=axs_coef_p,
    )
    axs_coef_p[0].set_title("")
    axs_coef_p[1].set_title("")
    fig.tight_layout()


feat_clean = {
    exp: load_trial_data(key, trials_folder=TRIAL_DIR)[1]["data"]
    for exp, key in fig13_hexes.items()
}
compare_features(**feat_clean)


# %% fig1.4
def create_fig1_4(
    trial_lor_ablate: FullSINDyTrialData,
    trial_kinem: FullSINDyTrialData,
    trial_kinem_bad: FullSINDyTrialData,
):
    """Show the effects of bad coordinates on SINDy

    First row: Show coefficient recovery vs true for ablated lorenz
    Second row: Coefficient recovery of kinematic system, quad vs cub  (L) Simulations, stacked (R)
    """
    fig = plt.figure(figsize=[16, 8])
    gs = fig.add_gridspec(2, 6)

    ax_lor_train = fig.add_subplot(gs[0, :2])
    _plot_training_trajectory(
        ax_lor_train, trial_lor_ablate["x_train"], trial_lor_ablate["x_true"], None
    )

    axs_lor_coeff = [fig.add_subplot(gs[0, 2]), fig.add_subplot(gs[0, 3])]
    compare_coefficient_plots(
        trial_lor_ablate["coeff_fit"],
        trial_lor_ablate["coeff_true"],
        trial_lor_ablate["input_features"],
        trial_lor_ablate["feature_names"],
        axs=axs_lor_coeff,
    )

    ax_lor_sim = fig.add_subplot(gs[0, 4:])
    _plot_test_sim_data_2d(
        [ax_lor_sim, ax_lor_sim], trial_lor_ablate["x_test"], trial_lor_ablate["x_sim"]
    )

    ax_lom_coeff_cu = fig.add_subplot(gs[1, 3])
    ax_kin_coeff_bad = fig.add_subplot(gs[1, 0])
    plot_coefficients(
        trial_kinem["coeff_fit"],
        trial_kinem["input_features"],
        trial_kinem["feature_names"],
        ax_lom_coeff_cu,
        cbar=False
    )
    plot_coefficients(
        trial_kinem_bad["coeff_fit"],
        trial_kinem_bad["input_features"],
        trial_kinem_bad["feature_names"],
        ax_kin_coeff_bad,
        cbar=False
    )

    ax_kin_sim_good = fig.add_subplot(gs[1, 4:])
    _plot_test_sim_data_2d(
        [ax_kin_sim_good, ax_kin_sim_good], trial_kinem["x_test"], trial_kinem["x_sim"]
    )

    ax_kin_sim_bad = fig.add_subplot(gs[1, 1:3])
    _plot_test_sim_data_2d(
        [ax_kin_sim_bad, ax_kin_sim_bad],
        trial_kinem_bad["x_test"],
        trial_kinem_bad["x_sim"]
    )
    fig.tight_layout()


coord_clean = {
    exp: load_trial_data(key, trials_folder=TRIAL_DIR)[1]["data"]
    for exp, key in fig14_hexes.items()
}
create_fig1_4(**coord_clean)

# %%
