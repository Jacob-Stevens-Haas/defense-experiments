
###############Failure experiments####################3
# Figure 1.2
# Works, needs tweak!
nohup mitosis data odes \
    --debug \
    -F trials/defense \
    -e data.group=\"lorenz_sin_forced\" \
    -e data.t_end=10 \
    -e data.noise_rel=.1 \
    -e data.dt=.4 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=testweak \
    -p odes.opt_params=ensmio-lorenz-ross &> fig1.2.log &

# Figure 1.3
# Works, needs tweak!
nohup mitosis data odes \
    --debug \
    -F trials/defense \
    -e data.group=\"vdp\" \
    -e data.t_end=10 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=miosr-vdp-quad &> fig1.3a.log &

# Works, needs tweak!
nohup mitosis data odes \
    --debug \
    -F trials/defense \
    -e data.group=\"vdp\" \
    -e data.t_end=10 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=cubic \
    -p odes.opt_params=miosr-vdp-cub &> fig1.3b.log &

# Works, needs tweak!
nohup mitosis data odes \
    --debug \
    -F trials/defense \
    -e data.group=\"pendulum\" \
    -e data.t_end=10 \
    -e data.ic_stdev=0.1
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=lin-plus-sin \
    -p odes.opt_params=stlsq &> fig1.3c.log &

# Fig 1.4
# HARD!
nohup mitosis data ablate \
    --debug \
    -F trials/defense \
    -e data.group=\"lorenz\" \
    -e data.t_end=10 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p ablate.diff_params=sfd-ps \
    -p ablate.feat_params=quadratic \
    -p ablate.opt_params=miosr-vdp-cub &> fig1.4a.log &

# Works, needs tweak!
nohup mitosis data odes \
    --debug \
    -F trials/defense \
    -e data.group=\"kinematics\" \
    -e data.t_end=10 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic \
    -p odes.opt_params=test &> fig1.4b.log &

# Works, needs tweak!
nohup mitosis data odes \
    --debug \
    -F trials/defense \
    -e data.group=\"kinematics\" \
    -e data.t_end=10 \
    -e data.noise_rel=0.01 \
    -e data.dt=.05 \
    -p odes.diff_params=sfd-ps \
    -p odes.feat_params=quadratic-noconst \
    -p odes.opt_params=test &> fig1.4c.log &




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
