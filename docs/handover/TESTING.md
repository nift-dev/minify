# Minify++ testing handover

## Current layers

The Makefile's `test` target runs:

- focused C++ format smoke tests;
- Node-based semantic comparison;
- deterministic generated JavaScript semantic programs;
- generated JSX/TSX syntax and idempotence cases;
- non-JavaScript format idempotence;
- cross-format adversarial/malformed cases;
- CLI behavior.

Retained checkpoint counts are evidence tied to current scripts, not a target.
Quality is the diversity of semantic assumptions attacked.

## Oracle selection

- Exact/golden output: useful for deliberately stable lexical transformation.
- Runtime equivalence: preferred for executable JavaScript when practical.
- Structural parse comparison: strong for JSON.
- Syntax/idempotence: useful discovery/protection for JSX and conservative
  non-JavaScript formats, but not complete semantic proof.
- Real-world corpus: catches interactions absent from generated matrices.
- Differential tools: discovery aid; another minifier's spelling is not contract.

Do not assume `minify(minify(x)) == minify(x)` for every format unless current
contract intentionally guarantees it. Existing idempotence gates protect the
formats/cases they actually exercise.

## Adversarial matrix

### Cross-cutting

Empty/whitespace input, Unicode, mixed newlines, long tokens, deep nesting,
unterminated constructs, malformed input, comments, escapes, and boundary bytes.

### HTML

Inline text whitespace, block/inline boundaries, `pre`/`textarea`, raw
`script`/`style`, comments, entities, attribute quotes, malformed tags, and
embedded language boundaries.

### CSS

Selector/token joining, strings, URLs, comments, functions, custom properties,
numbers/units, `calc()`, modern syntax, and malformed blocks.

### JavaScript

ASI after `return`/`throw`/`break`/`continue`, postfix increments, expression
statement boundaries, operator joining, regex/division/comments, templates and
nested `${...}`, async/generator/class/object/destructuring contexts, modules,
optional chaining, numeric/Unicode syntax, and side-effect evaluation.

### JSX/TSX

Nested elements/fragments, expressions, comments/strings/regex containing angle
characters, generic arrow ambiguities, type/assertion/satisfies contexts, and
malformed nesting.

### JSON/XML/SVG

JSON structural equivalence and malformed rejection. XML/SVG lexical safety,
CDATA/entities/attributes/comments, while retaining conservative non-validator
claims.

## Semantic generation and corpus growth

Generated matrices should vary independent context dimensions rather than create
thousands of cosmetic duplicates. Batch execution where it preserves case
isolation. Any real-world failure should be minimized into a focused permanent
case and retained in the corpus where representative.

## Native safety and fuzzing

Scanner/indexing changes are strong ASan/UBSan candidates. Fuzzing should mutate
valid seeds and malformed inputs, detect crashes/hangs/unbounded memory, minimize
findings, and convert them into deterministic regressions. Runtime differential
fuzzing is especially valuable for supported JavaScript.

The 111-document non-JavaScript corpus, including its Node-backed JSON structural
oracle, passed in an unrestricted process environment during the production audit.
The desktop process wrapper may stall that final `spawnSync` oracle; rerun it
outside that wrapper rather than silently omitting the result.

## Embedded synchronization

Run `make check-nift-sync NIFT_MINIFYPP_DIR=/path/to/nift/minifypp` whenever the
canonical standalone implementation, public surface, tests, or build contract
changes. It compares the explicit mirrored file set and fails on missing or
different files. Nift-specific integration behavior still requires Nift's own
tests; byte equality is necessary but not sufficient.

## Performance

Measure startup, many small files, large files, per-format throughput, peak RSS,
and output size using semantically green candidates. Record machine, compiler
flags, corpus, iterations, and tool versions. Report tradeoffs honestly.
