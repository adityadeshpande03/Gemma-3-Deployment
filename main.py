from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from transformers import AutoProcessor, Gemma3ForConditionalGeneration
import torch
import requests
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI(title="Gemma API", 
              description="API for accessing the Gemma 3 model with multimodal capabilities")

# Secure API Key (use environment variable)
API_KEY = '0a1cd8e325e5525b72c3fab8c11a2cd10017ea8d538c5b9adaae4b452ada8c32'

# Load model and processor
model_id = "google/gemma-3-27b-it"

try:
    model = Gemma3ForConditionalGeneration.from_pretrained(
        model_id, 
        use_fast=True,
        device_map="auto",
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
    ).eval()
    
    processor = AutoProcessor.from_pretrained(model_id)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {str(e)}")

class ContentItem(BaseModel):
    type: str
    text: str | None = None
    image: str | None = None

class ChatMessage(BaseModel):
    role: str
    content: list[ContentItem]

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    """Middleware to check API Key"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key is required")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

def load_image_from_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load image: {str(e)}")

@app.get("/")
def home():
    return {"message": "Gemma API is running!", "status": "online"}

@app.post("/chat/")
def chat(request: ChatRequest, x_api_key: str = Header(None, alias="X-API-Key")):
    verify_api_key(x_api_key)
    
    try:
        # Process any images in the messages
        processed_messages = []
        for message in request.messages:
            processed_content = []
            for content_item in message.content:
                if content_item.type == "image" and content_item.image:
                    image = load_image_from_url(content_item.image)
                    processed_content.append({"type": "image", "image": image})
                else:
                    processed_content.append({"type": "text", "text": content_item.text})
            
            processed_messages.append({
                "role": message.role,
                "content": processed_content
            })
        
        # Apply chat template and generate response
        inputs = processor.apply_chat_template(
            processed_messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(model.device)
        
        input_len = inputs["input_ids"].shape[-1]
        
        with torch.inference_mode():
            generation = model.generate(**inputs, max_new_tokens=100, do_sample=False)
            generation = generation[0][input_len:]
        
        decoded = processor.decode(generation, skip_special_tokens=True)
        
        return {"response": decoded}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main2:app", host="0.0.0.0", port=8000, reload=False)