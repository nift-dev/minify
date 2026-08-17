# Minify++ benchmark notes

`make benchmark` remains the canonical in-process regression benchmark for the
Minify++ C++ API. It is intentionally not a competitor ranking.

## Same-host CSS comparison

`compare_css_tools.py` compares complete CLI invocations on exactly the same CSS
files. Example:

```bash
python3 benchmarks/compare_css_tools.py \
  --minifypp ./minify \
  --esbuild /path/to/esbuild \
  --lightningcss /path/to/lightningcss \
  bootstrap-4.css animate.css tailwind.css
```

Record tool versions, host, compiler/build flags, fixtures and iteration count
with any retained result. Do not mix these CLI wall-clock medians with a tool's
published in-process API timing and call it a speed ranking.

Retained checkpoint CSV/text evidence lives under `benchmarks/results/`; public fixture files themselves are not vendored.

The public comparison checkpoint uses the GoalSmashers CSS benchmark copies of
Bootstrap 4, Animate.css 4.1.1 and Tailwind CSS because Lightning CSS publishes
esbuild/Lightning output sizes for those exact fixture sizes. The retained
Minify++ measurements were made independently on the checkpoint host; competitor
published times are context only and are not treated as same-host measurements.

## privatenumber JavaScript benchmark integration

`privatenumber_nift_adapter.ts` is a reference adapter for
`privatenumber/minification-benchmarks`. That benchmark gives each minifier an
adapter that accepts source text and returns minified source. Nift's public CLI is
file-oriented, so the adapter uses an isolated temporary `.js` file and invokes:

```bash
nift minify input.js
```

Set `NIFT_BIN=/absolute/path/to/nift` when running the upstream benchmark. The
adapter is intentionally kept here rather than vendoring/forking the upstream
suite. Any published Nift result should come from an actual run of the upstream
suite on its exact current artifacts and should record the upstream commit.

A local integration probe on a 515,136-byte `pptxgenjs` ES-module bundle produced
byte-identical Minify++ and Nift output (341,584 bytes; gzip -9: 102,233 bytes),
confirming that Nift exposes the same Minify++ engine through its CLI. This is an
integration probe, not a substitute for an upstream leaderboard result.
