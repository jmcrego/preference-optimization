# Architecture

The numbered stage directories own their entry points and stage-specific code. For example, Stage 01 uses its TSV converter as the Python entry point. Each stage documents its inputs and outputs. Stage-specific configuration lives in its stage directory. Shared storage, base-model, style, and dataset settings live in `configs/`. The scratch-path helper lives in `scripts/` beside the environment checker.

Feature definitions belong in `configs/features/`, with rules added where they are used once implemented. The shared data, training, and evaluation code will consume feature definitions through a common interface. See [adding features](adding_features.md).
