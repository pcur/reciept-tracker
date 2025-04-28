
import os
import json
from config.settings import UPLOAD_FOLDER

def save_receipt(data, image_name):
    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # Add image name to the data
    data["image_name"] = image_name + ".jpg"

    # Create a JSON filename based on the image name (e.g., Walmart_20210726.json)
    json_filename = f"{image_name}.json"
    json_path = os.path.join(UPLOAD_FOLDER, json_filename)

    # Write the dictionary to the JSON file
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Receipt data saved to {json_path}")

def save_receipt_update(receipt, filename):
    json_filename = os.path.splitext(filename)[0] + ".json"  # ensure .json extension
    file_path = os.path.join(UPLOAD_FOLDER, json_filename)
    try:
        with open(file_path, "w") as f:
            json.dump(receipt, f, indent=4)
    except Exception as e:
        st.error(f"Failed to save receipt: {e}")
        
def get_all_receipts():
    receipts = []

    if not os.path.exists(UPLOAD_FOLDER):
        return receipts  # No uploads yet

    for file_name in os.listdir(UPLOAD_FOLDER):
        if file_name.endswith(".json"):
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            try:
                with open(file_path, "r") as f:
                    receipt_data = json.load(f)
                    receipts.append(receipt_data)
            except Exception as e:
                print(f"Error loading {file_name}: {e}")

    return receipts

def delete_receipt(image_name_without_extension):
    # Assuming receipts are stored as JSON and images
    receipt_path = os.path.join(UPLOAD_FOLDER, f"{image_name_without_extension}.json")
    image_path = os.path.join(UPLOAD_FOLDER, f"{image_name_without_extension}.jpg")
    
    if os.path.exists(receipt_path):
        os.remove(receipt_path)
    
    if os.path.exists(image_path):
        os.remove(image_path)
