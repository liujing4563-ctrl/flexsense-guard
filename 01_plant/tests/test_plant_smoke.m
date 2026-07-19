%TEST_PLANT_SMOKE  Smoke test for the flexible joint plant.
%   Tests that:
%     1. Default parameters are valid
%     2. Dynamics function returns correct shape
%     3. Simulation runs without error
%     4. Output dimensions are correct
%
%   Run with: runtests('test_plant_smoke')

%% Test 1: Default parameters
params = flex_joint_default_params();
assert(params.J_m > 0, 'J_m must be positive');
assert(params.J_l > 0, 'J_l must be positive');
assert(params.K_s > 0, 'K_s must be positive');
fprintf('[PASS] Test 1: Default parameters valid\n');

%% Test 2: Dynamics evaluation
x = [0.0; 0.0; 0.0; 0.0];
u.tau_m = 1.0;
u.tau_ext = 0.0;
x_dot = flex_joint_dynamics(0, x, u, params);
assert(isequal(size(x_dot), [4, 1]), 'x_dot must be 4x1');
assert(all(isfinite(x_dot)), 'x_dot must be finite');
fprintf('[PASS] Test 2: Dynamics returns 4x1 finite vector\n');

%% Test 3: Simulation run
trajectory_fn = @(t) struct('tau_m', 0.5 * sin(2*pi*0.5*t), 'tau_ext', 0.0);
results = simulate_flex_joint(trajectory_fn, params, 0.001, 1.0);
assert(length(results.t) == 1001, 'Time vector must have 1001 elements');
assert(isequal(size(results.theta_m), [1001, 1]), 'theta_m must be 1001x1');
assert(isequal(size(results.theta_l), [1001, 1]), 'theta_l must be 1001x1');
assert(all(isfinite(results.theta_m)), 'theta_m must be finite');
assert(all(isfinite(results.theta_l)), 'theta_l must be finite');
fprintf('[PASS] Test 3: Simulation produces correct output dimensions\n');

%% Test 4: Scenario generation
scenarios = generate_probe_scenarios();
assert(numel(scenarios) == 3, 'Must have 3 scenarios');
for i = 1:3
    assert(isfield(scenarios(i), 'id'), 'Scenario must have id');
    assert(isfield(scenarios(i), 'trajectory'), 'Scenario must have trajectory');
    u_test = scenarios(i).trajectory(0);
    assert(isfield(u_test, 'tau_m'), 'Trajectory must output tau_m');
end
fprintf('[PASS] Test 4: Scenario generation produces 3 valid scenarios\n');

fprintf('\nAll plant smoke tests passed!\n');
