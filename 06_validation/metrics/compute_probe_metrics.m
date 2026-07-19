function metrics = compute_probe_metrics(theta_true, theta_est, omega_true, omega_est, ...
    tau_ext_true, tau_ext_est, detections, ground_truth_contact)
%COMPUTE_PROBE_METRICS  Compute standardized metrics for probe evaluation.
%
%   metrics = COMPUTE_PROBE_METRICS(theta_true, theta_est, ...) computes
%   evaluation metrics comparing estimated values to ground truth.
%
%   Inputs:
%       theta_true          - True load position              [rad]
%       theta_est           - Estimated load position         [rad]
%       omega_true          - True load velocity              [rad/s]
%       omega_est           - Estimated load velocity         [rad/s]
%       tau_ext_true        - True external torque            [Nm]
%       tau_ext_est         - Estimated external torque       [Nm]
%       detections          - Binary detection signal         [0/1]
%       ground_truth_contact- Binary ground truth contact     [0/1]
%
%   Output struct 'metrics':
%       .load_position_rmse  - RMSE of load position         [rad]
%       .load_velocity_rmse  - RMSE of load velocity         [rad/s]
%       .external_torque_rmse- RMSE of external torque       [Nm]
%       .false_alarm_count   - Number of false alarms        [-]
%       .missed_detection_count - Number of missed detections[-]
%
%   See also RUN_PROBE.

    % RMSE calculations
    metrics.load_position_rmse = sqrt(mean((theta_true - theta_est).^2));
    metrics.load_velocity_rmse = sqrt(mean((omega_true - omega_est).^2));
    metrics.external_torque_rmse = sqrt(mean((tau_ext_true - tau_ext_est).^2));
    
    % Detection statistics (if ground truth contact labels exist)
    if nargin >= 8 && ~isempty(ground_truth_contact)
        % Ensure logical
        detections = logical(detections);
        ground_truth_contact = logical(ground_truth_contact);
        
        % False alarms: detected but no contact
        metrics.false_alarm_count = sum(detections & ~ground_truth_contact);
        
        % Missed detections: contact but not detected
        metrics.missed_detection_count = sum(~detections & ground_truth_contact);
        
        % Total contacts
        metrics.total_contact_count = sum(ground_truth_contact);
    else
        metrics.false_alarm_count = NaN;
        metrics.missed_detection_count = NaN;
        metrics.total_contact_count = NaN;
    end
end
