from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from transformers import AutoProcessor, Gemma3ForConditionalGeneration
from PIL import Image
import requests
import torch
import os
import uvicorn

app = FastAPI(title="Gemma API", description="API for accessing the Gemma 3 model")

# Secure API Key (use environment variable)
API_KEY = "0a1cd8e325e5525b72c3fab8c11a2cd10017ea8d538c5b9adaae4b452ada8c32"

# Load Hugging Face Model and Processor
model_id = "google/gemma-3-27b-it"

try:
    model = Gemma3ForConditionalGeneration.from_pretrained(
        model_id, device_map={"layer_0": "cuda:0", "layer_1": "cuda:1"}
    ).eval()
    processor = AutoProcessor.from_pretrained(model_id)
except Exception as e:
    raise RuntimeError(f"Failed to load model or processor: {str(e)}")

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
        # Prepare the input for the model
        messages = [
            {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."}]},
            {"role": "user", "content": [{"type": "text", "text": request.text}]}
        ]

        # If an image URL is provided, process the image
        if request.image_url:
            try:
                image = Image.open(requests.get(request.image_url, stream=True).raw)
                messages[1]["content"].append({"type": "image", "image": image})
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image URL: {str(e)}")

        inputs = processor.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=True,
            return_dict=True, return_tensors="pt"
        ).to(model.device, dtype=torch.bfloat16)

        input_len = inputs["input_ids"].shape[-1]

        # Generate the response
        with torch.inference_mode():
            generation = model.generate(**inputs, max_new_tokens=200, do_sample=True)
            generation = generation[0][input_len:]

        # Decode the response
        response_text = processor.decode(generation, skip_special_tokens=True).strip()

        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run("model:app", host="0.0.0.0", port=8000, reload=False)