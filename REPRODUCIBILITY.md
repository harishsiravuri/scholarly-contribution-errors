# Reproducibility

This note documents the settings behind every number in the accompanying paper. The released
files carry the model outputs (per-fact `error_score`, `violated_constraints`, labels), so the
reported metrics can be recomputed directly from the data; the method settings below allow a
full re-implementation. Author identities are withheld for double-blind review.

## Data
- 47,613 quantitative facts extracted from the full text of 1,625 arXiv papers.
- Ground truth is a frozen Papers with Code snapshot dated 2025-07-28 (service retired
  2025-07-24), pinned by hash in `MANIFEST.sha256`.
- A fact is in-gold when its (method, dataset, metric) names match a leaderboard cell. It is
  labeled `correct` when its value matches the gold value within tolerance (relative 1 percent
  with a small absolute floor, plus a percent-versus-fraction rescaling), and `incorrect`
  otherwise. 5,433 facts are in-gold; 42,180 are out-of-gold.
- Split is at the paper level with a fixed seed, so no paper appears in both `dev` and `test`.

## Neural signal
A gradient-boosted decision tree over five value-independent extraction signals
(self-consistency across sampling temperatures, critic verdict, span grounding, source
location, and canonicalization match type), wrapped in isotonic regression and selected on the
development split by Brier score. Its output is the calibrated per-fact reliability
(`calibrated_prob`). It is out-of-sample on the test split.

## Symbolic constraints
Five families over sets of facts: metric bounds, ranking/transitivity within a
(dataset, metric) leaderboard, intra-paper coherence, multi-report agreement across papers, and
magnitude/precision outliers. A fact's symbolic features are its participation flags in each
family and a reliability-weighted estimate of being the erroneous member of a violated set.
`violated_constraints` records the families each fact violates.

## Learned combiner
The `error_score` is a logistic regression over the standardized neural signal and symbolic
features, fit on the development in-gold split to predict the incorrect label. Gradient-boosted
and random-forest combiners were run as robustness checks and give similar or better detection.

## Base-model scale sweep
The neural signal is replaced by a per-fact judgment from GPT-4o-mini, GPT-4o, and
Claude Opus 4.8, using a single zero-shot prompt that provides the tuple, the source location,
and the supporting quote, and asks *"How likely is this reported value correct?"* as a
probability. The prompt does not include the graph structure the symbolic features encode. Total
language-model spend was 10.71 USD; judgments are cached.

## Evaluation
Metrics are AUROC, AUPRC, and recall at a fixed review budget, with bootstrap 95 percent
confidence intervals and, for the main gaps, a paired bootstrap and a DeLong test. The
injected-error study uses five seeds.

## Human validation
800 facts sampled stratified by error-score bin and labeled blind to the score
(`human_validation.csv`). A second annotator independently labeled a 150-fact overlap
(`second_annotator_overlap.csv`); independent agreement was moderate (Cohen's kappa 0.53) and
disagreements, concentrated in table-column pairing, were adjudicated to consensus. The released
labels are the adjudicated set.

## Headline results (held-out test in-gold; 2,703 facts, 1,249 real errors)
- Learned neural-symbolic combiner AUROC 0.668, above neural-only 0.624 (+0.045, CI
  [0.034, 0.056]) and symbolic-only 0.644 (+0.025, CI [0.007, 0.044]) under a fixed-learner
  ablation.
- The learned symbolic layer improves every base model's per-fact judgment across scales,
  including the frontier (0.682 to 0.715); a naive additive layer ties at the frontier.
- Repair is unsafe: an auto-applied conservative repair would corrupt about 26 percent of
  candidates, so the method detects and triages for human review rather than editing the graph.
- Transfer: on the out-of-gold human labels the error score reaches AUROC about 0.64.
- Downstream: trimming the graph by the error score lowers a comparative question-answering
  consumer's confidently-wrong rate more than trimming the same fraction at random.
