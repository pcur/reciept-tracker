# reciept-tracker

  A basic app to allow users to upload receipt photo for safe keeping, but also including AI OCR integration for detailed breakdown of information within the receipts such as total spending, top areas of spending, top stores, payment type usage, etc.

## TODO: 
- basically everything

## Directory Breakdown

```
receipt_app/

│

├── app.py                  # Main Streamlit app

├── pages/                  # Separate pages like 'Dashboard', 'Upload'

│   ├── dashboard.py

│   └── upload.py

├── services/

│   ├── ocr_service.py      # Handles image upload and OCR/API call

│   └── db_service.py       # Handles all database interactions

├── utils/

│   └── helpers.py          # Text parsing, data validation, date handling, etc.

├── models/

│   └── receipt.py          # ORM model definitions (if using SQLAlchemy)

├── assets/

│   └── uploads/            # Local receipt image storage (at scale would be hosted online)

└── config                 

    ├── .env                # API Keys, private config

    ├── settings.py         # Generic app settings

    └── env.py              # loads settins into os env

```

