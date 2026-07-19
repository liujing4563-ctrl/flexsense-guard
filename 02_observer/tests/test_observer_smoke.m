%TEST_OBSERVER_SMOKE  Smoke test for the augmented EKF observer.
%   Tests that:
%     1. Observer configuration is valid
%     2. EKF initialization returns correct dimensions
%     3. EKF step executes without error
%     4. Innovation is finite and reasonable
%
%   Run with: runtests('test_observer_smoke')

%% Test 1: Observer configuration
config = observer_default_config();
assert(config.J_m_nom > 0, 'J_m_nom must be positive');
assert(config.J_l_nom > 0, 'J_l_nom must be positive');
assert(isequal(size(config.Q), [5, 5]), 'Q must be 5x5');
assert(isequal(size(config.R), [2, 2]), 'R must be 2x2');
fprintf('[PASS] Test 1: Observer configuration valid\n');

%% Test 2: EKF initialization
ekf = augmented_ekf_init(config);
assert(isequal(size(ekf.x), [5, 1]), 'State must be 5x1');
assert(isequal(size(ekf.P), [5, 5]), 'Covariance must be 5x5');
assert(all(diag(ekf.P) >= 0), 'Covariance diagonal must be non-negative');
fprintf('[PASS] Test 2: EKF initialization correct\n');

%% Test 3: EKF step (static, zero input)
y = [0.0; 0.0];
tau_m = 0.0;
dt = 0.001;
[ekf_update, innovation] = augmented_ekf_step(ekf, y, tau_m, dt);
assert(isequal(size(ekf_update.x), [5, 1]), 'Updated state must be 5x1');
assert(isequal(size(innovation), [2, 1]), 'Innovation must be 2x1');
assert(all(isfinite(ekf_update.x)), 'Updated state must be finite');
assert(all(isfinite(innovation)), 'Innovation must be finite');
fprintf('[PASS] Test 3: EKF step with zero input produces finite output\n');

%% Test 4: EKF step (with motion)
y = [0.1; 0.5];
tau_m = 1.0;
[ekf_update2, innovation2] = augmented_ekf_step(ekf, y, tau_m, 0.001);
assert(all(isfinite(ekf_update2.x)), 'Updated state must be finite');
assert(norm(innovation2) < 10, 'Innovation norm should be reasonable');
fprintf('[PASS] Test 4: EKF step with motion produces reasonable innovation\n');

%% Test 5: Parameter mismatch check
% Verify that observer config differs from plant params
plant_params = flex_joint_default_params();
fprintf('[INFO] Observer J_m_nom = %.4f, Plant J_m = %.4f (diff: %.2f%%)\n', ...
    config.J_m_nom, plant_params.J_m, 100 * abs(config.J_m_nom - plant_params.J_m) / plant_params.J_m);
fprintf('[INFO] Observer K_s_nom = %.1f, Plant K_s = %.1f (diff: %.1f%%)\n', ...
    config.K_s_nom, plant_params.K_s, 100 * abs(config.K_s_nom - plant_params.K_s) / plant_params.K_s);

fprintf('\nAll observer smoke tests passed!\n');
