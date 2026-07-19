function ekf = augmented_ekf_init(config)
%AUGMENTED_EKF_INIT  Initialize the augmented EKF observer.
%
%   ekf = AUGMENTED_EKF_INIT(config) creates and initializes the EKF struct
%   with the nominal observer configuration.
%
%   Input:
%       config - Observer configuration struct (see OBSERVER_DEFAULT_CONFIG)
%
%   Output struct 'ekf':
%       .x     - State vector [theta_m; omega_m; theta_l; omega_l; tau_ext]
%                Units: [rad; rad/s; rad; rad/s; Nm]
%       .P     - State covariance matrix (5x5)
%       .Q     - Process noise covariance (5x5)
%       .R     - Measurement noise covariance (2x2)
%       .config - Copy of observer config
%
%   State vector:
%       x[1] = theta_m : motor position             [rad]
%       x[2] = omega_m : motor velocity             [rad/s]
%       x[3] = theta_l : load position              [rad]
%       x[4] = omega_l : load velocity              [rad/s]
%       x[5] = tau_ext : external disturbance torque [Nm]
%
%   Measurement:
%       y = [theta_m; omega_m]  (motor side only!)
%
%   Note:
%       The tau_ext state is modeled as a random walk (d(tau_ext)/dt = 0 + noise)
%       in the prediction step. This is a simplification; a more sophisticated
%       model can be substituted later.
%
%   See also AUGMENTED_EKF_STEP, OBSERVER_DEFAULT_CONFIG.

    % Initialize state (all zeros - at rest)
    ekf.x = zeros(5, 1);
    
    % Initial covariance (moderate uncertainty)
    ekf.P = diag([1e-2, 1e-2, 1e-1, 1e-1, 1.0]);
    
    % Noise covariances from config
    ekf.Q = config.Q;
    ekf.R = config.R;
    
    % Store config
    ekf.config = config;
    
    % Validate
    assert(isequal(size(ekf.x), [5, 1]), 'State vector must be 5x1');
    assert(isequal(size(ekf.P), [5, 5]), 'Covariance must be 5x5');
    assert(all(diag(ekf.P) >= 0), 'Covariance diagonal must be non-negative');
end
