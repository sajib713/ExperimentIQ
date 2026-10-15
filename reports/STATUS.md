# Business decision memo — status / truthful outcome

**BLOCKED: actual Hillstrom CSV was not downloadable from the build sandbox.**

The report generator is implemented in `src/experimentiq/report.py`. It will write `business_decision_memo_actual.md` **only after** 64,000 raw CSV rows pass validation and the local pipeline completes. No business results or p-values are hard-coded. Test fixture metrics are never presented as actual experiment results.

The real memo will include business question, source SHA/provenance, assigned sample size per arm, conversion / visit / spend KPIs, Newcombe intervals, Holm-adjusted p-values, SRM, spend bootstrap intervals, guarded recommendations, missing business inputs and limits.

To generate: `python -m experimentiq.cli all`. **Do not take business action based on an absent or synthetic analysis.**
