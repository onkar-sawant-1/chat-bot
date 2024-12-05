import json
import sys
import uvicorn
import argparse
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI
from starlette.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configure templates
templates = Jinja2Templates(directory="templates")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize variables on startup
@app.on_event("startup")
async def startup_event():
    global sheet_url, sheet_name, google_api_key_file, openai_api_key_file, google_sheet_data, openai_client

    # Get environment variables
    sheet_url = os.getenv('SHEET_URL')
    sheet_name = os.getenv('SHEET_NAME')
    google_api_key_file = os.getenv('GOOGLE_API_KEY_FILE')
    openai_api_key_file = os.getenv('OPENAI_API_KEY_FILE')

    # Validate input parameters
    validate_parameters(sheet_url, sheet_name, google_api_key_file, openai_api_key_file)

    # Initialize OpenAI client
    openai_client = OpenAI(api_key=json.load(open(openai_api_key_file))['api_key'])

    # Get Google Sheet data
    google_sheet_data = get_google_sheet_data(sheet_url, sheet_name, google_api_key_file)
    print("Google Sheet data initialized.")


# Function to validate input parameters
def validate_parameters(sheet_url, sheet_name, google_api_key_file, openai_api_key_file):
    try:
        if not sheet_url or not sheet_url.startswith("https://docs.google.com/spreadsheets/"):
            raise ValueError("Invalid Google Sheet URL")
        if not sheet_name:
            raise ValueError("Sheet name cannot be empty")
        if not google_api_key_file:
            raise ValueError("Google API key file name cannot be empty")
        if not openai_api_key_file:
            raise ValueError("OpenAI API key file name cannot be empty")
    except ValueError as e:
        print(f"Error: {e}")
        print("Usage: SHEET_URL=<url> SHEET_NAME=<name> GOOGLE_API_KEY_FILE=<file> OPENAI_API_KEY_FILE=<file> python ChatBot.py")
        sys.exit(1)


# Function to initialize the Google Sheets API
def init_google_sheets_api(google_api_key_file):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_api_key_file, scope)
    client = gspread.authorize(creds)
    return client


# Function to get data from Google Sheet
def get_google_sheet_data(sheet_url, sheet_name, google_api_key_file):
    client = init_google_sheets_api(google_api_key_file)
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    return sheet.get_all_values()


# Function to get response from OpenAI API
def get_openai_response(prompt, google_sheet_data):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant. Use the following data to answer questions if possible: {google_sheet_data}"},
        {"role": "user", "content": prompt}
    ]
    response = openai_client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=messages
    )
    return response.choices[0].message.content


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.post('/submit', response_class=HTMLResponse)
async def submit(request: Request, prompt: str = Form(...)):
    try:
        # Get response from OpenAI API
        response = get_openai_response(prompt, google_sheet_data)
        print(response)

        return templates.TemplateResponse('index.html', {"request": request, "response": response})
    except Exception as e:
        return templates.TemplateResponse('index.html', {"request": request, "response": f"Error: {str(e)}"})


if __name__ == "__main__":
    uvicorn.run("ChatBot:app", host="0.0.0.0", port=8000, reload=True)

# Example command to run the application with original values:
# SHEET_URL="https://docs.google.com/spreadsheets/d/1FI1OW8F6Dp312Rv0SBu1HbRVlMZy94Gmtj9GvhcDgBA/edit?usp=sharing" SHEET_NAME="Sheet1" GOOGLE_API_KEY_FILE="google_api_key.json" OPENAI_API_KEY_FILE="secrets.json" python ChatBot.py