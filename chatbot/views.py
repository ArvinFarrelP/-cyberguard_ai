import time
import random
import google.generativeai as genai
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# ==============================
# GEMINI CONFIG
# ==============================

GEMINI_API_KEY = (
    getattr(settings, "GEMINI_API_KEY", "")
    or getattr(settings, "GOOGLE_API_KEY", "")
)

if not GEMINI_API_KEY:
    print("❌ Gemini API Key NOT FOUND")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"✅ Gemini API configured with key: {GEMINI_API_KEY[:15]}...")

# ==============================
# CONFIGURATION
# ==============================

# Model priority list berdasarkan output check_models.py Anda
MODEL_PRIORITY_LIST = [
    # Utama: model ringan, kuota biasanya lebih besar[citation:10]
    "gemini-2.5-flash-lite",
    "gemma-3-4b-it",          # Alternatif: model Gemma, kuota terpisah
    "gemini-2.0-flash",       # Coba lagi model standar
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

# Retry configuration
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2  # seconds
MAX_RETRY_DELAY = 60     # seconds

# ==============================
# GEMINI HELPER WITH QUOTA HANDLING
# ==============================


def generate_with_model(model_name: str, prompt: str, max_retries: int = 2):
    """
    Generate content with specific model and retry logic
    """
    retry_count = 0

    while retry_count <= max_retries:
        try:
            print(
                f"  🔄 Attempt {retry_count + 1}/{max_retries + 1} with model '{model_name}'")

            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }
            )

            if response.text:
                print(f"  ✅ Model '{model_name}' SUCCESS!")
                return response.text.strip()
            else:
                return "⚠️ Tidak ada respons dari model."

        except Exception as e:
            error_msg = str(e)
            retry_count += 1

            # Check error type
            if "429" in error_msg or "quota" in error_msg.lower() or "exceeded" in error_msg.lower():
                print(f"  ⚠️ Quota exceeded for '{model_name}'")

                # Extract retry delay from error message if available
                retry_delay = INITIAL_RETRY_DELAY * \
                    (2 ** retry_count)  # Exponential backoff

                # Try to parse retry time from error
                if "retry in" in error_msg.lower():
                    try:
                        # Extract seconds from error message
                        import re
                        match = re.search(
                            r'retry in (\d+\.?\d*)s', error_msg.lower())
                        if match:
                            retry_delay = float(match.group(1))
                            print(
                                f"  ⏰ Using extracted retry delay: {retry_delay}s")
                    except:
                        pass

                # Add jitter to avoid thundering herd
                retry_delay += random.uniform(0, 2)
                retry_delay = min(retry_delay, MAX_RETRY_DELAY)

                if retry_count <= max_retries:
                    print(f"  ⏳ Waiting {retry_delay:.1f}s before retry...")
                    time.sleep(retry_delay)
                else:
                    print(f"  ❌ Max retries reached for '{model_name}'")
                    return None

            elif "404" in error_msg or "not found" in error_msg.lower():
                print(f"  ❌ Model '{model_name}' not found")
                return None

            else:
                print(f"  ❌ Error with '{model_name}': {error_msg[:100]}")
                return None

    return None


