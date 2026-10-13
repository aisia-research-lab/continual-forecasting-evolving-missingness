# Continual Forecasting with Evolving Missingness

**Continual Forecasting with Evolving Missingness: Observational Ambiguity and Delayed Predictive Information**

**Paper status:** Submitted to *Neurocomputing* (Elsevier).

This repository provides the code, experimental results, and configurations supporting the manuscript. It includes theoretical computations, forecasting-result analysis, and reproducibility scripts.

## Reproduce the reported analyses

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
make test
make theory
make analyze
make selection
make audit
make tables
```

`make theory` computes exact finite-sample minimax risk for the regenerative model. `make analyze` reads original outcome archives and reports by-condition results for the long-horizon clipping study, the Beijing/Tetouan comparisons and the validation-locked experiment. `make selection` reconstructs whole-arm selected-vs-delayed origin-level loss contrasts. `make audit` checks the archived release-event timestamps. Recomputed CSVs appear under `results/derived/`.

### Experiments in the manuscript

| Manuscript evidence | Contents | Archive |
|---|---|---|
| Delayed adaptation on ETT | Historical ETT outcome archive (format may differ) | `ett_delayed_adaptation.tar.gz` |
| Bounded corrections for long-horizon ETTh2 forecasting | Five-seed paired corrected-vs-delayed losses | `long_horizon_clipping.tar.gz` |
| Beijing and Tetouan adaptation reliability | Controlled input masks and delayed online feedback | `external_datasets.tar.gz` |
| Validation-Locked arm selection | Source-seed selection provenance and held-out test losses | `validation_locked_selection.tar.gz` |

The historical ETT archive is retained for provenance; the generic `make analyze` targets the three consistently structured later experiments. Run the earlier ETT evaluation only after reviewing its archive schema.

### Statistical interpretation

Overlapping forecast origins are not independent statistical replicates. Paired inference is over training seeds. With five seeds, a two-sided exact sign-flip calculation cannot attain a p-value below 0.0625 when all differences have the same sign. Do not interpret origin-level harm fractions as confidence intervals. The timestamp audit verifies the logged event fields, not source-level absence of every possible leakage path.

### Data availability

The GitHub-ready bundle includes **derived experiment records**; original source datasets can be obtained from [ETT](https://github.com/zhouhaoyi/ETDataset), [Beijing Multi-Site](https://archive.ics.uci.edu/dataset/501/beijing), and [Tetouan Power Consumption](https://archive.ics.uci.edu/dataset/849/power+consumption+of+tetouan+city). Review redistribution rights and archive contents before pushing the included result bundles to a public repository.


### Scope and limitations

This repository covers results reported in the manuscript, including theoretical calculations and archived-result reanalysis. Full GPU training reproduction is not supported.

See `configs/` and `docs/REPRODUCIBILITY.md` for details.

