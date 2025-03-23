<center> # 🚀 Gemma 3 Deployment</center>

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

## 🚀 Deployment Steps

### 1️⃣ Clone the Repository
Run the following command to clone this repository:
```bash
git clone https://github.com/adityadeshpande03/Gemma-3-Deployment.git
cd Gemma-3-Deployment
```

### 2️⃣ Create a Virtual Environment
It is recommended to create a virtual environment before installing dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4️⃣ Start the FastAPI Server
Run the `main.py` script to start the API server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5️⃣ Test the API (Optional)
Once the server is running, you can test it using:
```bash
curl -X POST "http://your-vm-ip:8000/predict" \
     -H "Content-Type: application/json" \
     -H "API-Key: your_api_key" \
     -d '{"input_text": "Hello, how are you?"}'
```

### 6️⃣ Run the Client Script
Execute `client.py` to interact with the deployed model:
```bash
python client.py
```

---

Made with ❤️ by Adi | [GitHub Repository](https://github.com/adityadeshpande03/Gemma-3-Deployment)
