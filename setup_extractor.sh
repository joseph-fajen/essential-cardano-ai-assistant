#!/bin/bash

echo "Setting up Essential Cardano Content Extractor"

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file template if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env template..."
    cat > .env << EOF
# Add your Firecrawl API key here
FIRECRAWL_API_KEY=your_api_key_here
EOF
    echo "✅ Created .env file - please add your Firecrawl API key"
else
    echo "✅ .env file already exists"
fi

# Create output directory
mkdir -p extracted_content
echo "✅ Created output directory: extracted_content/"

echo ""
echo "Setup complete! Next steps:"
echo "1. Add your Firecrawl API key to .env file"
echo "2. Run: python test_firecrawl.py (to test API connection)"
echo "3. Run: python essential_cardano_extractor.py (to start extraction)"