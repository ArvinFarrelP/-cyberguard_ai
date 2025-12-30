# test_gemini.py
import os
import google.generativeai as genai

# Test 1: Cek environment variable
print("🔍 Checking environment variables...")
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in environment variables!")
    print("   Pastikan sudah di-set di Railway Variables")
    exit(1)

print(f"✅ API Key found: {api_key[:15]}...")

# Test 2: Konfigurasi dan list models
print("\n🔍 Listing available models...")
try:
    genai.configure(api_key=api_key)

    # List semua model yang tersedia
    models = genai.list_models()

    print(f"📋 Total models available: {len(models)}")
    print("\nModels with 'generateContent' support:")
    print("-" * 50)

    available_models = []
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"  • {m.name}")

    print("-" * 50)
    print(
        f"✅ Found {len(available_models)} models with generateContent support")

    # Test 3: Coba model yang mungkin cocok
    print("\n🧪 Testing models one by one...")

    test_models = [
        'models/gemini-2.0-flash',
        'models/gemini-1.5-flash-latest',
        'models/gemini-pro',
        'models/gemini-2.0-flash-exp',
        'models/gemini-2.5-flash-exp',
        'models/gemini-2.0-flash-001',
    ]

    successful_models = []

    for model_name in test_models:
        try:
            print(f"  Testing: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello", timeout=5)

            if response.text:
                successful_models.append(model_name)
                print(f"    ✅ Works!")
            else:
                print(f"    ⚠️ No response text")

        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg:
                print(f"    ❌ Model not found (404)")
            elif 'quota' in error_msg.lower():
                print(f"    ❌ Quota exceeded")
            elif 'permission' in error_msg.lower():
                print(f"    ❌ Permission denied")
            else:
                print(f"    ❌ Error: {error_msg[:60]}...")

    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS:")
    print("="*50)

    if successful_models:
        print("✅ WORKING MODELS:")
        for model in successful_models:
            print(f"  • {model}")
        print(
            f"\n💡 Use this in your views.py: model_name = '{successful_models[0]}'")
    else:
        print("❌ NO WORKING MODELS FOUND")
        print("\n⚠️ Possible issues:")
        print("  1. API key invalid or blocked")
        print("  2. Billing not enabled (required for newer models)")
        print("  3. Region restriction")
        print("  4. API key from wrong project")

except Exception as e:
    print(f"❌ Fatal error: {str(e)}")
