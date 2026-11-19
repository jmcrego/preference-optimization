# Jean Zay

Keep the checkout on persistent storage. The default scratch root is `/lustre/fsn1/projects/rech/eut/ujt99zo/josep/preference-optimization`. An absolute `SCRATCH_DIR` overrides it.

From the repository checkout, source this in your Bash login shell whenever you want to work on the project.

```bash
source scripts/setup_environment.sh
```

The script creates the scratch directories, exports cache paths and Hugging Face offline settings, and activates an existing virtual environment. It uses `$SCRATCH_DIR/venvs/preference-optimization` by default. Set `PROJECT_VENV` first if your environment lives elsewhere. If the environment is missing, setup reports its path and leaves the current Python active. Stage 01 works with system Python.

Load any modules required by your virtual environment before sourcing the script. Create the environment once after confirming the Python and module settings. The setup script can be sourced repeatedly and does not install anything. For Stage 01, choose a new output directory under `$SCRATCH_DIR/datasets/prepared/`.

Confirm the persistent checkout location, any required partition or memory settings, and the shared virtual environment's compatibility with the supplied runtime modules. Setup defaults `TRANSLATEGEMMA_MODEL_PATH` to the Jean Zay shared TranslateGemma directory. Stage 02 checks for `config.json` before submission. The model revision remains to be confirmed. Teacher and judge locations also remain open.

## Stage command logs and the shared environment

Each numbered stage keeps its Python entry point, SLURM template, and ordered `run.sh` together. Use `run.sh` to record the exact commands, arguments, and environment settings used on Jean Zay. Stage 01 runs the converter directly with system Python. Stage 02 submits the candidate-generation batch job. Stages 03–07 have command-log templates.

Future batch jobs that need the project environment should source the same script inside the job before starting Python.

## H100 batch templates

The Stage 02, 05, and 06 templates record the supplied reservation settings for account `eut@h100`. They specify one H100 on one node, ten CPUs per task, and a twenty-hour time limit. The module sequence loads `arch/h100` and `pytorch-gpu/py3/2.6.0` after purging the current modules. The reservation and module lines are enabled for Stage 02. Stages 05 and 06 keep them commented while their workloads are stubs. Stage 03's resource request depends on the judge backend.

Each `.slurm` script sets stdout and stderr paths under `./logs/`. Before submitting, create the Git-ignored `logs/` directory in the stage directory. Run the Stage 02 launcher from inside its stage directory so those relative paths resolve beside the scripts. Use the same submission pattern when enabling the other stages. The batch script loads the H100 modules and sources the project setup before running Python.
