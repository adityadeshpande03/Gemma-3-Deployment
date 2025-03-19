# 🚀 Gemma 3 Deployment

This repository provides instructions on how to deploy the **Gemma-3-27B-it** model on an Azure Virtual Machine (VM). The deployment utilizes **FastAPI** to create an API endpoint secured with an API key.

![image](https://github.com/user-attachments/assets/5bd9b6c5-8fa2-48ec-89cc-c88830ca756e)

## ✨ Features
- 🚀 Deploy **Gemma-3-27B-it** on an Azure VM.
- 🌐 Create a BASE URL using **FastAPI**.
- 🔒 Secure the API with an **API key**.
- 📡 Provide a client script to interact with the deployed model.

## 📂 Files
- 📝 **main.py** - FastAPI based deployment script for the model on Azure VM.
- 🖥️ **client.py** - Client code to interact with the deployed API.

## 📌 Requirements
Ensure you have the following installed before proceeding:
- 🐍 Python 3.8+
- ⚡ FastAPI
- 🔥 Uvicorn
- 🤗 Transformers
- 🌍 Requests
- 🖥️ GPU: NVIDIA A100 with 80GB storage

## 🚀 Running the Deployment & using Client Script

1️⃣ Install Dependencies

Run the following command to install the required dependencies:

pip install fastapi uvicorn transformers requests

2️⃣ Start the FastAPI Server

Run the main.py script to start the API server:

uvicorn main:app --host 0.0.0.0 --port 8000

If you want to run it in the background, use:

nohup uvicorn main:app --host 0.0.0.0 --port 8000 > output.log 2>&1 &

3️⃣ Test the API (Optional)

Once the server is running, you can test it using:

curl -X POST "http://your-vm-ip:8000/predict" \
     -H "Content-Type: application/json" \
     -H "API-Key: your_api_key" \
     -d '{"input_text": "Hello, how are you?"}'

4️⃣ Run the Client Script

Execute client.py to interact with the deployed model:

python client.py

---

Made with ❤️ by Adi | [GitHub Repository](https://github.com/adityadeshpande03/Gemma-3-Deployment)
