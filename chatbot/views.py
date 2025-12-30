# views.py - SIMPLE VERSION
from django.shortcuts import render
from django.http import HttpResponse
import os


def home_view(request):
    """View utama - return HTML langsung"""
    print("✅ DEBUG: home_view dipanggil")

    # Baca file HTML langsung
    html_path = os.path.join(os.path.dirname(
        __file__), 'templates', 'chatbot', 'index.html')

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HttpResponse(html_content)
    except Exception as e:
        return HttpResponse(f"❌ ERROR membaca template: {str(e)}")


def chat_api(request):
    """API endpoint sederhana"""
    print("✅ DEBUG: chat_api dipanggil")
    return HttpResponse('{"success": false, "error": "API dalam maintenance"}', content_type='application/json')
