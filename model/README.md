# Model

| File | What it is |
|---|---|
| `core.js` | The ML pipeline used in the Claude session: feature builder (17 price-history features), gradient boosting and logistic regression, walk-forward folds, calibration. Horizon 36 months for P(2x); a separate model predicts P(−50%). |
| `ml_results.json` | Output of the run: `pred` (per-stock P(2x), horizon, last data month, months of history), `loss` (P(−50%)), `folds` / `foldsUntuned` (walk-forward test metrics), `oos` (pooled out-of-sample AUC, Brier, decile calibration), `auc36`, `loss_model`, `imp` (feature importance), `lrw` (logistic weights), `data` (training-set size), `mktNow` (current market features). |

Training data was monthly price history downloaded during the session; it isn't stored here (it can be re-fetched).
The final P(2x) in the report blends this model 50/50 with the rules model.
