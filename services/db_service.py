
import os
import json
from config.settings import UPLOAD_FOLDER

def save_receipt(data, image_name):
    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    image_base = os.path.splitext(image_name)[0]
    # Add image name to the data
    data["image_name"] = image_name

    # Use store name directly
    store_name = data.get("store_name", "unknown_store")
    # Create a JSON filename based on the image name (e.g., Walmart_20210726.json)
    json_filename = f"{store_name}_{image_base}.json"
    json_path = os.path.join(UPLOAD_FOLDER, json_filename)

    # Write the dictionary to the JSON file
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Receipt data saved to {json_path}")

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