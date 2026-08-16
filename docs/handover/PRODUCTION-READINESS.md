# Minify++ production-readiness assessment

## Current decision

**REOPENED; REPAIRED CANDIDATE UNDER FINAL REVALIDATION — 2026-08-16**

The earlier pass was withdrawn when Minify++ corrupted ordinary production CSS in
its own website. The repaired candidate has substantially stronger evidence and
all executable gates available on the working tree are green, but the readiness
decision remains reopened until a clean committed source-package `distcheck` and
final website/browser validation are rerun. Do not quote the earlier pass as the
current release decision.

## Candidate identity and environment

- standalone CLI version: 1.1.0;
- public format/API version: 1;
- language/build: C++17 and Make;
- directly validated host: Linux 7.0.0 x86-64;
- compiler: g++ 15.2.0;
- semantic/parser oracles: Node 22.22.1 and tsc 7.0.2;
- embedded consumer: Nift through `<minify/Minify.h>` only.

## Evidence accepted

- clean warning-enabled standalone build;
- clean committed `git archive` source package build and complete test run;
- focused C++ tests for all seven formats and minimized historical/fuzz findings;
- 15,459 executable JavaScript differential programs;
- 180 JSX/TSX parse-and-idempotence programs;
- 115 generated non-JavaScript documents, including JSON structural equivalence;
- 16 representative CSS stylesheets compared through an independent normalized
  PostCSS semantic-tree oracle;
- cross-format adversarial/malformed cases and CLI transaction tests;
- deterministic 7,000,000-case mutation campaigns across all formats under both
  the ordinary and ASan/UBSan builds;
- ASan, UBSan, and LeakSanitizer runs of direct, mutation, and CLI workloads with
  no findings in the unrestricted release-like environment;
- per-format benchmark covering 0.71–1.16 MB inputs over 20 iterations, measuring
  roughly 62–409 MiB/s and 21 MiB aggregate peak RSS on the stated host;
- exact 20-file standalone/Nift synchronization gate;
- green Nift opt-in minification integration;
- Minify++ website rebuilt successfully from reconciled source documentation.

The reopened audit found additional genuine families: ordinary CSS component and
selector boundaries were merged; JavaScript spacing could manufacture block-comment
delimiters; the JSX root finder scanned inside JavaScript comments; and several
format scanners accepted unterminated quotes ending at a misleading `>` byte.
Every finding is now retained as a focused regression. This history is evidence
that passing finite gates does not make the decision irreversible.

## Remaining close-out evidence

- commit the coherent standalone and embedded changes, then run `make distcheck`
  against the resulting clean archive (the workflow intentionally refuses a dirty
  tree, so it cannot validate uncommitted source);
- rebuild the Minify++ website with the repaired embedded engine and verify the
  result in a browser, including layout width and representative computed styles;
- reconcile public website maturity claims with the reopened audit and final
  decision.

## Public safety and failure model

The library is stateless and whole-buffer. It returns success/output or a controlled
error. The CLI validates format and input, distinguishes failed reads from empty
files, prepares complete output in a sibling temporary directory, preserves an
existing regular file's permission bits, and rejects symbolic-link destinations.
On systems where standard rename cannot replace a destination, it uses a bounded
backup/restore fallback.

No claim is made that writes survive sudden power loss without filesystem-specific
durability primitives. Ownership and timestamps are not preserved as part of the
public contract. Multi-file CLI operation remains best-effort per file and returns
failure if any item fails.

## Known limitations that do not block this scoped decision

- macOS and Windows have not been directly validated in this checkpoint;
- XML/SVG modes are conservative lexical minifiers, not validating XML parsers;
- HTML raw script/style bodies and JavaScript template contents are preserved
  rather than recursively minified;
- TypeScript is not a general input mode; JSX support includes tested TSX-aware
  boundaries but does not compile TypeScript;
- semantic evidence is necessarily finite and must grow with real production bugs
  and language evolution;
- the benchmark is a regression reference for this host/fixture, not a competitor
  ranking or portable speed promise.

## Reopen or downgrade if

- a supported input changes meaning, crashes, hangs, or causes unbounded growth;
- a scanner or format contract changes without equivalent semantic/adversarial
  evidence;
- standalone and Nift embedded files drift;
- CLI replacement/recovery behavior changes;
- release claims expand to macOS/Windows without direct or CI evidence;
- a clean committed source package no longer builds and runs its gates;
- documentation or website claims outrun the implementation.

Every confirmed production defect should become a minimized deterministic
regression. Reassess rather than preserving this decision ceremonially.
