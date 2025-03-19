import requests

def predict_text(text, api_key, base_url, image_url=None):
    """
    Simple function to query the Gemma model API.
    
    Args:
        text (str): The text prompt to send to the model
        api_key (str): Your API key for authentication
        base_url (str): The base URL of the API endpoint
        image_url (str, optional): The URL of an image to send to the model
        
    Returns:
        The model's response text
    """
    headers = {"X-API-Key": api_key}
    data = {"text": text, "image_url": image_url}
    
    try:
        response = requests.post(
            f"{base_url}/predict/", 
            json=data, 
            headers=headers
        )
        response.raise_for_status()
        return response.json()["response"]
        
    except requests.exceptions.RequestException as e:
        return f"Error connecting to the API: {e}"

# Example usage
if __name__ == "__main__":
    API_KEY = "0a1cd8e325e5525b72c3fab8c11a2cd10017ea8d538c5b9adaae4b452ada8c32"
    BASE_URL = "http://127.0.0.1:8000"
    
    while True:
        user_input = input("\nEnter your prompt (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        image_url = input("Enter image URL (optional, press enter to skip): ").strip()
        image_url = image_url if image_url else None
            
        response = predict_text(user_input, API_KEY, BASE_URL, image_url)
        if isinstance(response, str):
            print("\nModel response:", response)
        else:
            print("\nModel response:", str(response))