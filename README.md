# Scholarly Contribution Graph: Error-Detection Resource

This repository releases the artifacts described in the paper *Detecting Wrong Facts in
Automatically Built Scholarly Contribution Graphs: A Neural-Symbolic Approach*. It contains
only those artifacts and their documentation.

*Anonymized for double-blind review.*

## Contents

| Path | What it is |
| --- | --- |
| `data/contribution_graph.parquet` | The cleaned, annotated contribution graph (47,613 facts). Each fact carries its (method, dataset, metric, value) tuple, the extraction signals, a per-fact reliability, the per-fact **error score**, the violated symbolic constraints, and a non-binding suggested repair. The 5,433 in-gold facts also carry the leaderboard label and gold value, so this file doubles as the **real-error benchmark**. |
| `data/human_validation.csv` | The 800-fact human validation set (adjudicated labels) used to test transfer of the error score to the out-of-gold majority. |
| `data/second_annotator_overlap.csv` | The 150-fact overlap independently labeled by a second annotator, so the reported inter-annotator agreement (Cohen's kappa) is reproducible. |
| `SCHEMA.md` | Column-by-column description of every file. |
| `DATASHEET.md` | Dataset documentation (motivation, composition, collection, uses, distribution). |
| `load.py` | A minimal loader and sanity check. |
| `MANIFEST.sha256` | SHA-256 of every released file, plus the frozen gold provenance. |
| `REPRODUCIBILITY.md` | Full settings, prompts, and constraint definitions. |
| `LICENSE` | CC BY-SA 4.0. |

## Provenance

The facts were extracted from the full text of arXiv papers and validated against a **frozen
Papers with Code snapshot dated 2025-07-28** (the live service was retired 2025-07-24). Papers
with Code is distributed under CC BY-SA 4.0; this release inherits **CC BY-SA 4.0** under the
ShareAlike term. The snapshot is pinned in `MANIFEST.sha256`.

## Quick start

```bash
pip install pandas pyarrow
python load.py
```

## How this maps to the paper

The `error_score` column is the learned neural-symbolic error score. Facts with `in_gold =
True` carry `correctness_label` and `gold_value` (the real-error benchmark). `human_validation.csv`
is the deployment-population validation. All numbers reported in the paper can be reproduced
from these files together with `REPRODUCIBILITY.md`.
