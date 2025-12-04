# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .ai.gemini_client import ask_gemini


# def chatbot_view(request):
#     context = {}

#     if request.method == "POST":
#         user_input = request.POST.get("user_input", "").strip()

#         if not user_input:
#             messages.error(request, "Masukkan pertanyaan terlebih dahulu!")
#         elif len(user_input) > 1000:
#             messages.error(request, "Pertanyaan terlalu panjang!")
#         else:
#             try:
#                 bot_reply = ask_gemini(user_input)
#                 context['user_input'] = user_input
#                 context['bot_reply'] = bot_reply
#             except Exception as e:
#                 messages.error(request, f"Terjadi kesalahan: {str(e)}")

#     return render(request, "chatbot/index.html", context)

# chatbot/views.py (COMPLETE SYSTEM FOR UAS)
from django.shortcuts import render
import google.generativeai as genai
import hashlib
import json
import os
import time


class CyberGuardAISystem:
    def __init__(self):
        self.api_key = "AIzaSyBNriuMvmemLME4xRkqJXJx0yXy2S-bgVU"
        self.cache_file = 'chatbot_cache.json'
        self.cache = self.load_cache()
        self.free_models = [
            'gemini-2.0-flash-lite',  # Paling hemat
            'gemini-2.0-flash',       # Alternatif
            'gemma-3-4b-it',          # Open source
        ]

    def load_cache(self):
        """Load cached responses"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def get_cache_key(self, question):
        """Generate cache key from question"""
        return hashlib.md5(question.lower().encode()).hexdigest()[:12]

    def get_cached_response(self, question):
        """Get response from cache"""
        key = self.get_cache_key(question)
        return self.cache.get(key)

    def cache_response(self, question, answer):
        """Cache the response"""
        key = self.get_cache_key(question)
        self.cache[key] = {
            'answer': answer,
            'timestamp': time.time(),
            'model': 'gemini-2.0-flash-lite'
        }
        self.save_cache()

    def get_api_response(self, question):
        """Try to get response from Gemini API"""
        for model_name in self.free_models:
            try:
                print(f"Mencoba model: {model_name}")

                # Configure
                genai.configure(api_key=self.api_key)

                # Create model
                model = genai.GenerativeModel(model_name)

                # Generate (hemat token)
                response = model.generate_content(
                    f"Sebagai ahli keamanan siber, jawab singkat: {question}",
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 250,  # Hemat token
                    }
                )

                if response.text:
                    # Cache the response untuk next time
                    self.cache_response(question, response.text)
                    return response.text

            except Exception as e:
                error_msg = str(e)
                if "quota" in error_msg or "429" in error_msg:
                    print(f"Quota habis untuk {model_name}")
                    time.sleep(1)  # Tunggu sebentar
                    continue
                else:
                    print(f"Error: {error_msg[:100]}")

        return None  # Semua model gagal

    def get_fallback_response(self, question):
        """Fallback jika API tidak bisa"""
        fallbacks = {
            'phishing': "Phishing: Jangan klik link email tak dikenal. Verifikasi pengirim.",
            'password': "Password: Minimal 12 karakter, campuran huruf, angka, simbol.",
            'malware': "Malware: Install antivirus, update software, backup data rutin.",
            'hacker': "Hacker: Gunakan firewall, VPN, dan autentikasi dua faktor.",
            'firewall': "Firewall: Aktifkan di router dan komputer untuk proteksi jaringan.",
            'ransomware': "Ransomware: Backup data 3-2-1 (3 copy, 2 media, 1 offsite).",
            'virus': "Virus: Scan reguler, hati-hati dengan USB, gunakan sandboxing.",
            'email': "Email keamanan: Verifikasi pengirim, jangan buka lampiran mencurigakan.",
            'wifi': "WiFi publik: Gunakan VPN, hindari transaksi sensitif.",
            'backup': "Backup: Rutin lakukan backup, simpan di cloud dan external drive.",
        }

        question_lower = question.lower()
        for keyword, answer in fallbacks.items():
            if keyword in question_lower:
                return f"🔒 {answer}"

        # Default response
        return f"""🤖 **CyberGuardAI**
        
Untuk pertanyaan "{question}", praktik keamanan siber terbaik:
1. **Update rutin** software & sistem
2. **Password kuat** dengan 2FA
3. **Backup data** secara berkala
4. **Waspada** terhadap social engineering

💡 *Tetap aman di dunia digital!*"""

    def ask(self, question):
        """Main method to get response"""
        if not question:
            return "Silakan tanyakan tentang keamanan siber."

        # 1. Cek cache dulu
        cached = self.get_cached_response(question)
        if cached:
            print("Menggunakan cached response")
            return cached.get('answer', '')

        # 2. Coba API
        print("Mencoba API...")
        api_response = self.get_api_response(question)
        if api_response:
            return api_response

        # 3. Fallback
        print("Menggunakan fallback response")
        return self.get_fallback_response(question)


# Global instance
chatbot_system = CyberGuardAISystem()


def chatbot_view(request):
    context = {}

    if request.method == "POST":
        user_input = request.POST.get("user_input", "").strip()

        if user_input:
            # Get response from system
            bot_reply = chatbot_system.ask(user_input)

            context['bot_reply'] = bot_reply
            context['user_input'] = user_input

    return render(request, "chatbot/index.html", context)
