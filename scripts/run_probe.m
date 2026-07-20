function results = run_probe()
%RUN_PROBE Run the gated feasibility probe sequence.
%   RESULTS = RUN_PROBE() executes only P1 in this revision. P2 and P3 are
%   intentionally blocked until P1 has a reviewed pass decision.

    fprintf('========================================\n');
    fprintf('FlexSense-Guard feasibility probe\n');
    fprintf('========================================\n\n');

    results.probe1 = run_p1_feasibility_probe();

    if results.probe1.pass
        results.decision = 'inconclusive';
        results.next_action = 'Review P1, then prepare an isolated P2 probe.';
        results.probe2_status = 'not_run_pending_p1_review';
        results.probe3_status = 'not_run_pending_p1_review';
        fprintf('\nP1 passed. P2 and P3 remain blocked pending review.\n');
    else
        results.decision = 'fail';
        results.next_action = 'Downscope to motor-side control simulation.';
        results.probe2_status = 'not_run_p1_failed';
        results.probe3_status = 'not_run_p1_failed';
        fprintf('\nP1 failed. P2 and P3 were not run.\n');
        fprintf('Project decision: %s\n', results.next_action);
    end
end
