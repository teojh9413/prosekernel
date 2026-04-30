#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e .
prosekernel brief "write a launch email for an AI writing tool" --root . --output /tmp/prosekernel-brief.md
prosekernel search-examples "write a launch email for an AI writing tool" --root . --limit 3
prosekernel lint examples/ai-slop-sample.md || true  # expected to fail: this fixture demonstrates anti-slop findings
prosekernel scorecard examples/ai-slop-sample.md --task "write a launch email for an AI writing tool" || true  # expected to fail quality gate for demo fixture
prosekernel eval --root .
