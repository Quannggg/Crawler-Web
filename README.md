# Elegant Web Crawler and Search Application

Welcome to our Elegant Web Crawler and Search Application, designed to simplify your web data extraction and exploration needs. This comprehensive tool offers a wide range of capabilities:

- **Web Crawling:** Gather valuable information from web pages effortlessly.
- **Efficient Data Storage:** Utilize SQLAlchemy for seamless data management and storage.
- **User-Friendly Interface:** Access and search your data through an intuitive web interface powered by Flask.
- **Customizability:** Configure web crawling targets and search functionality to meet your unique requirements.
- **Reliability:** Built-in error handling and data validation ensure consistent performance.

This project's versatility makes it suitable for various applications, from news aggregation to comprehensive data collection and search.

## Features

- **Web Crawling:** Easily collect data from web pages.
- **Database Management:** Utilize SQLAlchemy for efficient data storage.
- **User-Friendly Interface:** Explore and search your data using an intuitive web interface built with Flask.
- **Customizability:** Configure web crawling targets and search functionality to meet your unique needs.
- **Reliable Operation:** Robust error handling and data validation ensure dependable performance.

## Getting Started

To embark on your journey with our Elegant Web Crawler and Search Application, follow these straightforward steps:

### Prerequisites

Before you get started, make sure you have the following prerequisites installed:

- **Python 3.x** :```sudo apt install python3```
- **Flask** : ```pip install flask```
- **SQLAlchemy** : ```pip install sqlalchemy```

### Installation

1. **Clone this repository to your local machine:**```git clone https://github.com/Quannggg/Crawler-Web.git```
2. **Navigate to the project directory:**```cd Crawler-Web```
3. **Create a virtual environment for the project (recommended):**```python -m venv venv```
4. **Activate the virtual environment:**
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```
5. **Install the required Python packages within the virtual environment using pip:**
- ```pip install beautifulsoup4```
- ```pip install requests```
- ```pip install sqlalchemy```
- ```pip install flask```
- ```pip install Flask-SocketIO```
## Note
For easy installation, use our [installation script](./install_crawler_web.sh).

### To use the installation script:
1. **Download and save the script to your Ubuntu machine.**

2. **Make the script executable:**
   ```
   chmod +x install_crawler_web.sh
   ```

3. **Run the script:**
   ```
   ./install_crawler_web.sh
   ```

## Usage
To make the most of our Elegant Web Crawler and Search Application, follow these steps:
1. **Start the Flask application by running the following command:** ```python app.py```
2. **Access the application in your web browser by visiting [http://localhost:8000/](http://localhost:8000/).**
## Web Crawling
To extract information from web pages and store it in the database, run the following command:```python extractInformation.py```

## New Version
You can get the information from the urls we provide and download it as .zip file
## Usage New Version 
To make the most of our Elegant Web Crawler and Search Application, follow these steps:
1. **Start the Flask application by running the following command:** ```python app.py```
2. **Access the application in your web browser by visiting [http://localhost:5000](http://localhost:8000/).**
3. **Select the list of urls you want and click the button** ```Start Processing```