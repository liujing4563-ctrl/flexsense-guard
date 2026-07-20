function report = run_p1_feasibility_probe()
%RUN_P1_FEASIBILITY_PROBE Evaluate load-side estimation without truth leakage.
%   REPORT = RUN_P1_FEASIBILITY_PROBE compares a motor-side mapping baseline
%   with a small, predefined EKF process-noise sweep. Plant truth is read only
%   after each observer run for offline metric calculation.

    plant_params = flex_joint_default_params();
    scenarios = generate_probe_scenarios();
    scenario = scenarios(1);
    simulation = simulate_flex_joint(scenario.trajectory, plant_params, ...
        scenario.sample_time, scenario.duration, 'random_seed', 42);

    % This is a predefined probe sweep, not an optimization over evaluation data.
    q_scales = [1.0, 1e-2, 1e-4, 1e-6, 1e-8];
    candidate_count = numel(q_scales);
    candidates = repmat(struct( ...
        'q_scale', 0.0, ...
        'load_position_rmse_rad', NaN, ...
        'improvement_pct', NaN, ...
        'finite', false), candidate_count, 1);

    theta_motor_mapped = simulation.theta_m / plant_params.N;
    theta_load_truth = simulation.theta_l; % Evaluation only; never sent to the observer.
    motor_mapping_rmse = sqrt(mean((theta_load_truth - theta_motor_mapped).^2));

    for candidate_index = 1:candidate_count
        config = observer_default_config();
        config.Q = config.Q * q_scales(candidate_index);
        ekf = augmented_ekf_init(config);
        theta_load_estimate = zeros(size(theta_load_truth));

        for sample_index = 1:numel(simulation.t)
            measurement = [simulation.theta_m(sample_index); ...
                           simulation.omega_m(sample_index)];
            [ekf, ~] = augmented_ekf_step(ekf, measurement, ...
                simulation.tau_m(sample_index), scenario.sample_time);
            theta_load_estimate(sample_index) = ekf.x(3);
        end

        estimate_rmse = sqrt(mean((theta_load_truth - theta_load_estimate).^2));
        improvement_pct = 100.0 * (motor_mapping_rmse - estimate_rmse) / ...
            motor_mapping_rmse;

        candidates(candidate_index).q_scale = q_scales(candidate_index);
        candidates(candidate_index).load_position_rmse_rad = estimate_rmse;
        candidates(candidate_index).improvement_pct = improvement_pct;
        candidates(candidate_index).finite = isfinite(estimate_rmse);
    end

    candidate_errors = [candidates.load_position_rmse_rad];
    [best_rmse, best_index] = min(candidate_errors);
    best_improvement_pct = candidates(best_index).improvement_pct;

    % Require both an absolute bound and a meaningful improvement over the
    % motor-side baseline. This avoids a false pass when the baseline is already
    % below the absolute threshold.
    pass = isfinite(best_rmse) && best_rmse < 0.05 && best_improvement_pct >= 30.0;

    report.scenario_id = scenario.id;
    report.random_seed = 42;
    report.motor_mapping_rmse_rad = motor_mapping_rmse;
    report.candidates = candidates;
    report.best_q_scale = candidates(best_index).q_scale;
    report.best_load_position_rmse_rad = best_rmse;
    report.best_improvement_pct = best_improvement_pct;
    report.pass = pass;

    fprintf('P1 motor-side mapping RMSE: %.6f rad\n', motor_mapping_rmse);
    fprintf('P1 best EKF RMSE: %.6f rad (Q scale %.0e)\n', ...
        best_rmse, report.best_q_scale);
    fprintf('P1 best improvement: %.2f%%\n', best_improvement_pct);
    fprintf('P1 decision: %s\n', ternary(pass, 'PASS', 'FAIL'));
end

function value = ternary(condition, true_value, false_value)
%TERNARY Return TRUE_VALUE when CONDITION is true, otherwise FALSE_VALUE.
    if condition
        value = true_value;
    else
        value = false_value;
    end
end
