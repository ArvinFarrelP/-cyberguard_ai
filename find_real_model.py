
# find_real_model.py
import google.generativeai as genai

API_KEY = "AIzaSyBNriuMvmemLME4xRkqJXJx0yXy2S-bgVU"

print("🔍 MENCARI MODEL GEMINI YANG TERSEDIA...")
print("=" * 60)

try:
    genai.configure(api_key=API_KEY)

    # List semua model
    models = genai.list_models()

    print("📋 MODEL YANG SUPPORT generateContent:")
    print("-" * 50)

    available_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            model_name = model.name
            short_name = model_name.split('/')[-1]
            available_models.append(short_name)
            print(f"✅ {short_name}")

    print(f"\n🎯 Total model tersedia: {len(available_models)}")

    if available_models:
        print(f"\n💡 Model pertama: {available_models[0]}")
        print("🧪 Testing model ini...")

        # Test model pertama
        try:
            test_model = genai.GenerativeModel(available_models[0])
            response = test_model.generate_content("Halo, tes koneksi 123")
            print(f"✅ TEST BERHASIL!")
            print(f"Response: {response.text[:100]}...")

            # Simpan ke file untuk digunakan
            with open('model_info.txt', 'w') as f:
                f.write(available_models[0])

            print(f"\n📁 Model disimpan ke: model_info.txt")

        except Exception as e:
            print(f"❌ Test gagal: {e}")

except Exception as e:
    print(f"❌ Error: {e}")
