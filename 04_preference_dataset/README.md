# 04 Preference dataset

Phase 1 stub. `python3 04_preference_dataset/run.py` exits with a message describing its status.

Expand each validated pair into two reversed style-conditioned DPO records in its existing source split. Preserve candidate IDs and validation provenance.

**TODO** — TranslateGemma prompt format after inspection of the actual tokenizer and chat template.

Use [run.sh](run.sh) as the Jean Zay command log. The stage's batch template is [`build_preferences.slurm`](build_preferences.slurm).
