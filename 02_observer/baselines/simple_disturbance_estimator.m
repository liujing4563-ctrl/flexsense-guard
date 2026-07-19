function tau_ext_est = simple_disturbance_estimator(tau_m, omega_m, domega_m, J_m_nom)
%SIMPLE_DISTURBANCE_ESTIMATOR  Baseline disturbance torque estimator.
%
%   tau_ext_est = SIMPLE_DISTURBANCE_ESTIMATOR(tau_m, omega_m, domega_m, J_m_nom)
%   estimates the external disturbance torque using a simplified momentum-based
%   approach, ignoring torsional dynamics.
%
%   This is a naive baseline: assuming the motor dynamics are dominant and
%   attributing any unexplained torque to external disturbance.
%
%   Formula:
%       tau_ext_est = tau_m - J_m_nom * domega_m - viscous_friction(omega_m)
%
%   Inputs:
%       tau_m     - Motor torque command              [Nm]
%       omega_m   - Motor velocity                    [rad/s]
%       domega_m  - Motor acceleration                [rad/s^2]
%       J_m_nom   - Nominal motor inertia             [kg*m^2]
%
%   Output:
%       tau_ext_est - Estimated external disturbance  [Nm]
%
%   Note:
%       This baseline intentionally ignores the torsional spring dynamics.
%       It will produce poor estimates during significant joint deflection.
%
%   See also MOTOR_SIDE_MAPPING.

    % Simple viscous friction coefficient (assumed)
    B_m = 0.02;  % [Nm*s/rad]
    
    % Friction torque estimate
    tau_friction = B_m * omega_m;
    
    % Disturbance estimate from motor-side momentum balance
    tau_ext_est = tau_m - J_m_nom * domega_m - tau_friction;
end
