# reciept-tracker

  A basic app to allow users to upload receipt photo for safe keeping, but also including AI OCR integration for detailed breakdown of information within the receipts such as total spending, top areas of spending, top stores, payment type usage, etc.
  
## Installation:
  Running `poetry install` in the project's root directory *should* handle managing the environment and installing all dependencies. NOTE, this requires you to have poetry already installed. Should have a comprehensive list of all dependencies eventually in case you'd like to install manually without a venv, but for now, you at least need:
  - pandas
  - streamlit
  - google.genai
  - pillow

After installation, you can run `streamlit run Dashboard.py` either through `poetry run`, or however best suits your environment setup if manually/alternatively built.

## TODO: 
- Manual Receipt management (deletion, editing)
- Search feature for dashboard
- Detailed breakdown (spending for each category, pie charts?)
- Aesthetics