def generate_gemini_reply(user_input: str) -> str:
    """
    Generate reply from Gemini AI with smart model switching and quota handling
    """
    print(f"📝 User input: {user_input[:50]}...")

    # Create optimized prompt
    prompt = f"""
Anda adalah CyberGuardAI, asisten keamanan siber profesional.
Jawab dengan bahasa Indonesia yang jelas dan praktis.

**Pertanyaan:**
{user_input}

**Format jawaban:**
1. 📊 Analisis singkat tentang masalah keamanan
2. 🛠️ Solusi / langkah-langkah konkret
3. 🛡️ Tips pencegahan untuk masa depan

Gunakan bahasa yang mudah dipahami dan berikan contoh praktis jika diperlukan.
"""

    # Try models in priority order
    for model_name in MODEL_PRIORITY_LIST:
        print(f"\n🔄 Trying model: {model_name}")

        result = generate_with_model(model_name, prompt, max_retries=1)

        if result:
            return result

    # If all models failed due to quota, try a simpler approach
    print("\n⚠️ All primary models failed. Trying emergency fallback...")

    # Emergency fallback: Very short prompt with Gemma model
    try:
        emergency_models = ["gemma-3-4b-it",
                            "gemma-3-12b-it", "gemini-2.0-flash-lite"]

        for model_name in emergency_models:
            try:
                print(f"  🆘 Emergency try with '{model_name}'")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"Jawab singkat dalam bahasa Indonesia: {user_input}",
                    generation_config={"max_output_tokens": 256}
                )
                if response.text:
                    return response.text.strip()
            except:
                continue
    except:
        pass

    # Final fallback message
    quota_message = """
❌ **QUOTA HABIS / BILLING REQUIRED**

Semua model Gemini telah melebihi batas quota gratis.

**Solusi:**
1. **Aktifkan Billing** di Google Cloud Console
   - Buka: https://console.cloud.google.com
   - Pilih project → Billing → Enable Billing
   - Dapatkan $300 credit gratis (new users)

2. **Buat API Key Baru** dari project baru
   - Buka: https://aistudio.google.com/apikey
   - Create new project → Generate new API key

3. **Tunggu quota reset** (biasanya 24 jam)

Chatbot akan bekerja normal setelah quota tersedia.
"""

    return quota_message


# ==============================
# VIEWS
# ==============================

def home_view(request):
    """Main homepage view"""
    return render(request, "chatbot/index.html")


@require_POST
def chat_api(request):
    """API endpoint for AJAX chat requests"""
    user_input = request.POST.get("user_input", "").strip()

    if not user_input:
        return JsonResponse({
            "success": False,
            "error": "Pesan tidak boleh kosong",
            "bot_reply": "⚠️ Silakan ketik pesan terlebih dahulu."
        })

    if not GEMINI_API_KEY:
        return JsonResponse({
            "success": False,
            "error": "API Key Gemini belum dikonfigurasi",
            "bot_reply": "🔑 Error: API Key tidak ditemukan. Pastikan GEMINI_API_KEY sudah diatur."
        })

    try:
        # Log the request
        print(f"\n" + "="*50)
        print(f"📨 Chat API Request: '{user_input}'")
        print("="*50)

        start = time.time()
        bot_reply = generate_gemini_reply(user_input)
        elapsed = int((time.time() - start) * 1000)

        print(f"\n⏱️ Total response time: {elapsed}ms")
        print("="*50)

        # Check if it's a quota error message
        is_quota_error = "QUOTA HABIS" in bot_reply or "billing" in bot_reply.lower()

        return JsonResponse({
            "success": not is_quota_error,
            "user_input": user_input,
            "bot_reply": bot_reply,
            "response_time": elapsed,
            "is_quota_error": is_quota_error,
            "debug": f"Models tried: {MODEL_PRIORITY_LIST[:3]}"
        })

    except Exception as e:
        error_msg = f"Server Error: {str(e)}"
        print(f"❌ {error_msg}")

        return JsonResponse({
            "success": False,
            "error": error_msg,
            "bot_reply": f"❌ Error Server: {str(e)[:150]}"
        })


