function [decision, new_state] = update_gate(ekf_current, ekf_candidate, confidence_current, confidence_candidate, config)
%UPDATE_GATE  Gate logic for accepting, holding, or rolling back state estimates.
%
%   [decision, new_state] = UPDATE_GATE(ekf_current, ekf_candidate, ...
%       confidence_current, confidence_candidate, config) implements the
%   update gate logic: accept / hold / rollback.
%
%   Inputs:
%       ekf_current         - Current active EKF state
%       ekf_candidate       - Candidate new EKF state (e.g., after calibration)
%       confidence_current  - Confidence score of current state [0, 1]
%       confidence_candidate- Confidence score of candidate state [0, 1]
%       config              - Gate configuration:
%           .accept_threshold    - Min confidence to accept update
%           .rollback_threshold  - Confidence below which to rollback
%
%   Outputs:
%       decision  - 'accept', 'hold', or 'rollback'
%       new_state - The EKF state to use after gate decision
%
%   See also CONFIDENCE_SCORE, CALIBRATION_TRIGGER.

    % Default config
    if nargin < 5 || isempty(config)
        config.accept_threshold = 0.6;
        config.rollback_threshold = 0.2;
    end
    
    if confidence_candidate > config.accept_threshold && ...
       confidence_candidate >= confidence_current
        % Accept candidate - it's better than current
        decision = 'accept';
        new_state = ekf_candidate;
        
    elseif confidence_current < config.rollback_threshold
        % Rollback - current state is too unreliable
        decision = 'rollback';
        % Reset to a safe initial state
        new_state = ekf_current;  % In practice, restore from backup
        new_state.x = new_state.x * 0;  % Reset to zero
        new_state.P = diag([1e-2, 1e-2, 1e-1, 1e-1, 1.0]);
        
    else
        % Hold - keep current state
        decision = 'hold';
        new_state = ekf_current;
    end
end
