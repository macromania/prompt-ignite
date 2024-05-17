#!/bin/bash

set -e

cd ./

echo "Running python from:"
which python

echo "🐍 Creating a virtual environment..."

# all of our dependencies rely on python3.11
python3.11 -m venv .venv

echo "🐍 Virtual environment created. Running 'source .venv/bin/activate' to activate it."

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not in a virtual environment. Connecting to it..."
    source .venv/bin/activate
else
    echo "Already connected to a virtual environment: $VIRTUAL_ENV."
fi

echo "🐍 Installing dependencies..."
pip install -r requirements.txt

echo "🐍 Setting up notebooks filtering"
nbstripout --install --attributes .gitattributes