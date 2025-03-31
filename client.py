import requests
import time
from typing import Optional, List, Dict

def chat_with_gemma(messages: List[Dict], api_key: str, base_url: str) -> Dict:
    """
    Function to query the Gemma model API with chat-style multimodal inputs.
    
    Args:
        messages (List[Dict]): List of chat messages with roles and content
        api_key (str): Your API key for authentication
        base_url (str): The base URL of the API endpoint
        
    Returns:
        dict: Contains the model's response and generation time
    """
    headers = {"X-API-Key": api_key}
    request_data = {"messages": messages}
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{base_url}/chat/", 
            json=request_data, 
            headers=headers
        )
        response.raise_for_status()
        end_time = time.time()
        generation_time = end_time - start_time
        return {
            "response": response.json()["response"],
            "generation_time": generation_time,
            "start_time": start_time,
            "end_time": end_time
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "response": f"Error connecting to the API: {e}",
            "generation_time": 0,
            "start_time": 0,
            "end_time": 0
        }

def create_message(role: str, text: Optional[str] = None, image_url: Optional[str] = None) -> Dict:
    """
    Helper function to create a properly formatted message.
    
    Args:
        role (str): "system", "user", or "assistant"
        text (str, optional): Text content
        image_url (str, optional): URL of an image
        
    Returns:
        Dict: Formatted message for the API
    """
    content = []
    if text:
        content.append({"type": "text", "text": text})
    if image_url:
        content.append({"type": "image", "image": image_url})
    return {"role": role, "content": content}

# Example usage
if __name__ == "__main__":
    API_KEY = "0a1cd8e325e5525b72c3fab8c11a2cd10017ea8d538c5b9adaae4b452ada8c32"
    BASE_URL = "http://127.0.0.1:8000"
    
    # Initial system message
    messages = [
        create_message(
            role="system",
            text="You are a helpful assistant."
        )
    ]
    
    total_generation_time = 0
    num_interactions = 0
    
    while True:
        print("\nCurrent conversation context:")
        for msg in messages:
            print(f"\n{msg['role'].capitalize()}:")
            for content in msg["content"]:
                if content["type"] == "text":
                    print(content["text"])
                else:
                    print(f"[Image: {content['image']}]")
        
        user_input = input("\nEnter your text (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            if num_interactions > 0:
                avg_generation_time = total_generation_time / num_interactions
                print(f"\nSession Statistics:")
                print(f"Total interactions: {num_interactions}")
                print(f"Total generation time: {total_generation_time:.2f} seconds")
                print(f"Average generation time: {avg_generation_time:.2f} seconds")
            break
            
        image_url = input("Enter image URL (optional, press enter to skip): ").strip()
        image_url = image_url if image_url else None
        
        # Add user message to conversation
        messages.append(create_message(
            role="user",
            text=user_input,
            image_url=image_url
        ))
        
        print("\nGenerating response...")
        result = chat_with_gemma(messages, API_KEY, BASE_URL)
        
        # Add assistant response to conversation
        messages.append(create_message(
            role="assistant",
            text=result["response"]
        ))
        
        # Update timing statistics
        total_generation_time += result["generation_time"]
        num_interactions += 1
        
        print(f"\nAssistant: {result['response']}")
        print(f"Generation time: {result['generation_time']:.2f} seconds")
        print(f"Start time: {time.strftime('%H:%M:%S', time.localtime(result['start_time']))}")
        print(f"End time: {time.strftime('%H:%M:%S', time.localtime(result['end_time']))}")