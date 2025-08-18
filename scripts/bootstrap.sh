#!/bin/bash
echo "🐝 Initializing NECTR_AI environment..."

# Create venv
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt

# Create attack logs folder
mkdir -p data/attack_logs

# Confirm setup
echo "✅ NECTR_AI environment ready."
