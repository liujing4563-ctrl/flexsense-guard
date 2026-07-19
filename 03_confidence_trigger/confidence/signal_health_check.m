function health = signal_health_check(y, y_prev, tau_m, tau_m_prev, params)
%SIGNAL_HEALTH_CHECK  Check the health status of measured signals.
%
%   health = SIGNAL_HEALTH_CHECK(y, y_prev, tau_m, tau_m_prev, params) evaluates
%   the health of incoming sensor signals and returns flags indicating validity.
%
%   Inputs:
%       y          - Current measurement [theta_m; omega_m]    [rad; rad/s]
%       y_prev     - Previous measurement                      [rad; rad/s]
%       tau_m      - Current motor torque                      [Nm]
%       tau_m_prev - Previous motor torque                     [Nm]
%       params     - Detection parameters:
%           .current_stuck_threshold  - Current change threshold for stuck det.
%           .encoder_stuck_threshold  - Position change threshold for stuck det.
%           .dropout_threshold        - Max expected dropout rate
%
%   Output struct 'health':
%       .current_valid  - Current signal is valid (not stuck, not NaN)  [0/1]
%       .encoder_valid  - Encoder signals are valid (not stuck, not NaN) [0/1]
%       .params_nominal - Parameters are within nominal range           [0/1]
%       .all_valid      - All signals are valid                          [0/1]
%
%   See also CONFIDENCE_SCORE.

    % Default detection parameters
    if nargin < 5 || isempty(params)
        params.current_stuck_threshold = 1e-6;   % Torque change [Nm]
        params.encoder_stuck_threshold = 1e-8;   % Position change [rad]
        params.dropout_threshold = 0.5;            % Max acceptable dropout
    end
    
    % Check for NaN or Inf
    current_valid = all(isfinite([tau_m; y]));
    
    % Check for stuck current signal
    if current_valid
        d_tau = abs(tau_m - tau_m_prev);
        if d_tau < params.current_stuck_threshold
            current_valid = false;
        end
    end
    
    % Check for stuck encoder
    encoder_valid = all(isfinite(y));
    if encoder_valid
        d_theta = abs(y(1) - y_prev(1));
        d_omega = abs(y(2) - y_prev(2));
        if d_theta < params.encoder_stuck_threshold && d_omega < params.encoder_stuck_threshold
            encoder_valid = false;
        end
    end
    
    % Parameter nominal check (flag - simplified for probe)
    params_nominal = true;
    
    % Package
    health.current_valid = double(current_valid);
    health.encoder_valid = double(encoder_valid);
    health.params_nominal = double(params_nominal);
    health.all_valid = double(current_valid && encoder_valid && params_nominal);
end
