from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from transformers import pipeline
import torch
import os
import uvicorn

app = FastAPI(title="Gemma API", description="API for accessing the Gemma 3 model")

# Secure API Key (use environment variable)
API_KEY = '0a1cd8e325e5525b72c3fab8c11a2cd10017ea8d538c5b9adaae4b452ada8c32'

# Load Hugging Face Model on GPU (if available)
pipe = pipeline(
    "text-generation",  # Changed back to text-generation
    model="google/gemma-3-12b-it",
    device_map="auto", #if torch.cuda.is_available() else -1,
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    use_cache=True,
)

class TextRequest(BaseModel):
    text: str
    image_url: str | None = None

def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    """Middleware to check API Key"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key is required")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
@app.get("/")
def home():
    return {"message": "Gemma API is running!", "status": "online"}

@app.post("/predict/")
def predict(request: TextRequest, x_api_key: str = Header(None, alias="X-API-Key")):
    verify_api_key(x_api_key)
    
    try:
        prompt = f"System: You are a helpful assistant.\nUser: {request.text}\nAssistant:"
        
        # Generate response
        output = pipe(prompt, max_new_tokens=100, do_sample=True)
        
        # Extract the assistant's response
        if isinstance(output, list) and len(output) > 0:
            full_text = output[0]['generated_text']
            response_text = full_text.split("Assistant:")[-1].strip()
        else:
            response_text = "No response generated"
            
        return {"response": response_text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)