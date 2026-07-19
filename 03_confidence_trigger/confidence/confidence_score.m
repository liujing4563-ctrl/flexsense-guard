function score = confidence_score(innovation_norm, signal_health)
%CONFIDENCE_SCORE  Compute a confidence score for the current state estimate.
%
%   score = CONFIDENCE_SCORE(innovation_norm, signal_health) returns a scalar
%   confidence score in [0, 1] indicating how trustworthy the current estimate is.
%
%   Inputs:
%       innovation_norm - L2 norm of the EKF innovation vector      [-]
%       signal_health   - Signal health struct with fields:
%           .current_valid  - Current signal is valid               [0/1]
%           .encoder_valid  - Encoder signal is valid               [0/1]
%           .params_nominal - Parameters within nominal range       [0/1]
%
%   Output:
%       score - Confidence score [0, 1]
%           1.0 = fully confident
%           0.0 = completely untrustworthy
%
%   Algorithm:
%       score = innovation_score * health_score
%       where:
%           innovation_score = exp(-lambda * innovation_norm)
%           health_score     = mean(signal_health fields)
%
%   Note:
%       This is NOT a probability. It is a relative confidence indicator.
%       The score is used for mode switching and trigger decisions, not for
%       statistical inference.
%
%   See also SIGNAL_HEALTH_CHECK, CALIBRATION_TRIGGER.

    % Innovation-based confidence
    lambda = 2.0;  % Sensitivity parameter
    innovation_score = exp(-lambda * innovation_norm);
    
    % Signal health score
    health_values = [signal_health.current_valid;
                     signal_health.encoder_valid;
                     signal_health.params_nominal];
    health_score = mean(health_values);
    
    % Combined score
    score = innovation_score * health_score;
    
    % Clamp to [0, 1]
    score = max(0.0, min(1.0, score));
end
