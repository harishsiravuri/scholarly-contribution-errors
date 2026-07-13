# Datasheet

Following the datasheets-for-datasets framework. Author identities are withheld for
double-blind review.

## Motivation
The dataset supports the study of error detection in automatically built scholarly contribution
graphs. It was created to release the cleaned graph, a real-error benchmark, and a human
validation set described in the accompanying paper.

## Composition
- **Instances.** 47,613 quantitative contribution facts, each a (method, dataset, metric,
  value) tuple extracted from an arXiv paper, with extraction signals, a per-fact reliability,
  an error score, violated symbolic constraints, and a non-binding suggested repair.
- **Labels.** 5,433 facts are in-gold (they map to a leaderboard cell) and carry a
  correctness label and gold value against a frozen Papers with Code snapshot. The remaining
  42,180 are out-of-gold and carry no external label. A separate 800-fact human validation set
  carries adjudicated human labels, and a 150-fact overlap carries a second annotator's labels.
- **Confidentiality.** All content derives from public arXiv papers and a public Papers with
  Code snapshot. No personal or sensitive data.

## Collection and preprocessing
Facts were extracted from paper full text by a multi-stage language-model pipeline, then
matched to leaderboard cells for the in-gold labels. The human validation facts were sampled
stratified by error score, labeled blind to the score, and disagreements between two annotators
were adjudicated to consensus. Full settings and prompts are in `REPRODUCIBILITY.md`.

## Uses
Intended for research on quality control, error detection, and curation of scholarly knowledge
graphs, and as a benchmark for per-fact error-detection methods. The error score ranks facts
by likelihood of being wrong; it is a triage signal, not a calibrated probability, and the
method detects and triages rather than autonomously repairs.

## Distribution and license
Released under CC BY-SA 4.0, inherited from the Papers with Code snapshot (CC BY-SA 4.0) under
ShareAlike. Attribute this dataset and Papers with Code. The frozen gold snapshot is pinned by
hash in `MANIFEST.sha256`.

## Maintenance
The gold snapshot is a fixed 2025-07-28 archive of a now-retired service and cannot drift, so
the benchmark is stable. Corrections to the released files, if any, will be versioned.
