# 03 Candidate validation

Phase 1 stub. `python3 03_candidate_validation/validate_candidates.py` exits with a message describing its status.

Independently assess adequacy, grammar, and terminology. Compare idiomaticity and source closeness with blinded, randomized pairs. Allow ties and reject ambiguous pairs.

**TODO** — Judge model, calibration data, and acceptance thresholds.

The Jean Zay command log in [run.sh](run.sh) records the upstream Stage 02 command and its candidate output path. The upstream command is commented so validation can reuse generated candidates. The stage's batch template is [`validate_candidates.slurm`](validate_candidates.slurm).
