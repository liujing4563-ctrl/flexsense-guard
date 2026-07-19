function scenarios = generate_probe_scenarios()
%GENERATE_PROBE_SCENARIOS  Generate three standard test scenarios for the 72h probe.
%
%   scenarios = GENERATE_PROBE_SCENARIOS() returns a struct array with three
%   scenarios used for feasibility testing:
%
%       scenarios(1) - Normal acceleration/deceleration (sinusoidal tracking)
%       scenarios(2) - Flexible vibration (near-resonant excitation)
%       scenarios(3) - External impact (pulse torque injection)
%
%   Each scenario contains:
%       .id          - Scenario identifier string
%       .trajectory  - Function handle @(t) -> struct with tau_m, tau_ext
%       .sample_time - Sampling time [s]
%       .duration    - Total duration [s]
%       .description - Human-readable description
%
%   Uses the default plant parameters.
%
%   See also SIMULATE_FLEX_JOINT, FLEX_JOINT_DEFAULT_PARAMS.

    params = flex_joint_default_params();
    
    %% Scenario A: Normal acceleration/deceleration
    % Sinusoidal position tracking at moderate speed
    scenarios(1).id = 'nominal_accel_decel';
    scenarios(1).sample_time = 0.001;  % 1 kHz
    scenarios(1).duration = 10.0;      % 10 seconds
    scenarios(1).description = 'Normal acceleration and deceleration with sinusoidal trajectory';
    
    % Simple PD tracking controller for demonstration
    Kp_nominal = 10.0;
    Kd_nominal = 1.0;
    scenarios(1).trajectory = @(t) nominal_trajectory(t, Kp_nominal, Kd_nominal, params);
    
    %% Scenario B: Flexible vibration
    % Trajectory near the resonant frequency to excite torsional vibration
    scenarios(2).id = 'flexible_vibration';
    scenarios(2).sample_time = 0.001;
    scenarios(2).duration = 10.0;
    scenarios(2).description = 'Flexible vibration induced by near-resonant excitation';
    
    % Higher frequency trajectory to excite dynamics
    Kp_vib = 20.0;
    Kd_vib = 0.3;
    scenarios(2).trajectory = @(t) vibration_trajectory(t, Kp_vib, Kd_vib, params);
    
    %% Scenario C: External impact
    % Constant velocity motion with a pulse torque disturbance at t=5s
    scenarios(3).id = 'external_impact';
    scenarios(3).sample_time = 0.001;
    scenarios(3).duration = 10.0;
    scenarios(3).description = 'External impact torque injected at t=5.0s during constant velocity motion';
    
    impact_time = 5.0;
    impact_amplitude = 3.0;  % [Nm]
    Kp_impact = 10.0;
    Kd_impact = 1.0;
    scenarios(3).trajectory = @(t) impact_trajectory(t, impact_time, impact_amplitude, Kp_impact, Kd_impact, params);
    
    % Validate scenarios
    for i = 1:numel(scenarios)
        assert(scenarios(i).sample_time > 0, 'Sample time must be positive');
        assert(scenarios(i).duration > 0, 'Duration must be positive');
        assert(isa(scenarios(i).trajectory, 'function_handle'), 'Trajectory must be a function handle');
    end
end

function u = nominal_trajectory(t, Kp, Kd, params)
%NOMINAL_TRAJECTORY  Sinusoidal tracking with PD control (simplified).
    % Desired trajectory: sinusoidal position
    theta_d = 1.0 * sin(0.5 * t);       % [rad]
    omega_d = 1.0 * 0.5 * cos(0.5 * t); % [rad/s]
    
    % Simplified PD torque (assuming theta_m tracks theta_d * N)
    u.tau_m = Kp * (theta_d * params.N - 0) + Kd * (omega_d * params.N - 0);
    u.tau_ext = 0.0;
end

function u = vibration_trajectory(t, Kp, Kd, params)
%VIBRATION_TRAJECTORY  Higher frequency trajectory near resonant frequency.
    % Desired trajectory: faster sinusoidal to excite vibration
    theta_d = 0.5 * sin(2.0 * t);         % [rad]
    omega_d = 0.5 * 2.0 * cos(2.0 * t);   % [rad/s]
    
    u.tau_m = Kp * (theta_d * params.N - 0) + Kd * (omega_d * params.N - 0);
    u.tau_ext = 0.0;
end

function u = impact_trajectory(t, impact_time, impact_amplitude, Kp, Kd, params)
%IMPACT_TRAJECTORY  Constant velocity with pulse torque at impact_time.
    % Desired trajectory: constant velocity
    speed = 0.5;  % [rad/s]
    theta_d = speed * t;
    omega_d = speed;
    
    % PD torque
    tau_m = Kp * (theta_d * params.N - 0) + Kd * (omega_d * params.N - 0);
    
    % Impact torque: pulse (0.1s width)
    if t >= impact_time && t < impact_time + 0.1
        tau_ext = impact_amplitude;
    else
        tau_ext = 0.0;
    end
    
    u.tau_m = tau_m;
    u.tau_ext = tau_ext;
end
