from config.env import load_config
load_config()

import streamlit as st
import os
from datetime import datetime
from services.db_service import get_all_receipts
from config.settings import UPLOAD_FOLDER

st.header("📊 Dashboard")
