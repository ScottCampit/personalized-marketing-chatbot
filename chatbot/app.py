"""
Fine-tune GPT models
"""

import os
import openai
import streamlit as st

openai.api_key = os.environ["OPENAI_API_KEY"]