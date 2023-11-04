#!/bin/bash

CWD="$(dirname "$0")"
cd $CWD

# Setup pyenv since .bashrc isn't loaded for a systemd service
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Need python version 3.8
pyenv local 3.8

source .env/bin/activate
python -u run.py
