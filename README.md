# Gemma 3 Deployment

This repository provides instructions on how to deploy the **Gemma-3-27B-it** model on an Azure Virtual Machine (VM). The deployment utilizes **FastAPI** to create an API endpoint secured with an API key.

## Features
- Deploy **Gemma-3-27B-it** on an Azure VM.
- Create a BASE URL using **FastAPI**.
- Secure the API with an **API key**.
- Provide a client script to interact with the deployed model.

## Files
- **main.py** - FastAPI-based deployment script for the model on Azure VM.
- **client.py** - Client code to interact with the deployed API.

## Requirements
Ensure you have the following installed before proceeding:
- Python 3.8+
- FastAPI
- Uvicorn
- Transformers
- Requests

