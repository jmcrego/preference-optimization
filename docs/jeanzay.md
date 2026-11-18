# Jean Zay

Keep the checkout on persistent storage. The default scratch root is `/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization`. An absolute `SCRATCH_DIR` overrides it.

Sourcing `slurm/setup_environment.sh` in Bash exports scratch-based cache paths and Hugging Face offline settings. From the repository checkout on Jean Zay, run:

```bash
SCRATCH_DIR=/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization \
  bash scripts/initialize_storage.sh
```

The initializer creates the dataset and experiment subdirectories, cache directories, and the top-level `venvs`, `logs`, and `tmp` directories. It prints the root it initialized and can be rerun safely. For Stage 01, choose a new output directory under `datasets/prepared/`. The environment creation script and all SLURM templates exit as stubs.

Confirm the persistent checkout location, account, partition, time limits, CPU and memory requests, GPU allocation syntax, module commands, and Python/CUDA/PyTorch environment. Each future GPU job uses one H100. Confirm the existing shared TranslateGemma path and revision before populating `TRANSLATEGEMMA_MODEL_PATH`. Teacher and judge locations also remain open.
