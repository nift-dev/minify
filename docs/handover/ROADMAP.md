# Minify++ production-readiness roadmap

This is a living risk assessment. Review it at every substantial checkpoint;
new corpus failures, syntax evolution, sanitizer findings, performance evidence,
Nift integration, and user needs may reorder, expand, narrow, or remove work.

## Architecture-reconciliation findings

The August 2026 reconciliation verified a stateless whole-buffer implementation
with seven formats, byte-identical standalone and Nift-embedded trees, substantial
JavaScript/JSX generated evidence, and final-output Nift integration. It also
converted inherited concerns into concrete roadmap work:

- enforce standalone-to-embedded equality with a machine-checkable sync/diff gate;
- make standalone CLI reads report open/read failure rather than treating failure
  as empty input;
- replace direct truncating writes with a safe temporary/commit model, preserving
  appropriate metadata and accounting for cross-platform rename rules;
- rerun the non-JavaScript JSON oracle outside the restricted Codex stream
  environment; the JSX generated corpus has since passed all 180 programs with
  tsc 7.0.2;
- add repeatable ASan/UBSan, fuzz, and performance/RSS targets;
- retain the conservative policy that HTML raw script/style bodies and JavaScript
  template contents are preserved rather than recursively minified.

Reorder or retire these items as implementation evidence changes.

## Current checkpoint status

- **COMPLETE — production-readiness audit:** all current standalone gates pass,
  including 15,459 executable JavaScript programs, 180 JSX/TSX programs, and the
  111-document non-JavaScript corpus with JSON structural comparison. The latter
  was rerun successfully outside the desktop stream wrapper.
- **COMPLETE — synchronization evidence:** an 18-file standalone/Nift equality
  gate now makes embedded drift machine-checkable.
- **COMPLETE — bounded CLI hardening:** checked reads distinguish failure from
  empty input; sibling-temporary replacement preserves existing permission bits,
  rejects symbolic-link destinations, and has CLI regression coverage.
- **COMPLETE — native/tooling evidence:** repeatable sanitizer, 70,000-case
  fuzz-smoke, and performance/output-size/RSS targets are green. The fuzz gate
  exposed three token-manufacturing families, now fixed and retained.
- **PLANNED — clean package/platform evidence:** prove a source-only checkout,
  document the validated host/toolchain, and keep broader platform claims bounded.
- **PLANNED — public reconciliation:** correct the website's stale 39-document
  claim to the current 111-document evidence and publish only defensible maturity
  language.

## Production-ready meaning

A developer should be able to run Minify++ deliberately on documented supported
production assets with strong evidence that meaning is preserved, unsupported or
problematic input fails/preserves predictably, the CLI/API are stable enough to
use, performance is strong, and releases are repeatably validated.

It does not require smallest output on every file or perfect support for every
future syntax.

## Current inherited priorities

1. Reconcile exact per-format supported and malformed-input contracts with source,
   tests, README, and website.
2. Systematically audit HTML whitespace/raw-text contexts, CSS token/custom
   property/modern syntax boundaries, and JavaScript ASI/slash/template/token
   families.
3. Expand real-world HTML/CSS/JS/JSX/XML/SVG corpus coverage and minimize findings.
4. Strengthen runtime/structural semantic oracles where exact output is weak.
5. Run substantial ASan/UBSan validation and introduce sanitizer-backed fuzzing
   proportionately.
6. Establish reproducible startup/throughput/RSS/output-size benchmarks only for
   semantically green checkpoints.
7. Keep standalone and Nift embedded copies synchronized and exercise Nift's
   opt-in integration.
8. Reconcile documentation, website maturity language, limits, tests, and claims.
9. Validate a clean release-like package and decide production status with Nick.

The current maturity assessment is “substantial hardening evidence, but production
confidence should be re-earned from current corpus/safety results,” not a fixed
percentage.

## After production

Track evolving web syntax deliberately, expand corpus diversity, respond to every
production bug with a regression, improve diagnostics/platform coverage, monitor
performance, and keep Nift integration and the public contract synchronized.
