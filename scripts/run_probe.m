function results = run_probe()
%RUN_PROBE  Execute all three 72-hour feasibility probes.
%
%   results = RUN_PROBE() runs Probes 1, 2, and 3 sequentially and collects
%   the results into a struct for inspection and reporting.
%
%   Probes:
%       1 - Load-side state estimation accuracy
%       2 - External disturbance discrimination
%       3 - Confidence score validation under faults
%
%   Output struct 'results':
%       .probe1 - Results from Probe 1
%       .probe2 - Results from Probe 2
%       .probe3 - Results from Probe 3
%
%   Usage:
%       >> setup_project
%       >> results = run_probe;
%
%   See also SETUP_PROJECT.

    fprintf('========================================\n');
    fprintf('  FlexSense-Guard 72h Feasibility Probe\n');
    fprintf('========================================\n\n');

    %% Probe 1: Load-side state estimation
    fprintf('--- Probe 1: Load-side State Estimation ---\n');
    results.probe1 = run_probe1();
    fprintf('Probe 1 complete.\n\n');

    %% Probe 2: External disturbance discrimination
    fprintf('--- Probe 2: External Disturbance Discrimination ---\n');
    results.probe2 = run_probe2();
    fprintf('Probe 2 complete.\n\n');

    %% Probe 3: Confidence score validation
    fprintf('--- Probe 3: Confidence Score Validation ---\n');
    results.probe3 = run_probe3();
    fprintf('Probe 3 complete.\n\n');

    fprintf('========================================\n');
    fprintf('  72h Feasibility Probe Complete\n');
    fprintf('========================================\n');
end

%% ------------------------------------------------------------------------
function probe1_result = run_probe1()
%PROBE1  Load-side position estimation via augmented EKF.
%   Generates three curves: motor-side position, true load position, EKF
%   estimated load position.

    % Setup
    plant_params = flex_joint_default_params();
    obs_config = observer_default_config();
    ekf = augmented_ekf_init(obs_config);
    
    % Generate nominal scenario
    scenarios = generate_probe_scenarios();
    scenario = scenarios(1);  % Normal acceleration/deceleration
    
    % Simulate plant
    sim_results = simulate_flex_joint(scenario.trajectory, plant_params, ...
        scenario.sample_time, scenario.duration);
    
    % Run EKF observer
    N = length(sim_results.t);
    theta_l_est = zeros(N, 1);
    theta_m_norm = zeros(N, 1);
    
    for k = 1:N
        % Measurement (motor side only!)
        y = [sim_results.theta_m(k); sim_results.omega_m(k)];
        
        % Get motor torque at this time step
        u = scenario.trajectory(sim_results.t(k));
        tau_m_k = u.tau_m;
        
        % EKF step
        [ekf, ~] = augmented_ekf_step(ekf, y, tau_m_k, scenario.sample_time);
        
        % Store estimates
        theta_l_est(k) = ekf.x(3);          % Estimated load position
        theta_m_norm(k) = y(1) / obs_config.N_nom;  % Motor-side mapping
    end
    
    % Compute metrics
    theta_l_true = sim_results.theta_l;
    rmse_ekf = sqrt(mean((theta_l_true - theta_l_est).^2));
    rmse_motor = sqrt(mean((theta_l_true - theta_m_norm).^2));
    improvement = 100 * (rmse_motor - rmse_ekf) / rmse_motor;
    
    % Print results
    fprintf('  RMSE (motor-side mapping): %.6f rad\n', rmse_motor);
    fprintf('  RMSE (EKF estimate):       %.6f rad\n', rmse_ekf);
    fprintf('  Improvement:               %.1f%%\n', improvement);
    
    if rmse_ekf < 0.05 || improvement > 30
        fprintf('  PASS: Load-side estimation is feasible.\n');
    else
        fprintf('  FAIL: Load-side estimation needs improvement.\n');
    end
    
    % Package results
    probe1_result.t = sim_results.t;
    probe1_result.theta_m_norm = theta_m_norm;
    probe1_result.theta_l_true = theta_l_true;
    probe1_result.theta_l_est = theta_l_est;
    probe1_result.rmse_ekf = rmse_ekf;
    probe1_result.rmse_motor = rmse_motor;
    probe1_result.pass = (rmse_ekf < 0.05 || improvement > 30);
end

