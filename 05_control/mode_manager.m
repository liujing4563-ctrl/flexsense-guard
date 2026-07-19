function [mode, control_command] = mode_manager(current_mode, confidence_score, contact_score, ...
    classification_result, sensor_health)
%MODE_MANAGER  Determine the operation mode and adjust control command.
%
%   [mode, control_command] = MODE_MANAGER(current_mode, confidence_score, ...
%       contact_score, classification_result, sensor_health) implements the
%   mode switching logic for the flexible joint controller.
%
%   Inputs:
%       current_mode          - Current operation mode string:
%                               'normal', 'vibration_suppression',
%                               'safe_slowdown', 'degraded'
%       confidence_score      - Current confidence score [0, 1]
%       contact_score         - Contact likelihood score [0, 1] (not probability)
%       classification_result - Classification result string:
%                               'normal', 'vibration', 'contact'
%       sensor_health         - Sensor health struct from signal_health_check
%
%   Outputs:
%       mode             - New operation mode string
%       control_command  - Struct with control adjustments:
%           .gain_scale      - Control gain multiplier [0, 1]
%           .velocity_limit  - Max velocity limit     [rad/s]
%           .emergency_stop  - Emergency stop flag    [0/1]
%
%   Mode transition rules:
%       - normal <-> vibration_suppression: based on classification
%       - normal/safe_slowdown: if classification is 'contact'
%       - any -> degraded: if confidence_score < degraded_threshold
%       - degraded -> normal: if confidence recovers above recovery_threshold
%
%   See also CONFIDENCE_SCORE.

    % Default thresholds
    vibration_threshold = 0.6;
    contact_threshold = 0.7;
    degraded_threshold = 0.2;
    recovery_threshold = 0.5;
    
    % Initialize control command
    control_command.gain_scale = 1.0;
    control_command.velocity_limit = inf;
    control_command.emergency_stop = false;
    
    % Check for degraded mode due to low confidence
    if confidence_score < degraded_threshold || ~sensor_health.all_valid
        mode = 'degraded';
        control_command.gain_scale = 0.3;
        control_command.velocity_limit = 0.2;  % [rad/s]
        return;
    end
    
    % If currently degraded, check if recovery is possible
    if strcmp(current_mode, 'degraded') && confidence_score > recovery_threshold
        mode = 'normal';
        return;
    end
    
    % Mode switching based on classification
    switch classification_result
        case 'contact'
            if contact_score > contact_threshold
                mode = 'safe_slowdown';
                control_command.gain_scale = 0.5;
                control_command.velocity_limit = 0.1;
                control_command.emergency_stop = true;
            else
                mode = 'normal';
            end
            
        case 'vibration'
            if contact_score > vibration_threshold
                mode = 'vibration_suppression';
                control_command.gain_scale = 0.7;
                control_command.velocity_limit = 0.5;
            else
                mode = 'normal';
            end
            
        case 'normal'
            mode = 'normal';
            
        otherwise
            mode = current_mode;  % Keep current mode
    end
end
