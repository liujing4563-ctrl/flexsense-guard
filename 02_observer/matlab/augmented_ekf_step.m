function [ekf, innovation] = augmented_ekf_step(ekf, y, tau_m, dt)
%AUGMENTED_EKF_STEP  Perform one EKF prediction and update step.
%
%   [ekf, innovation] = AUGMENTED_EKF_STEP(ekf, y, tau_m, dt) runs one cycle
%   of the augmented Extended Kalman Filter.
%
%   Inputs:
%       ekf    - EKF struct from AUGMENTED_EKF_INIT
%       y      - Measurement vector [theta_m; omega_m]    [rad; rad/s]
%       tau_m  - Motor torque command                      [Nm]
%       dt     - Time step                                [s]
%
%   Outputs:
%       ekf        - Updated EKF struct with new state and covariance
%       innovation - Innovation vector (y - y_pred)       [rad; rad/s]
%
%   State transition model:
%       x_pred = f(x, tau_m)  (nonlinear, from flex_joint_dynamics)
%       y_pred = H * x_pred   (linear measurement model)
%
%   Measurement model H:
%       H = [1, 0, 0, 0, 0;   % theta_m measured
%            0, 1, 0, 0, 0]   % omega_m measured
%
%   Units:
%       All angles in [rad], velocities in [rad/s], torques in [Nm].
%
%   See also AUGMENTED_EKF_INIT, OBSERVER_DEFAULT_CONFIG.

    % Validate inputs
    assert(isequal(size(y), [2, 1]), 'y must be a 2x1 vector');
    assert(isscalar(tau_m) && isfinite(tau_m), 'tau_m must be a finite scalar');
    assert(isscalar(dt) && dt > 0, 'dt must be a positive scalar');
    
    % Extract config for convenience
    cfg = ekf.config;
    
    % --- Prediction Step ---
    % State prediction using nominal model
    x_pred = predict_state(ekf.x, tau_m, cfg, dt);
    
    % Linearized state transition matrix (Jacobian)
    F = compute_state_jacobian(ekf.x, cfg, dt);
    
    % Covariance prediction
    P_pred = F * ekf.P * F' + ekf.Q;
    
    % --- Update Step ---
    % Measurement prediction
    H = [1, 0, 0, 0, 0;
         0, 1, 0, 0, 0];
    y_pred = H * x_pred;
    
    % Innovation
    innovation = y - y_pred;
    
    % Innovation covariance
    S = H * P_pred * H' + ekf.R;
    
    % Kalman gain
    K = P_pred * H' / S;
    
    % State update
    ekf.x = x_pred + K * innovation;
    
    % Covariance update (Joseph form for numerical stability)
    I = eye(5);
    ekf.P = (I - K * H) * P_pred * (I - K * H)' + K * ekf.R * K';
    
    % Ensure symmetry
    ekf.P = (ekf.P + ekf.P') / 2;
    
    % Ensure positive definiteness of diagonal
    ekf.P = ekf.P + 1e-12 * eye(5);
end

function x_pred = predict_state(x, tau_m, cfg, dt)
%PREDICT_STATE  Predict next state using nominal model.
%   Uses Euler integration of the nominal dynamics for the augmented state.

    % Current state
    theta_m = x(1);
    omega_m = x(2);
    theta_l = x(3);
    omega_l = x(4);
    tau_ext = x(5);
    
    % Nominal torsional torque
    theta_m_ref = theta_m / cfg.N_nom;
    omega_m_ref = omega_m / cfg.N_nom;
    tau_s_nom = cfg.K_s_nom * (theta_m_ref - theta_l) + ...
                cfg.D_s_nom * (omega_m_ref - omega_l);
    
    % Nominal friction (simplified, viscous only for observer)
    tau_fm_nom = cfg.D_s_nom * 0.1 * omega_m;  % Simplified friction
    tau_fl_nom = cfg.D_s_nom * 0.05 * omega_l;  % Simplified friction
    
    % Derivatives with nominal parameters
    dtheta_m = omega_m;
    domega_m = (tau_m - tau_s_nom - tau_fm_nom) / cfg.J_m_nom;
    dtheta_l = omega_l;
    domega_l = (tau_s_nom - tau_ext - tau_fl_nom) / cfg.J_l_nom;
    dtau_ext = 0.0;  % Random walk model
    
    % Euler integration
    x_pred = x + dt * [dtheta_m; domega_m; dtheta_l; domega_l; dtau_ext];
end

function F = compute_state_jacobian(x, cfg, dt)
%COMPUTE_STATE_JACOBIAN  Compute linearized state transition matrix.
%   F = I + df/dx * dt where df/dx is the Jacobian of the continuous-time dynamics.

    % Partial derivatives of the augmented dynamics
    % f(x) = [omega_m;
    %         (tau_m - tau_s - tau_fm) / J_m;
    %         omega_l;
    %         (tau_s - tau_ext - tau_fl) / J_l;
    %         0]
    %
    % where tau_s = K_s * (theta_m/N - theta_l) + D_s * (omega_m/N - omega_l)

    J_m = cfg.J_m_nom;
    J_l = cfg.J_l_nom;
    K_s = cfg.K_s_nom;
    D_s = cfg.D_s_nom;
    N = cfg.N_nom;
    
    % df/dx continuous-time Jacobian
    A = zeros(5, 5);
    
    % d(dtheta_m)/dx
    A(1, 2) = 1;  % d(omega_m)/d(omega_m)
    
    % d(domega_m)/dx
    A(2, 1) = -K_s / (J_m * N);    % d(tau_s)/d(theta_m) / J_m
    A(2, 2) = -D_s / (J_m * N) - 0.1*D_s/J_m;  % d(tau_s + friction)/d(omega_m)
    A(2, 3) = K_s / J_m;            % d(tau_s)/d(theta_l) / J_m
    A(2, 4) = D_s / J_m;            % d(tau_s)/d(omega_l) / J_m
    
    % d(dtheta_l)/dx
    A(3, 4) = 1;  % d(omega_l)/d(omega_l)
    
    % d(domega_l)/dx
    A(4, 1) = K_s / (J_l * N);     % d(tau_s)/d(theta_m) / J_l
    A(4, 2) = D_s / (J_l * N);     % d(tau_s)/d(omega_m) / J_l
    A(4, 3) = -K_s / J_l;          % d(tau_s)/d(theta_l) / J_l
    A(4, 4) = -D_s / J_l - 0.05*D_s/J_l;  % d(tau_s + friction)/d(omega_l)
    A(4, 5) = -1 / J_l;            % d(tau_ext)/d(tau_ext)
    
    % Discrete-time approximation: F = I + A * dt
    F = eye(5) + A * dt;
end
