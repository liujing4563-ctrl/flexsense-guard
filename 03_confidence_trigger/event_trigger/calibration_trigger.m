function [trigger, reason] = calibration_trigger(confidence_score, last_calibration_time, current_time, config)
%CALIBRATION_TRIGGER  Determine whether a low-amplitude calibration should be triggered.
%
%   [trigger, reason] = CALIBRATION_TRIGGER(confidence_score, last_calibration_time, current_time, config)
%   evaluates whether conditions are met to inject a calibration signal.
%
%   Inputs:
%       confidence_score      - Current confidence score [0, 1]
%       last_calibration_time - Time of last calibration  [s]
%       current_time          - Current simulation time   [s]
%       config                - Trigger configuration:
%           .threshold         - Confidence threshold to trigger  [-]
%           .cooldown_period   - Minimum time between calibrations [s]
%
%   Outputs:
%       trigger - true if calibration should be triggered
%       reason  - String describing the trigger reason
%
%   See also CONFIDENCE_SCORE, UPDATE_GATE.

    % Default config
    if nargin < 4 || isempty(config)
        config.threshold = 0.3;
        config.cooldown_period = 2.0;  % seconds
    end
    
    % Check cooldown
    time_since_last = current_time - last_calibration_time;
    if time_since_last < config.cooldown_period
        trigger = false;
        reason = 'Cooldown period not elapsed';
        return;
    end
    
    % Check confidence threshold
    if confidence_score < config.threshold
        trigger = true;
        reason = sprintf('Confidence score %.2f below threshold %.2f', ...
            confidence_score, config.threshold);
    else
        trigger = false;
        reason = 'Confidence score above threshold';
    end
end
