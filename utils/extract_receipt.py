from PIL import Image
import os
import json
from google import genai
# pip install google.genai json Pillow
# Set the environment variable for the API key
# export GEMINI_API_KEY="your_api_key_here"
# Make sure to set the GEMINI_API_KEY environment variable in your shell or IDE

# Retrieve the API key from the environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("Error: GEMINI_API_KEY environment variable is not set.")

# Configure the client with the API key
client = genai.Client(api_key=api_key)

def extract_receipt_details(image_path):  
    # Open the image file
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return {}

    # Create the prompt
    prompt = """
    You are a helpful assistant analyzing receipt images.
    Extract the following details from the receipt:
    - Store name
    - Purchase date (in strict format of YYYY-MM-DD HH:MM:SS, default to current values for any unknown, for example if year or time is not shown)
    - Category of purchase (gas, restaurant, grocery, etc)
    - Subtotal
    - Total amount
    Return the result as a JSON object. Ensure that the structure and name of the keys is as follows:
    - store_name
    - purchase_date
    - category
    - subtotal
    - total_amount
    """

    try:
        # Send the prompt to the Gemini model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image, prompt]
        )

        # Extract the JSON content from the response
        candidates = response.candidates
        if not candidates or not candidates[0].content.parts:
            print("Empty or invalid response from genai API")
            return {}

        # Parse the JSON content from the first candidate's text
        json_text = candidates[0].content.parts[0].text.strip("```json\n").strip("```")
        details = json.loads(json_text)
        return details

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {}
    except AttributeError as e:
        print(f"Attribute error: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

# Example usage
#result = extract_receipt_details("/home/vboxuser/cloud/testproject/narrow-gasoline-receipt.jpg")
#print(result)
