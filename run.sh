#!/bin/bash

# Williamsburg News - Development Server Startup Script

echo "Starting Williamsburg News Flask Application"
echo "============================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the application
echo "Starting Flask development server..."
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
