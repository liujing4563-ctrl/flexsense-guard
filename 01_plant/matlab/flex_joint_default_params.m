function params = flex_joint_default_params()
%FLEX_JOINT_DEFAULT_PARAMS  Default parameters for the flexible joint plant.
%
%   params = FLEX_JOINT_DEFAULT_PARAMS() returns a struct with the default
%   physical parameters for the two-mass flexible joint model.
%
%   Units:
%       J_m        - Motor inertia              [kg*m^2]
%       J_l        - Load inertia               [kg*m^2]
%       K_s        - Torsional stiffness        [Nm/rad]
%       D_s        - Torsional damping          [Nm*s/rad]
%       N          - Gear ratio                 [-]
%       tau_fm_c   - Motor Coulomb friction     [Nm]
%       tau_fm_v   - Motor viscous friction     [Nm*s/rad]
%       tau_fl_c   - Load Coulomb friction      [Nm]
%       tau_fl_v   - Load viscous friction      [Nm*s/rad]
%       tau_sat    - Torque saturation limit    [Nm]
%       delay_s    - Measurement delay          [s]
%
%   See also FLEX_JOINT_DYNAMICS, SIMULATE_FLEX_JOINT.

    % Motor inertia
    params.J_m = 0.01;          % [kg*m^2]
    
    % Load inertia
    params.J_l = 0.05;          % [kg*m^2]
    
    % Torsional spring constant
    params.K_s = 100.0;         % [Nm/rad]
    
    % Torsional damping coefficient
    params.D_s = 0.5;           % [Nm*s/rad]
    
    % Gear ratio
    params.N = 50.0;            % [-]
    
    % Motor friction: Coulomb
    params.tau_fm_c = 0.05;     % [Nm]
    
    % Motor friction: Viscous
    params.tau_fm_v = 0.01;     % [Nm*s/rad]
    
    % Load friction: Coulomb
    params.tau_fl_c = 0.02;     % [Nm]
    
    % Load friction: Viscous
    params.tau_fl_v = 0.005;    % [Nm*s/rad]
    
    % Torque saturation limit
    params.tau_sat = 5.0;       % [Nm]
    
    % Measurement delay (applied as integer step delay)
    params.delay_s = 0.001;     % [s]
    
    % Validate parameters
    validate_params(params);
end

function validate_params(params)
%VALIDATE_PARAMS  Validate that all parameters are physically meaningful.
    
    assert(params.J_m > 0, 'J_m must be positive');
    assert(params.J_l > 0, 'J_l must be positive');
    assert(params.K_s > 0, 'K_s must be positive');
    assert(params.D_s >= 0, 'D_s must be non-negative');
    assert(params.N > 0, 'N must be positive');
    assert(params.tau_sat > 0, 'tau_sat must be positive');
    assert(params.delay_s >= 0, 'delay_s must be non-negative');
    
    % Check for NaN or Inf
    fields = fieldnames(params);
    for i = 1:numel(fields)
        value = params.(fields{i});
        if ~isa(value, 'function_handle')
            assert(isfinite(value), 'Parameter %s must be finite', fields{i});
        end
    end
end