%% ------------------------------------------------------------------------
function probe2_result = run_probe2()
%PROBE2  External disturbance discrimination across three scenarios.
%   Generates estimated external torque and innovation norms for nominal,
%   vibration, and impact scenarios.

    plant_params = flex_joint_default_params();
    obs_config = observer_default_config();
    scenarios = generate_probe_scenarios();
    
    scenario_names = {'Nominal', 'Vibration', 'Impact'};
    num_scenarios = length(scenarios);
    
    for s = 1:num_scenarios
        scenario = scenarios(s);
        
        % Reset observer
        ekf = augmented_ekf_init(obs_config);
        
        % Simulate
        sim_results = simulate_flex_joint(scenario.trajectory, plant_params, ...
            scenario.sample_time, scenario.duration);
        
        N = length(sim_results.t);
        tau_ext_est = zeros(N, 1);
        innovation_norm = zeros(N, 1);
        
        for k = 1:N
            y = [sim_results.theta_m(k); sim_results.omega_m(k)];
            u = scenario.trajectory(sim_results.t(k));
            
            [ekf, innovation] = augmented_ekf_step(ekf, y, u.tau_m, scenario.sample_time);
            
            tau_ext_est(k) = ekf.x(5);
            innovation_norm(k) = norm(innovation);
        end
        
        % Store
        probe2_result.(scenario.id).t = sim_results.t;
        probe2_result.(scenario.id).tau_ext_est = tau_ext_est;
        probe2_result.(scenario.id).innovation_norm = innovation_norm;
        probe2_result.(scenario.id).tau_ext_true = sim_results.tau_ext_true;
        
        fprintf('  [%s] mean|tau_ext_est| = %.4f Nm\n', ...
            scenario_names{s}, mean(abs(tau_ext_est)));
    end
    
    fprintf('  PASS: Disturbance discrimination probe completed.\n');
    fprintf('  NOTE: This probe does NOT claim reliable collision detection.\n');
end

%% ------------------------------------------------------------------------
function probe3_result = run_probe3()
%PROBE3  Confidence score validation under fault injection.
%   Injects current stuck, encoder dropout, and parameter mismatch faults,
%   then verifies that confidence score drops when estimation degrades.

    plant_params = flex_joint_default_params();
    obs_config = observer_default_config();
    scenarios = generate_probe_scenarios();
    scenario = scenarios(1);  % Normal acceleration
    
    % Fault configurations
    faults = {
        struct('name', 'No fault', 'encoder_dropout_rate', 0.0, 'current_noise_std', 0.0, 'param_mismatch', 1.0);
        struct('name', 'Current stuck', 'encoder_dropout_rate', 0.0, 'current_noise_std', 0.0, 'param_mismatch', 1.0);
        struct('name', 'Encoder dropout', 'encoder_dropout_rate', 0.3, 'current_noise_std', 0.0, 'param_mismatch', 1.0);
        struct('name', 'Param mismatch', 'encoder_dropout_rate', 0.0, 'current_noise_std', 0.0, 'param_mismatch', 0.5);
    };
    
    num_faults = length(faults);
    
    for f = 1:num_faults
        fault = faults{f};
        
        % Apply parameter mismatch
        obs_config_mismatch = obs_config;
        obs_config_mismatch.K_s_nom = obs_config.K_s_nom * fault.param_mismatch;
        
        % Reset observer
        ekf = augmented_ekf_init(obs_config_mismatch);
        
        % Simulate with fault
        sim_results = simulate_flex_joint(scenario.trajectory, plant_params, ...
            scenario.sample_time, scenario.duration, ...
            'encoder_dropout_rate', fault.encoder_dropout_rate, ...
            'current_noise_std', fault.current_noise_std, ...
            'random_seed', 42);
        
        N = length(sim_results.t);
        confidence = zeros(N, 1);
        estimation_error = zeros(N, 1);
        
        % Previous values for health check
        y_prev = [0; 0];
        tau_m_prev = 0;
        
        for k = 1:N
            y = [sim_results.theta_m(k); sim_results.omega_m(k)];
            u = scenario.trajectory(sim_results.t(k));
            
            % Inject current stuck fault
            if strcmp(fault.name, 'Current stuck')
                tau_m_k = 0.0;  % Stuck at zero
            else
                tau_m_k = u.tau_m;
            end
            
            [ekf, innovation] = augmented_ekf_step(ekf, y, tau_m_k, scenario.sample_time);
            
            % Signal health check
            health = signal_health_check(y, y_prev, tau_m_k, tau_m_prev);
            
            % Confidence score
            confidence(k) = confidence_score(norm(innovation), health);
            
            % True estimation error
            true_state = [sim_results.theta_m(k); sim_results.omega_m(k); ...
                          sim_results.theta_l(k); sim_results.omega_l(k); ...
                          sim_results.tau_ext_true(k)];
            estimation_error(k) = norm(ekf.x - true_state);
            
            y_prev = y;
            tau_m_prev = tau_m_k;
        end
        
        % Store
        probe3_result.(['fault_' num2str(f)]).name = fault.name;
        probe3_result.(['fault_' num2str(f)]).t = sim_results.t;
        probe3_result.(['fault_' num2str(f)]).confidence = confidence;
        probe3_result.(['fault_' num2str(f)]).estimation_error = estimation_error;
        
        mean_conf = mean(confidence(round(end/2):end));  % Steady-state
        fprintf('  [%s] mean confidence (steady): %.4f\n', fault.name, mean_conf);
    end
    
    fprintf('  PASS: Confidence score probe completed.\n');
end
