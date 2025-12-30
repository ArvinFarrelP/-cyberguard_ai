# check_models.py
from django.conf import settings
import os
import sys
import django
import google.generativeai as genai

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyberguardai.settings')
django.setup()


# Get API key
API_KEY = getattr(settings, "GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = getattr(settings, "GOOGLE_API_KEY", "")

if not API_KEY:
    print("❌ No API key found in settings!")
    exit()

print(f"🔑 Using API key: {API_KEY[:15]}...")
genai.configure(api_key=API_KEY)

print("\n" + "="*50)
print("📋 AVAILABLE MODELS FOR YOUR ACCOUNT")
print("="*50)

try:
    models = genai.list_models()
    available_models = []

    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            model_name = model.name.split('/')[-1]
            available_models.append(model_name)
            print(f"✅ {model_name:25} - {model.display_name}")

    print("\n" + "="*50)
    print("🎯 RECOMMENDED MODELS TO USE:")
    print("="*50)

    # Prioritize certain models
    priority_order = [
        'gemini-1.0-pro',
        'gemini-pro',
        'gemini-1.5-pro',
        'gemini-1.5-pro-latest',
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'gemini-2.0-flash-exp',
        'gemini-2.0-flash',
    ]

    for model in priority_order:
        if model in available_models:
            print(f"🔥 USE THIS: '{model}'")
            break

    if not any(m in available_models for m in priority_order):
        print("⚠️ No standard models found. Try these:")
        for model in available_models[:5]:  # Show first 5
            print(f"   '{model}'")

except Exception as e:
    print(f"❌ Error: {str(e)}")
