#!/bin/sh
set -e

uv run pytest trips/tests/ --cov=trips --cov-report=xml --cov-report=term-missing
