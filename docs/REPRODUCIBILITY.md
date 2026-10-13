# Reproducibility and known limitations

## What is reproducible
- Exact numerical minimax-risk formula for the restricted Markov--MNAR construction.
- Per-origin and valid-coordinate-weighted loss recomputation from the bundled forecasting-outcome archives.
- Validation-Locked choice reconstruction from whole-arm forecast rows and the original selection manifest.
- Release chronology checks for logged events, and seed-level paired statistical utilities.

## What is NOT reproduced from scratch
The original deep-learning architecture implementations, model initialization and source checkpoint training pipeline, optimizer states, and author-native baseline dependency tree were not supplied in the recovered materials as those files are too heavy to upload through Github. They cannot be reconstructed bitwise from CSV losses. 

Reproducing the trained forecasts from input datasets therefore requires additional code. Please follow our instructions for reproducibility.

## Evaluation definitions
Artificially masked historical inputs must not be treated as true observed future labels. Genuine target observation validity determines loss inclusion. When valid counts vary, use valid-coordinate-weighted MSE for aggregate forecasts, not simple average of per-origin MSE; both statistics are available in the reanalysis output. Strict release: `target_end + reporting_delay < used_at`. The names inside archived files reflect the historical execution layout and are deliberately preserved to avoid modifying experiment evidence; they are not public experiment identifiers.

## External evaluation limitation
The model-selection experiment uses new seeds but test timestamps previously examined in the external fixed-arm study. It is not an independently untouched-time test. Unequal candidate-training costs also mean that validation selection is not compute matched.

## Original raw datasets
ETT: https://github.com/zhouhaoyi/ETDataset
Beijing: https://archive.ics.uci.edu/dataset/501/beijing
Tetouan: https://archive.ics.uci.edu/dataset/849/power+consumption+of+tetouan+city
