function config = observer_default_config()
%OBSERVER_DEFAULT_CONFIG  Default configuration for the augmented EKF observer.
%
%   config = OBSERVER_DEFAULT_CONFIG() returns a struct with the nominal
%   parameters used by the observer. These intentionally differ from the true
%   plant parameters to simulate realistic model mismatch.
%
%   Units:
%       J_m_nom     - Nominal motor inertia          [kg*m^2]
%       J_l_nom     - Nominal load inertia           [kg*m^2]
%       K_s_nom     - Nominal torsional stiffness    [Nm/rad]
%       D_s_nom     - Nominal torsional damping      [Nm*s/rad]
%       N_nom       - Nominal gear ratio             [-]
%       Q           - Process noise covariance       [mixed units]
%       R           - Measurement noise covariance   [mixed units]
%
%   Note:
%       Plant真实参数 != Observer名义参数
%       These nominal parameters are intentionally offset from the true values
%       in flex_joint_default_params.m to simulate realistic model mismatch.
%
%   See also AUGMENTED_EKF_INIT, AUGMENTED_EKF_STEP, FLEX_JOINT_DEFAULT_PARAMS.

    % Nominal dynamic parameters (intentionally mismatched from plant)
    config.J_m_nom = 0.012;         % True: 0.01    (+20% error)
    config.J_l_nom = 0.045;         % True: 0.05    (-10% error)
    config.K_s_nom = 90.0;          % True: 100.0   (-10% error)
    config.D_s_nom = 0.6;           % True: 0.5     (+20% error)
    config.N_nom   = 50.0;          % True: 50.0    (no error)
    
    % Process noise covariance (tuning parameters)
    % State order: [theta_m, omega_m, theta_l, omega_l, tau_ext]
    config.Q = diag([1e-4, 1e-2, 1e-4, 1e-2, 1e-1]);
    
    % Measurement noise covariance
    % Measurement: [theta_m, omega_m]
    config.R = diag([1e-4, 1e-2]);
    
    % Validate
    validate_config(config);
end

function validate_config(config)
%VALIDATE_CONFIG  Validate observer configuration.
    assert(config.J_m_nom > 0, 'J_m_nom must be positive');
    assert(config.J_l_nom > 0, 'J_l_nom must be positive');
    assert(config.K_s_nom > 0, 'K_s_nom must be positive');
    assert(config.D_s_nom >= 0, 'D_s_nom must be non-negative');
    assert(config.N_nom > 0, 'N_nom must be positive');
    
    % Check covariance matrices
    [nQ, mQ] = size(config.Q);
    assert(nQ == 5 && mQ == 5, 'Q must be 5x5');
    assert(issymmetric(config.Q), 'Q must be symmetric');
    assert(all(diag(config.Q) >= 0), 'Q diagonal must be non-negative');
    
    [nR, mR] = size(config.R);
    assert(nR == 2 && mR == 2, 'R must be 2x2');
    assert(issymmetric(config.R), 'R must be symmetric');
    assert(all(diag(config.R) >= 0), 'R diagonal must be non-negative');
end
