# 06 Evaluation

Phase 1 stub. `python3 06_evaluation/evaluate.py` exits with a message describing its status.

Compare base and adapted models on held-out sources. Assess style-switch success and whether idiomatic naturalness and translation quality are preserved.

**TODO** — Judge, metric versions, decoding settings, and human annotation protocol.

Evaluation settings are in [style_evaluation.yaml](style_evaluation.yaml).

The Jean Zay command log in [run.sh](run.sh) records the Stage 05 fine-tuning command. The upstream command is commented so this stage can reuse existing artifacts. The stage's batch template is [`evaluate.slurm`](evaluate.slurm).
