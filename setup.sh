#!/bin/bash
# Setup script for Headless Job Applier - Linux/Mac
# This script initializes the development environment

echo ""
echo "========================================"
echo "Headless Job Applier - Setup Script"
echo "========================================"
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

echo "[1/7] Checking Python version..."
python3 --version
echo ""

# Create virtual environment
echo "[2/7] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping creation"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/7] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo ""

# Upgrade pip
echo "[4/7] Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to upgrade pip"
    exit 1
fi
echo ""

# Install dependencies
echo "[5/7] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

# Install Playwright browsers
echo "[6/7] Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "WARNING: Playwright browser installation had issues, continuing anyway..."
fi
echo ""

# Initialize application
echo "[7/7] Initializing application..."
python src/main.py setup
if [ $? -ne 0 ]; then
    echo "ERROR: Application setup failed"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and fill in your credentials"
echo "2. Update input/user_profile.yaml with your information"
echo "3. Run: python src/main.py status"
echo ""
echo "To activate the environment in the future:"
echo "  source venv/bin/activate"
echo ""
