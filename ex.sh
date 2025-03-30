
###############Failure experiments####################3
# Figure 1.2
nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"lorenz\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_abs=0.2 \
    -e data.n_trajectories=2 \
    -e data.dt=.01 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=ensmio-lorenz-ross &> fig1.2a.log &

nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"lorenz\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_abs=2.0 \
    -e data.n_trajectories=2 \
    -e data.dt=.01 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=ensmio-lorenz-ross &> fig1.2b.log &

nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"lorenz\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_abs=0.2 \
    -e data.n_trajectories=2 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=ensmio-lorenz-ross &> fig1.2c.log &

nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"lorenz_sin_forced\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_abs=0.2 \
    -e data.n_trajectories=2 \
    -e data.dt=.01 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=ensmio-lorenz-ross &> fig1.2d.log &

# Figure 1.3
nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"vdp\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=miosr-vdp-quad &> fig1.3a.log &

nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"vdp\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=cubic \
    -p odes.opt_params=miosr-vdp-cub &> fig1.3b.log &

nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"pendulum\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.ic_stdev=0.1 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=short-lin-sin \
    -p odes.opt_params=enslsq &> fig1.3c.log &

# Fig 1.4
nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"lorenz\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_rel=0.0 \
    -e data.n_trajectories=2 \
    -e data.dt=.01 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=ensmio-lorenz-ross &> fig1.4a.log &

nohup mitosis data ablate \
    -F trials/intro \
    -e data.group=\"lorenz\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_rel=0.0 \
    -e data.n_trajectories=2 \
    -e data.dt=.01 \
    -p ablate.diff_params=sfd-ps \
    -p ablate.feat_params=quadratic \
    -p ablate.opt_params=miosr-vdp-cub &> fig1.4b.log &

nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"kinematics\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_abs=0.2 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps-smooth \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=test &> fig1.4c.log &

nohup mitosis data odes \
    -F trials/intro \
    -e data.group=\"kinematics\" \
    -e data.seed=6 \
    -e data.t_end=10 \
    -e data.noise_abs=0.2 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps-smooth \
    -p odes.feat_params=lin-cubic \
    -p odes.opt_params=test &> fig1.4d.log &




#########################################kernel experimentsE###########################

# --param other_params=lor-ross-cubic \
nohup mitosis gridsearch \
    --debug \
    -F trials \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"none\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=4nonzero-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel &> mock.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"lorenz\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=lor-ross-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> lorenz.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"cubic_ho\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=4nonzero-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=more_noise \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> cubic_ho.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"sho\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=4nonzero-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> sho.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"vdp\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=4nonzero-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> vdp.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"lv\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=4nonzero-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> lv.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"duff\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=4nonzero-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> duff.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"hopf\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=hopf-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> hopf.log &

nohup mitosis gridsearch \
    -F trials/kernel \
    -e gridsearch.seed=19 \
    -e gridsearch.group=\"ross\" \
    --param gridsearch.metrics=all \
    --param gridsearch.other_params=lor-ross-kernel \
    --param gridsearch.grid_params=kernel_noise_scale \
    --param gridsearch.grid_vals=small_even2 \
    --param gridsearch.grid_decisions=noplot \
    --param +gridsearch.plot_prefs=all-kernel  &> ross.log &
