#!/usr/bin/env bash
set -euo pipefail

# Activate conda
# Needed to make conda available in non-interactive shells first
# Reference: https://github.com/ContinuumIO/docker-images/issues/89#issuecomment-467287039
# FIXME: hard-coded conda path
source $CONDA_DIR/etc/profile.d/conda.sh

# Note this is also duplicated in the docker-base file, where we add them to ~/.bashrc
# for non-login shells
conda deactivate
conda activate lumos

exec "$@"