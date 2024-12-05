# ChatBot Application

## Overview
This is a simple web-based ChatBot application built with FastAPI and HTML that interacts with OpenAI's language model to provide conversational responses. It also integrates with Google Sheets for additional contextual data. The application features a chatbot-like user interface where users can submit prompts and view bot responses.

## Features
- **Chatbot UI**: User-friendly interface that mimics a chat experience.
- **Google Sheets Integration**: Uses data from a Google Sheet to enhance the contextuality of responses.

## Technologies Used
- **FastAPI**: A modern web framework for building APIs with Python.
- **Bootstrap 5**: For styling the user interface and making the application look visually appealing.
- **Jinja2 Templates**: Used for rendering dynamic HTML content.
- **OpenAI API**: For generating responses to user prompts.
- **Google Sheets API**: To fetch data from a Google Sheet.

## Prerequisites
To run this application, you will need:
- **Python 3.7+**
- **Google API credentials** in JSON format to access the Google Sheets.
- **OpenAI API key** to interact with the OpenAI GPT-3.5 model.
- **Uvicorn** to serve the FastAPI application.

## Installation
1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file or set the following environment variables:
    - `SHEET_URL`: URL of the Google Sheet.
    - `SHEET_NAME`: Name of the sheet tab to use.
    - `GOOGLE_API_KEY_FILE`: Path to the Google API key JSON file.
    - `OPENAI_API_KEY_FILE`: Path to the OpenAI API key JSON file.

## Running the Application
To run the application, use the following command:

```bash
python chatbot.py
```

Access the application in your browser at `http://localhost:8000`.

## Usage
1. **Open the application** in your browser.
2. **Enter your prompt** in the input box and click "Send".
3. The bot uses information from the Google Sheet to enhance its answers if relevant.

## File Structure
- `ChatBot.py`: Main application script.
- `templates/index.html`: HTML template for the web interface.
- `requirements.txt`: Contains the list of Python packages required to run the app.

## Example Environment Variables
Here is an example of the environment variables you can set in a `.env` file:

```env
SHEET_URL="https://docs.google.com/spreadsheets/d/your_sheet_id/edit"
SHEET_NAME="Sheet1"
GOOGLE_API_KEY_FILE="google_api_key.json"
OPENAI_API_KEY_FILE="secrets.json"
```
