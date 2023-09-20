
#!/bin/bash

# Installing prerequisites
sudo apt update
sudo apt install python3
pip install flask sqlalchemy

# Cloning the repository
git clone https://github.com/Quannggg/Crawler-Web.git

# Navigating to the project directory
cd Crawler-Web

# Creating a virtual environment
python -m venv venv

# Activating the virtual environment
source venv/bin/activate

# Installing the required Python packages
pip install beautifulsoup4 requests sqlalchemy flask Flask-SocketIO

echo "Installation complete!"
