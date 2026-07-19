function results = simulate_flex_joint(trajectory_fn, params, sample_time_s, duration_s, varargin)
%SIMULATE_FLEX_JOINT  Simulate the flexible joint plant over a time span.
%
%   results = SIMULATE_FLEX_JOINT(trajectory_fn, params, sample_time_s, duration_s)
%   performs a time-domain simulation of the flexible joint model.
%
%   Inputs:
%       trajectory_fn - Function handle @(t) -> struct with fields:
%                       tau_m: motor torque command       [Nm]
%                       tau_ext: external disturbance     [Nm] (optional)
%       params        - Plant parameter struct
%       sample_time_s - Sampling time                    [s]
%       duration_s    - Simulation duration              [s]
%
%   Optional name-value pairs:
%       'encoder_dropout_rate' - Probability of encoder dropout  [0,1]
%       'current_noise_std'    - Current measurement noise std   [A]
%       'random_seed'          - Random seed for reproducibility
%
%   Output struct 'results':
%       .t             - Time vector                          [s]
%       .theta_m       - Motor position (measured)            [rad]
%       .omega_m       - Motor velocity (measured)            [rad/s]
%       .theta_l       - Load position (ground truth, NOT for observer) [rad]
%       .omega_l       - Load velocity (ground truth, NOT for observer) [rad/s]
%       .tau_ext_true  - External torque (ground truth)       [Nm]
%       .tau_s         - Torsional torque                     [Nm]
%       .tau_m         - Motor torque command                 [Nm]
%       .valid_flag    - Measurement validity flag            [-]
%
%   Units: rad, rad/s, Nm, s.
%
%   See also FLEX_JOINT_DYNAMICS, FLEX_JOINT_DEFAULT_PARAMS.

    % Parse optional inputs
    p = inputParser;
    addParameter(p, 'encoder_dropout_rate', 0.0, @(x) isnumeric(x) && x >= 0 && x <= 1);
    addParameter(p, 'current_noise_std', 0.0, @(x) isnumeric(x) && x >= 0);
    addParameter(p, 'random_seed', 0, @(x) isnumeric(x) && isscalar(x));
    parse(p, varargin{:});
    
    encoder_dropout_rate = p.Results.encoder_dropout_rate;
    current_noise_std = p.Results.current_noise_std;
    random_seed = p.Results.random_seed;
    
    % Set random seed for reproducibility
    if random_seed > 0
        rng(random_seed);
    end
    
    % Simulation parameters
    N_steps = round(duration_s / sample_time_s);
    t = (0:N_steps)' * sample_time_s;
    
    % Preallocate
    nx = 4;  % theta_m, omega_m, theta_l, omega_l
    x = zeros(nx, N_steps + 1);
    tau_s_vec = zeros(N_steps + 1, 1);
    tau_m_vec = zeros(N_steps + 1, 1);
    tau_ext_true_vec = zeros(N_steps + 1, 1);
    valid_flag = true(N_steps + 1, 1);
    
    % Initial condition (at rest)
    x(:, 1) = [0; 0; 0; 0];
    
    % Euler integration (simple, adequate for probe)
    for k = 1:N_steps
        % Get control input from trajectory function
        u = trajectory_fn(t(k));
        
        tau_m_cmd = u.tau_m;
        if isfield(u, 'tau_ext')
            tau_ext_cmd = u.tau_ext;
        else
            tau_ext_cmd = 0.0;
        end
        
        % Save true values (for evaluation only)
        tau_m_vec(k) = tau_m_cmd;
        tau_ext_true_vec(k) = tau_ext_cmd;
        
        % Add current measurement noise
        tau_m_meas = tau_m_cmd + current_noise_std * randn();
        
        % State derivative
        u_struct.tau_m = tau_m_meas;
        u_struct.tau_ext = tau_ext_cmd;
        x_dot = flex_joint_dynamics(t(k), x(:, k), u_struct, params);
        
        % Euler step
        x(:, k + 1) = x(:, k) + sample_time_s * x_dot;
        
        % Compute torsional torque for output
        theta_m_ref = x(1, k) / params.N;
        omega_m_ref = x(2, k) / params.N;
        tau_s_vec(k) = params.K_s * (theta_m_ref - x(3, k)) + ...
                       params.D_s * (omega_m_ref - x(4, k));
        
        % Encoder dropout simulation
        if rand() < encoder_dropout_rate
            valid_flag(k) = false;
        end
    end
    
    % Compute final step tau_s
    theta_m_ref = x(1, end) / params.N;
    omega_m_ref = x(2, end) / params.N;
    tau_s_vec(end) = params.K_s * (theta_m_ref - x(3, end)) + ...
                     params.D_s * (omega_m_ref - x(4, end));
    
    % Package results
    results.t = t;
    results.theta_m = x(1, :)';
    results.omega_m = x(2, :)';
    results.theta_l = x(3, :)';
    results.omega_l = x(4, :)';
    results.tau_ext_true = tau_ext_true_vec;
    results.tau_s = tau_s_vec;
    results.tau_m = tau_m_vec;
    results.valid_flag = valid_flag;
end
