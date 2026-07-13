# Schema

## `data/contribution_graph.parquet` (47,613 rows)

One row per extracted quantitative fact.

| Column | Type | Description |
| --- | --- | --- |
| `paper_id` | str | arXiv identifier of the source paper. |
| `method` | str | Extracted method name (canonicalized where possible). |
| `dataset` | str | Extracted dataset name. |
| `metric` | str | Extracted evaluation metric. |
| `value` | float | Extracted numeric result. |
| `unit` | str | Unit of the value, if any. |
| `is_own_result` | bool | Whether the paper claims this as its own result rather than a cited baseline. |
| `claim_strength` | str | Strength of the surrounding claim. |
| `source_block` | str | Where the value was found (table, prose, abstract, or figure caption). |
| `evidence_quote` | str | The cited text span the value was extracted from. |
| `calibrated_prob` | float | Neural per-fact reliability, a calibrated probability that the fact is correct. |
| `correctness_label` | str | For in-gold facts only: `correct` or `incorrect` against the leaderboard. Empty otherwise. |
| `gold_value` | float | For in-gold facts only: the leaderboard value. Empty otherwise. |
| `in_gold` | bool | Whether the fact maps to a leaderboard cell (about 11 percent of facts). |
| `split` | str | Paper-level `dev` or `test` split (leakage-safe: no paper spans both). |
| `error_score` | float | Learned neural-symbolic error score; higher means more likely wrong. |
| `violated_constraints` | str | Pipe-separated list of symbolic constraints the fact violates (e.g., `intra_paper|multi_report`). |
| `repair_action` | str | `keep`, `flag_for_review`, or `suggested_repair`. |
| `proposed_repair` | float | Non-binding suggested corrected value, where one could be inferred. |
| `repair_source` | str | Basis for the proposed repair. |

The in-gold subset (`in_gold = True`, 5,433 facts) with `correctness_label` is the real-error
benchmark.

## `data/human_validation.csv` (800 rows)

Human-adjudicated labels used to validate transfer of the error score to the out-of-gold
majority. Joins to the graph on (`arxiv_id` = `paper_id`) and the tuple fields.

| Column | Description |
| --- | --- |
| `fact_id` | Stable identifier for the fact. |
| `tuple` | `method \| dataset \| metric \| value`. |
| `value` | Extracted numeric value. |
| `evidence_quote` | Cited text span. |
| `arxiv_id` | Source paper (equals `paper_id` in the graph). |
| `in_gold` | Whether the fact maps to a leaderboard cell. |
| `split` | Paper-level dev/test split. |
| `error_score` | The model's error score for this fact. |
| `score_bin` | Error-score bin used for stratified sampling. |
| `violated_constraints` | Symbolic constraints violated. |
| `human_label` | `correct`, `genuinely-wrong`, or `unjudgeable`. |
| `error_type` | For wrong facts: `wrong-value`, `wrong-pairing`, `not-a-result`, or `other`. |

## `data/second_annotator_overlap.csv` (150 rows)

The 150-fact subset labeled independently by a second annotator. `human_label` here is the
second annotator's judgment; the primary annotator's judgment for the same `fact_id` is in
`human_validation.csv`. Together they reproduce the reported Cohen's kappa.
