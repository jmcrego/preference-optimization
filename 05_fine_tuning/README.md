# 05 Fine-tuning

Phase 1 stub. `python3 05_fine_tuning/run.py` exits with a message describing its status.

Train one shared LoRA adapter for both styles with DPO against a fixed TranslateGemma reference policy.

**TODO** — LoRA and DPO hyperparameters, and reference policy memory strategy on one H100.

Use [run.sh](run.sh) as the Jean Zay command log. The stage's batch template is [`train_dpo.sbatch`](train_dpo.sbatch).

Stage configuration is in [style_dpo.yaml](style_dpo.yaml).
