function setup_project()
%SETUP_PROJECT  Add all module paths to MATLAB/Octave search path.
%
%   SETUP_PROJECT() adds the necessary directories to the MATLAB path so that
%   all project functions are accessible. Run this once at the start of each
%   session.
%
%   Usage:
%       >> setup_project
%
%   See also RUN_PROBE.

    % Get the root directory of the project
    root_dir = fileparts(mfilename('fullpath'));
    root_dir = fileparts(root_dir);  % Go up from scripts/ to root

    % Define all module paths
    module_paths = {
        fullfile(root_dir, '01_plant', 'matlab');
        fullfile(root_dir, '01_plant', 'tests');
        fullfile(root_dir, '02_observer', 'matlab');
        fullfile(root_dir, '02_observer', 'baselines');
        fullfile(root_dir, '02_observer', 'tests');
        fullfile(root_dir, '03_confidence_trigger', 'confidence');
        fullfile(root_dir, '03_confidence_trigger', 'event_trigger');
        fullfile(root_dir, '03_confidence_trigger', 'rollback');
        fullfile(root_dir, '05_control');
        fullfile(root_dir, '06_validation', 'metrics');
        fullfile(root_dir, 'scripts');
    };

    % Add paths
    for i = 1:numel(module_paths)
        if exist(module_paths{i}, 'dir')
            addpath(module_paths{i});
            fprintf('Added: %s\n', module_paths{i});
        else
            warning('Directory not found: %s', module_paths{i});
        end
    end

    fprintf('\nFlexSense-Guard project setup complete.\n');
    fprintf('Run >> run_probe  to execute the 72h feasibility probes.\n');
end
