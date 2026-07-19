function x_dot = flex_joint_dynamics(t, x, u, params)
%FLEX_JOINT_DYNAMICS  State derivative for the two-mass flexible joint model.
%
%   x_dot = FLEX_JOINT_DYNAMICS(t, x, u, params) computes the time derivative
%   of the state vector for a flexible robot joint.
%
%   Inputs:
%       t      - Current time                        [s]
%       x      - State vector [theta_m; omega_m; theta_l; omega_l] 
%                theta_m: motor position             [rad]
%                omega_m: motor velocity             [rad/s]
%                theta_l: load position              [rad]
%                omega_l: load velocity              [rad/s]
%       u      - Control input struct with fields:
%                tau_m: motor torque command         [Nm]
%                tau_ext: external disturbance torque [Nm] (optional, default 0)
%       params - Plant parameter struct (see FLEX_JOINT_DEFAULT_PARAMS)
%
%   Output:
%       x_dot  - State derivative vector [dtheta_m; domega_m; dtheta_l; domega_l]
%
%   Model:
%       J_m * domega_m = tau_m - tau_s - tau_fm
%       J_l * domega_l = tau_s - tau_ext - tau_fl
%       tau_s = K_s * (theta_m/N - theta_l) + D_s * (omega_m/N - omega_l)
%
%   Units:
%       All angles in [rad], velocities in [rad/s], torques in [Nm].
%
%   See also FLEX_JOINT_DEFAULT_PARAMS, SIMULATE_FLEX_JOINT.

    % Validate inputs
    assert(isscalar(t) && isfinite(t), 't must be a finite scalar');
    assert(isnumeric(x) && numel(x) == 4, 'x must be a 4-element numeric vector');
    assert(isstruct(params), 'params must be a struct');
    
    % Parse state vector
    theta_m = x(1);
    omega_m = x(2);
    theta_l = x(3);
    omega_l = x(4);
    
    % Parse control inputs
    tau_m = u.tau_m;
    if isfield(u, 'tau_ext')
        tau_ext = u.tau_ext;
    else
        tau_ext = 0.0;
    end
    
    % Apply torque saturation
    tau_m = max(min(tau_m, params.tau_sat), -params.tau_sat);
    
    % Torsional torque
    theta_m_ref = theta_m / params.N;
    omega_m_ref = omega_m / params.N;
    tau_s = params.K_s * (theta_m_ref - theta_l) + ...
            params.D_s * (omega_m_ref - omega_l);
    
    % Friction torques
    tau_fm = params.tau_fm_c * sign(omega_m) + params.tau_fm_v * omega_m;
    tau_fl = params.tau_fl_c * sign(omega_l) + params.tau_fl_v * omega_l;
    
    % State derivatives
    dtheta_m = omega_m;
    domega_m = (tau_m - tau_s - tau_fm) / params.J_m;
    dtheta_l = omega_l;
    domega_l = (tau_s - tau_ext - tau_fl) / params.J_l;
    
    x_dot = [dtheta_m; domega_m; dtheta_l; domega_l];
end
