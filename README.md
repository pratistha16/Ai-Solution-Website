# AI-Solution Django Project

## Overview

This is a Django project for an AI solutions company. It includes features for managing events, solutions, blogs, articles, gallery items, and more.

### Features:
- Event management and registration
- Gallery for event images
- Solutions & services display
- Article management
- Team management

Additionally, a **chatbot** can interact with the website's features using the **API**.

---

## Prerequisites

1. Python 3.10 or higher
2. Virtual environment (recommended)

---

## Setup Guide

### Step 1: Clone the repository

Clone the repository from GitHub:

```bash
git clone <https://github.com/pratistha16/Ai-Solution-Website>
cd <aisolution>

Step 2: Set up a Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

python -m venv venv


Activate the virtual environment:

On Windows:

venv\Scripts\activate


On macOS/Linux:

source venv/bin/activate

Step 3: Install Dependencies

Install all required Python libraries:

pip install -r requirements.txt

Step 4: Set Up the Database

Make sure you have a working SQLite or PostgreSQL database set up. Then, run the following commands to apply the migrations:

python manage.py migrate

Step 5: Create Superuser (Optional)

To access the Django Admin panel, you’ll need a superuser. Create one by running:

python manage.py createsuperuser


Follow the prompts to set up the admin account.

Step 6: Run the Development Server

Start the server to view your project in the browser:

python manage.py runserver


Visit http://127.0.0.1:8000 to view the project in your browser.




AI Solutions Chatbot Setup

This repository provides a chatbot built with FastAPI that serves as an AI assistant. The chatbot interacts with users through a conversational interface and is powered by an AI model (e.g., OpenAI, or custom model). You will set up the backend using FastAPI, run the application using Uvicorn, and interact with it.

1.
Navigate to right Path
cd ai-solutions/chatbot

2. Set Up a Virtual Environment (Optional but recommended)

Create and activate a virtual environment to manage your Python dependencies:

python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install Required Dependencies

Install the required dependencies using pip:

pip install -r requirements.txt


This command will install all the necessary packages, including FastAPI, Uvicorn, and any other dependencies listed in requirements.txt.

Setting Up the Backend
1. Configuration

create .env 
- set your GOOGLE_API_KEY
- set your LANGCHAIN_API_KEY
For example 
GOOGLE_API_KEY = AIdhdhdbhdbfbhfbhjb_NXGhduhde
LANGCHAIN_API_KEY = lsv2_pt_4874755704570Jbdfbf88784sd_64483ffhb7

2. The retriever.py Script


Running the Application
1. Start the FastAPI Application with Uvicorn

FastAPI can be run using Uvicorn, which is an ASGI server. To start the application, run the following command:

uvicorn app:app --reload --host 0.0.0.0 --port 8001


app:app tells Uvicorn where to find your FastAPI application instance (app in the app.py file).

--reload makes Uvicorn restart the server on code changes.

--host 0.0.0.0 allows the app to be accessible on your local network.

--port 8001 specifies the port number.

2. Access the API

Once the server is running, you can access the FastAPI app by navigating to:

http://127.0.0.1:8001/docs


This will open the interactive Swagger documentation where you can test the chatbot API directly from the browser.

Testing the Chatbot

You can interact with the chatbot API by sending a POST request to the /chat endpoint. Here's an example using curl or a REST client (e.g., Postman or Insomnia):

curl -X 'POST' \
  'http://127.0.0.1:8001/chat' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Hello, chatbot!"
}'


This should return a response similar to:

{
  "response": "Hello! How can I assist you today?"
}


If everything is set up correctly, the chatbot should respond based on the AI model logic defined in retriever.py.
