#!/bin/bash

CURRENT_TIME=$(date +%Y%m%d_%H%M%S)

coverage run --omit="*/.venv/*,*/package/*" -m unittest discover -s . -p "test_*.py"
coverage report -m > "coverage_report_${CURRENT_TIME}.txt"