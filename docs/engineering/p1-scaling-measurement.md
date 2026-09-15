# P1 measurement: halftone scaling cost

## Problem redefinition

The first-order performance question is how processing cost scales with input pixels, output pixels, and effect complexity. A local micro-optimization is only useful if the corresponding stage is material to end-to-end runtime or memory.

## Hypothesis

The dominant cost may scale approximately with pixel count, with some behaviors adding a second multiplier through multi-pass effects or intermediate buffers. Identify which dimension actually dominates before changing implementation.

## Measurement matrix

Use fixed representative inputs at 512, 1024, 2048, and 4096 px long edge. Measure at least one simple, one texture-heavy, and one multi-stage style.

Record:

- wall-clock time
- peak memory where available
- output dimensions and file size
- stage-level timing when instrumentation permits
- output-quality/eval score

Repeat enough times to report median and tail/range. Keep runtime, image format, and settings fixed.

## Ablation

After locating the dominant stage, compare exactly one candidate change against baseline. Also include a simplified pipeline with the suspected optional stage removed to establish its marginal cost and quality contribution.

## P1 gate

Only optimize a stage if it represents a material share of end-to-end cost and its removal or implementation change preserves the quality envelope. Otherwise reject the candidate.

This PR establishes the measurement contract without changing rendering behavior.
