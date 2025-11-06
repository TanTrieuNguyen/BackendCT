#!/bin/bash

# Quick Start Script for Jaremis Character Server
# Run this script to start the server quickly

echo "🎭 Starting Jaremis Character Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/lib/python*/site-packages/flask/__init__.py" ]; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements_character.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Start server
echo "🚀 Starting server on http://localhost:10000"
echo ""
echo "📝 Press Ctrl+C to stop the server"
echo "🌐 Open browser: http://localhost:10000"
echo ""

python character_server.py
