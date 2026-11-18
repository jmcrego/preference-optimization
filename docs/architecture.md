# Architecture

The numbered stage directories own their entry points and document their inputs and outputs. Shared code belongs in `src/preference_optimization/`. Phase 1 provides scratch path resolution and leaves namespaces in place for later implementations.

Feature definitions belong in `configs/features/`, with feature-specific rules under the package's `features` namespace. The shared data, training, and evaluation code will consume feature definitions through a common interface. See [adding features](adding_features.md).
