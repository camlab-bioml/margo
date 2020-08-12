#!/usr/bin/env bash

set -e
set -x

pytest --cov=margo --cov=tests --cov-report=term-missing ${@}
# pytest .
bash ./scripts/lint.sh
