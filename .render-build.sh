#!/usr/bin/env bash

# Use a shared wheel cache to avoid recompiling wheels
export WHEEL_DIR=/tmp/wheels

# Install packages for building
pip install --no-cache-dir --upgrade pip
pip wheel --wheel-dir $WHEEL_DIR -r app/requirements.txt  # Corrected path to requirements.txt

# Install from wheel cache
pip install --no-index --find-links=$WHEEL_DIR -r app/requirements.txt  # Corrected path to requirements.txt