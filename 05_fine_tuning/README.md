# 05 Fine-tuning

Phase 1 stub. `python3 05_fine_tuning/train_dpo.py` exits with a message describing its status.

Train one shared LoRA adapter for both styles with DPO against a fixed TranslateGemma reference policy.

**TODO** — LoRA and DPO hyperparameters, and reference policy memory strategy on one H100.

The Jean Zay command log in [run.sh](run.sh) records the Stage 04 preference dataset command. The upstream command is commented so this stage can reuse existing artifacts. The stage's batch template is [`train_dpo.slurm`](train_dpo.slurm).

Stage configuration is in [style_dpo.yaml](style_dpo.yaml).
