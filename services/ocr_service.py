from utils.extract_receipt import extract_receipt_details
from config.settings import LOG_LEVEL

def upload_receipt(image_path):
    receiptData = extract_receipt_details(image_path)
    if LOG_LEVEL == 1:
        print(receiptData)
    return receiptData