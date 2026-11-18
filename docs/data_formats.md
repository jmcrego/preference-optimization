# Data formats

Stage 01 converts existing train and test TSVs into separate JSONL files with source text, references, language codes, and IDs derived from the split and input line number. See the [converter usage](../01_data_preparation/README.md). Provenance tracking is deferred. Split by source before expanding accepted pairs into two reversed style-conditioned preference records. Keep links to candidates and validation evidence.

See the [roadmap](implementation_plan.md) for sample records. Versioned schemas for later stages are deferred.
