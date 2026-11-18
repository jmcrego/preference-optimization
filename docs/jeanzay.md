# Jean Zay

Keep the checkout on persistent storage. The default scratch root is `/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization`. An absolute `SCRATCH_DIR` overrides it.

From the repository checkout, source this in your Bash login shell whenever you want to work on the project.

```bash
source scripts/setup_environment.sh
```

The script creates the scratch directories, exports cache paths and Hugging Face offline settings, and activates an existing virtual environment. It uses `$SCRATCH_DIR/venvs/preference-optimization` by default. Set `PROJECT_VENV` first if your environment lives elsewhere. If the environment is missing, setup reports its path and leaves the current Python active. Stage 01 works with system Python.

Load any modules required by your virtual environment before sourcing the script. Create the environment once after confirming the Python and module settings. The setup script can be sourced repeatedly and does not install anything. For Stage 01, choose a new output directory under `$SCRATCH_DIR/datasets/prepared/`.

Confirm the persistent checkout location, any required partition or memory settings, and the shared virtual environment's compatibility with the supplied runtime modules. Confirm the existing shared TranslateGemma path and revision before populating `TRANSLATEGEMMA_MODEL_PATH`. Teacher and judge locations also remain open.

## Stage command logs and the shared environment

Each numbered stage keeps its Python entry point, SLURM template, and ordered `run.sh` together. Use `run.sh` to record the exact commands, arguments, and environment settings used on Jean Zay. Stage 01 runs the converter directly with system Python. The remaining command logs are templates for future stages.

Future batch jobs that need the project environment should source the same script inside the job before starting Python.

## H100 batch templates

The Stage 02, 05, and 06 templates record the supplied reservation settings for account `eut@h100`. They specify one H100 on one node, ten CPUs per task, and a twenty-hour time limit. The module sequence loads `arch/h100` and `pytorch-gpu/py3/2.6.0` after purging the current modules. The reservation and module lines stay commented while these stages are stubs. Stage 03's resource request depends on the judge backend.

The supplied `./logs/` paths are relative to the job's working directory. Once the templates are enabled, use the project scratch root as the job working directory and reference the batch script and project code via the persistent checkout. Source the project setup before submission to create the scratch log directory, then load the H100 modules and source the setup script inside the job before running Python.
