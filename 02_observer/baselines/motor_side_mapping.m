function theta_l_est = motor_side_mapping(theta_m, N)
%MOTOR_SIDE_MAPPING  Baseline load position estimate using motor-side mapping.
%
%   theta_l_est = MOTOR_SIDE_MAPPING(theta_m, N) estimates the load position
%   by simply dividing the measured motor position by the gear ratio.
%
%   This is the simplest possible baseline: assuming zero torsional deflection.
%   The true load position will differ from this estimate due to joint flexibility.
%
%   Inputs:
%       theta_m    - Measured motor position          [rad]
%       N          - Gear ratio                       [-]
%
%   Output:
%       theta_l_est - Estimated load position         [rad]
%
%   See also SIMPLE_DISTURBANCE_ESTIMATOR.

    theta_l_est = theta_m / N;
end
