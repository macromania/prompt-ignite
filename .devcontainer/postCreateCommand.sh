#!/usr/bin/env bash

set -e

echo "🚚 Removing cache..."
rm -rf .venv

echo "🚚 Installing Poetry..."
poetry config virtualenvs.in-project true
POETRY_REQUESTS_TIMEOUT=120 poetry install -vv

echo "🤖 Setting script file permissions..."
chmod -R +x ./scripts

echo "🤖 Setting up ownership at repository root..."
git config --global --add safe.directory /workspaces/prompt-ignite

# Activate the virtual environment
if [ -d ".venv" ]; then
    echo "📟 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "👀 Virtual environment not found. Please create it first."
fi

echo "🐍 Setting up notebooks filtering"
nbstripout --install --attributes .gitattributes