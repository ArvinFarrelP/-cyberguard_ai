# chatbot/ai/gemini_client.py
import google.generativeai as genai
import os
from django.conf import settings


def configure_gemini():
    """Configure Gemini API with proper error handling"""
    # Coba dari environment variable
    api_key = os.getenv('AIzaSyBNriuMvmemLME4xRkqJXJx0yXy2S-bgVU')

    # Jika tidak ada, coba dari settings
    if not api_key:
        try:
            api_key = settings.GEMINI_API_KEY
        except AttributeError:
            api_key = None

    # Jika masih tidak ada, tampilkan error
    if not api_key:
        print("⚠️ WARNING: GOOGLE_API_KEY not found!")
        print("Please create .env file with GOOGLE_API_KEY=your_key")
        return None

    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini API configured successfully")
        return genai.GenerativeModel(model_name="gemini-1.5-flash")
    except Exception as e:
        print(f"❌ Error configuring Gemini: {e}")
        return None


# Inisialisasi model
model = configure_gemini()


def ask_gemini(prompt):
    """Send prompt to Gemini API"""
    if model is None:
        return "Error: Gemini API not configured. Please check your API key."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini API: {str(e)}"
