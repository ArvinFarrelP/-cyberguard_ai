import os
import google.generativeai as genai
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_POST

# Configure Gemini API
try:
    # Gunakan environment variable dari settings.py
    GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', '') or getattr(
        settings, 'GOOGLE_API_KEY', '')

    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        print(
            f"DEBUG: Gemini API configured. Key length: {len(GEMINI_API_KEY)}")
    else:
        print("DEBUG: WARNING - No API key found!")
except Exception as e:
    print(f"DEBUG: Error configuring Gemini: {str(e)}")


def home_view(request):
    """View utama untuk halaman chatbot"""
    return render(request, 'chatbot/index.html')


@require_POST
def chat_api(request):
    """API endpoint untuk menerima dan memproses pesan"""
    try:
        user_input = request.POST.get('user_input', '').strip()

        if not user_input:
            return JsonResponse({
                'success': False,
                'error': 'Pesan tidak boleh kosong'
            })

        print(f"DEBUG: Received message: '{user_input}'")

        # Cek API key
        GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', '') or getattr(
            settings, 'GOOGLE_API_KEY', '')

        if not GEMINI_API_KEY:
            error_msg = "ERROR: API Key tidak ditemukan. Pastikan GEMINI_API_KEY sudah diatur di Railway Variables."
            print(error_msg)
            return JsonResponse({
                'success': False,
                'error': error_msg,
                'bot_reply': error_msg
            })

        try:
            # Gunakan model Gemini yang stabil
            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            # Tambahkan konteks cybersecurity
            prompt = f"""Anda adalah CyberGuardAI, asisten keamanan siber profesional. 
            Berikan jawaban yang jelas, praktis, dan relevan untuk pertanyaan keamanan siber.
            
            Pertanyaan: {user_input}
            
            Jawab dengan format:
            1. Analisis singkat
            2. Solusi/langkah-langkah
            3. Tips pencegahan
            4. Sumber/referensi jika diperlukan
            
            Gunakan bahasa yang mudah dipahami."""

            start_time = time.time()
            response = model.generate_content(prompt)
            elapsed_time = int((time.time() - start_time) * 1000)

            bot_reply = response.text if response.text else "Maaf, saya tidak dapat memproses permintaan Anda saat ini."

            print(f"DEBUG: Gemini response received in {elapsed_time}ms")

            return JsonResponse({
                'success': True,
                'user_input': user_input,
                'bot_reply': bot_reply,
                'response_time': elapsed_time
            })

        except Exception as api_error:
            error_msg = f"ERROR menghubungi AI: {str(api_error)}"
            print(f"DEBUG: {error_msg}")
            return JsonResponse({
                'success': False,
                'error': str(api_error),
                'bot_reply': f"❌ Error menghubungi AI: {str(api_error)}"
            })

    except Exception as e:
        error_msg = f"ERROR sistem: {str(e)}"
        print(f"DEBUG: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'bot_reply': f"❌ Error sistem: {str(e)}"
        })


def chatbot_view(request):
    """View untuk halaman chatbot (legacy support)"""
    if request.method == 'POST':
        try:
            user_input = request.POST.get('user_input', '').strip()

            if not user_input:
                return render(request, 'chatbot/index.html', {
                    'error': 'Pesan tidak boleh kosong'
                })

            print(f"DEBUG: Received message via POST: '{user_input}'")

            # Cek API key
            GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', '') or getattr(
                settings, 'GOOGLE_API_KEY', '')

            if not GEMINI_API_KEY:
                error_msg = "ERROR: API Key tidak ditemukan. Pastikan GEMINI_API_KEY sudah diatur di Railway Variables."
                print(error_msg)
                return render(request, 'chatbot/index.html', {
                    'user_input': user_input,
                    'bot_reply': error_msg,
                    'error': error_msg
                })

            try:
                # Gunakan model Gemini
                model = genai.GenerativeModel('gemini-1.5-flash-latest')

                # Tambahkan konteks cybersecurity
                prompt = f"""Anda adalah CyberGuardAI, asisten keamanan siber profesional. 
                Berikan jawaban yang jelas, praktis, dan relevan untuk pertanyaan keamanan siber.
                
                Pertanyaan: {user_input}
                
                Jawab dengan format yang terstruktur dan mudah dibaca."""

                response = model.generate_content(prompt)
                bot_reply = response.text if response.text else "Maaf, tidak ada respon dari AI."

                return render(request, 'chatbot/index.html', {
                    'user_input': user_input,
                    'bot_reply': bot_reply,
                    'success': True
                })

            except Exception as api_error:
                error_msg = f"ERROR menghubungi AI: {str(api_error)}"
                print(f"DEBUG: {error_msg}")
                return render(request, 'chatbot/index.html', {
                    'user_input': user_input,
                    'bot_reply': f"❌ Error menghubungi AI: {str(api_error)}",
                    'error': error_msg
                })

        except Exception as e:
            error_msg = f"ERROR sistem: {str(e)}"
            print(f"DEBUG: {error_msg}")
            return render(request, 'chatbot/index.html', {
                'error': error_msg,
                'bot_reply': f"❌ Error sistem: {str(e)}"
            })

    # GET request
    return render(request, 'chatbot/index.html')
