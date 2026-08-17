#!/usr/bin/env python3
"""Same-host CLI comparison for Minify++, esbuild, and Lightning CSS.

This benchmark intentionally measures complete command-line invocations. It does
not replace benchmarks that call a tool's library API in-process. Missing
competitor executables are reported and skipped rather than silently substituted.
"""
from __future__ import annotations

import argparse
import csv
import shutil
import statistics
import subprocess
import tempfile
import time
from pathlib import Path


def run_once(tool: str, binary: Path, source: Path, output: Path) -> float:
    if tool == "minifypp":
        work_input = output.with_name("input.css")
        shutil.copy2(source, work_input)
        generated = work_input.with_name("input.min.css")
        if generated.exists():
            generated.unlink()
        command = [str(binary), str(work_input)]
        expected = generated
    elif tool == "esbuild":
        command = [str(binary), str(source), "--minify", "--legal-comments=none", f"--outfile={output}"]
        expected = output
    elif tool == "lightningcss":
        command = [str(binary), "--minify", str(source), "-o", str(output)]
        expected = output
    else:
        raise ValueError(tool)

    start = time.perf_counter()
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    if completed.returncode != 0:
        raise RuntimeError(
            f"{tool} failed ({completed.returncode}): "
            + completed.stderr.decode("utf-8", "replace")[:1000]
        )
    if not expected.exists():
        raise RuntimeError(f"{tool} did not create expected output {expected}")
    if expected != output:
        shutil.copy2(expected, output)
    return elapsed_ms


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures", nargs="+", type=Path)
    parser.add_argument("--minifypp", type=Path, default=Path("./minify"))
    parser.add_argument("--esbuild", type=Path)
    parser.add_argument("--lightningcss", type=Path)
    parser.add_argument("--iterations", type=int, default=15)
    parser.add_argument("--warmups", type=int, default=3)
    args = parser.parse_args()
    if args.iterations < 1 or args.warmups < 0:
        parser.error("iterations must be positive and warmups non-negative")

    tools: list[tuple[str, Path | None]] = [
        ("minifypp", args.minifypp),
        ("esbuild", args.esbuild),
        ("lightningcss", args.lightningcss),
    ]

    writer = csv.writer(__import__("sys").stdout)
    writer.writerow(["fixture", "tool", "input_bytes", "output_bytes", "median_ms", "iterations"])
    with tempfile.TemporaryDirectory(prefix="minifypp-css-bench-") as td:
        temp = Path(td)
        for fixture in args.fixtures:
            fixture = fixture.resolve()
            if not fixture.is_file():
                raise SystemExit(f"fixture not found: {fixture}")
            for tool, binary in tools:
                if binary is None:
                    continue
                binary = binary.resolve()
                if not binary.is_file():
                    raise SystemExit(f"{tool} executable not found: {binary}")
                samples: list[float] = []
                output = temp / f"{fixture.stem}-{tool}.css"
                for index in range(args.warmups + args.iterations):
                    if output.exists():
                        output.unlink()
                    elapsed = run_once(tool, binary, fixture, output)
                    if index >= args.warmups:
                        samples.append(elapsed)
                writer.writerow([
                    fixture.name,
                    tool,
                    fixture.stat().st_size,
                    output.stat().st_size,
                    f"{statistics.median(samples):.3f}",
                    args.iterations,
                ])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
