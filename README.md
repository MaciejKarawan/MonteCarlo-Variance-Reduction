# Monte Carlo variance reduction

Academic work by Adamek and Karawan; attribution remains in the report.

Install Python 3.11 or 3.12 and `python -m pip install -e .`. This research code retains a legacy conversion of a length-one NumPy array to a scalar; NumPy is constrained to `>=1.26,<2` to preserve its original numerical implementation. NumPy 2.x rejects that conversion. The migration checks exercise this compatibility requirement.

- `src/variance_reduction/`: pricing and variance-reduction implementations.
- `scripts/`: explicit analysis and plot entry points.
- `reports/`: original PDF; `results/`: reference/generated result policy; `data/`: input policy.

From the repository root: `python -m scripts.analysis`, `python -m scripts.comparison_plots`, or `python -m variance_reduction.control_variate`. These commands run simulations and plots; inspect budgets first. Importing computational modules no longer starts those experiments. The former test.py is now pricing.py: it contains model functions, not an automated test suite. Distinct antithetic/control-variate implementations are retained without merging their numerical logic.

See `docs/file-migration.json`. Original environment versions are unknown; no licence was assigned. Small deterministic regression checks cover the migration, not scientific validity of all estimators.

## Migration checks

After installation: `python -m unittest discover -s tests -v`. These small checks do not run the full research experiments.
