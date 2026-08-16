# Minify++ production-readiness assessment

## Current decision

**PASS WITH KNOWN LIMITATIONS — 2026-08-16**

Minify++ is production-ready for deliberate use within its documented conservative
HTML, CSS, JavaScript, JSX, JSON, XML, and SVG format/API/CLI contract on the
directly validated Linux toolchain. This is a maintained evidence judgment, not a
claim of universal semantic equivalence, smallest possible output, support for all
future syntax, or validation on platforms not actually exercised.

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
- 111 generated non-JavaScript documents, including JSON structural equivalence;
- cross-format adversarial/malformed cases and CLI transaction tests;
- deterministic 70,000-case mutation gate across all formats;
- ASan, UBSan, and LeakSanitizer runs of direct, mutation, and CLI workloads with
  no findings in the unrestricted release-like environment;
- per-format benchmark covering 0.71–1.16 MB inputs over 20 iterations, measuring
  roughly 62–409 MiB/s and 21 MiB aggregate peak RSS on the stated host;
- exact 19-file standalone/Nift synchronization gate;
- green Nift opt-in minification integration;
- Minify++ website rebuilt successfully from reconciled source documentation.

The mutation layer materially increased confidence by discovering three genuine
token-manufacturing families before this decision: CSS `/ *` joining into a
comment, JSX-mode `< name` joining into an opener, and malformed HTML/XML prefixes
joining into comment/CDATA-like syntax. All were fixed conservatively and retained
as focused regressions before the complete evidence wall was rerun.

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