def chatbot_view(request):
    """Legacy view for traditional form submission"""
    if request.method == "POST":
        user_input = request.POST.get("user_input", "").strip()

        if not user_input:
            return render(request, "chatbot/index.html", {
                "error": "Pesan tidak boleh kosong",
                "bot_reply": "⚠️ Silakan ketik pesan terlebih dahulu."
            })

        if not GEMINI_API_KEY:
            return render(request, "chatbot/index.html", {
                "error": "API Key tidak ditemukan",
                "bot_reply": "🔑 Error: GEMINI_API_KEY belum dikonfigurasi di settings."
            })

        try:
            print(f"\n📨 Chatbot View Request: '{user_input}'")

            start = time.time()
            bot_reply = generate_gemini_reply(user_input)
            elapsed = int((time.time() - start) * 1000)

            print(f"✅ Response generated in {elapsed}ms")

            return render(request, "chatbot/index.html", {
                "user_input": user_input,
                "bot_reply": bot_reply,
                "response_time": elapsed,
                "success": "QUOTA HABIS" not in bot_reply
            })

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error in chatbot_view: {error_msg}")

            return render(request, "chatbot/index.html", {
                "error": error_msg,
                "bot_reply": f"❌ Error: {error_msg[:100]}",
                "user_input": user_input
            })

    # GET request - render empty chat page
    return render(request, "chatbot/index.html")


# ==============================
# UTILITY FUNCTIONS
# ==============================

def check_model_availability():
    """Check which models are currently available"""
    print("\n🔍 Checking model availability...")

    available_models = []
    test_prompt = "Halo"

    for model_name in MODEL_PRIORITY_LIST + ["gemma-3-4b-it", "gemma-3-12b-it"]:
        try:
            print(f"  Testing '{model_name}'...", end=" ")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                test_prompt, request_options={"timeout": 5})
            available_models.append(model_name)
            print("✅")
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str:
                print(f"⚠️ (Quota)")
            elif "404" in error_str:
                print(f"❌ (Not Found)")
            else:
                print(f"❌ ({error_str[:30]})")

    print(f"\n📊 Available models: {available_models}")
    return available_models


def get_quota_status():
    """Simulate quota status check"""
    print("\n📊 Simulating quota status...")
    print("⚠️ Note: Actual quota check requires Google Cloud API")
    print("\nUntuk cek quota sebenarnya:")
    print("1. Buka: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas")
    print("2. Pilih project Anda")
    print("3. Lihat 'Quota' untuk generate_content_free_tier")
    print("\nUntuk enable billing:")
    print("1. Buka: https://console.cloud.google.com/billing")
    print("2. Pilih project → Enable Billing")
    print("3. Dapatkan $300 credit gratis (new users)")

    return "Manual check required"


# ==============================
# QUOTA MANAGEMENT HELPERS
# ==============================

def suggest_quota_solution():
    """Provide detailed quota solution"""
    solutions = [
        "🎯 **SOLUSI 1: AKTIFKAN BILLING**",
        "   - Buka: https://console.cloud.google.com/billing",
        "   - Enable Billing dengan credit card",
        "   - Dapatkan $300 free credit (90 hari)",
        "   - Set budget alert ($5/bulan)",
        "",
        "🎯 **SOLUSI 2: BUAT API KEY BARU**",
        "   - Buka: https://aistudio.google.com/apikey",
        "   - Buat project BARU (Create new project)",
        "   - Generate API key dari project baru",
        "   - Ganti GEMINI_API_KEY di Railway/.env",
        "",
        "🎯 **SOLUSI 3: GUNAKAN ALTERNATIF**",
        "   - Coba besok (quota reset setiap 24 jam)",
        "   - Gunakan API key dari akun Google lain",
        "   - Minta API key dari teman (sementara)",
    ]

    return "\n".join(solutions)


# ==============================
# QUICK TEST FUNCTION
# ==============================

def quick_test():
    """Quick test of the chatbot"""
    print("\n" + "="*60)
    print("🤖 CYBERGUARDAI QUICK TEST")
    print("="*60)

    test_messages = ["Halo", "Apa itu firewall?",
                     "Bagaimana membuat password kuat?"]

    for msg in test_messages:
        print(f"\n📤 Testing: '{msg}'")
        print("-" * 40)

        try:
            result = generate_gemini_reply(msg)
            print(f"📥 Result: {result[:100]}...")
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}")

    print("\n" + "="*60)
    print("✅ Quick test completed")
    print("="*60)
