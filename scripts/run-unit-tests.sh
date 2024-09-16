#!/bin/bash

set -e

cd ./

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not in a virtual environment. Connecting to it..."
    source .venv/bin/activate
else
    echo "Already connected to a virtual environment: $VIRTUAL_ENV."
fi

echo "🐍 Running unit tests..."

pytest test