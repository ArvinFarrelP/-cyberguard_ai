# 🔐 CyberGuard AI - Advanced Cybersecurity Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![AI](https://img.shields.io/badge/AI-Gemini-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**AI-powered cybersecurity terminal with real-time threat analysis, security advisories, and interactive guidance.**

[![Live Demo](https://img.shields.io/badge/Demo-Live%20Preview-9cf)](https://your-demo-link.com)
[![Documentation](https://img.shields.io/badge/Docs-Read%20Here-blueviolet)](docs/)
[![Issues](https://img.shields.io/github/issues/yourusername/cyberguard-ai)](https://github.com/yourusername/cyberguard-ai/issues)
[![Stars](https://img.shields.io/github/stars/yourusername/cyberguard-ai)](https://github.com/yourusername/cyberguard-ai/stargazers)

<div align="center">
  <img src="https://img.shields.io/badge/Theme-Cyber%20Terminal-00f3ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/UI-Responsive-8a2be2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Security-AES%20256-00ff88?style=for-the-badge" />
</div>

## ✨ Features

### 🎨 **Cyber Terminal Interface**

- 7+ Theme variations (Cyber, Hacker, Matrix, Neon, Void, Ice, Fire)
- Real-time typing animations & scan line effects
- Terminal-style command interface
- Fully responsive design (mobile/desktop)

### 🤖 **AI Cybersecurity Capabilities**

- Real-time threat analysis & vulnerability assessment
- Phishing detection guidance
- Firewall configuration advice
- Malware removal procedures
- Password security best practices
- Incident response protocols

### 💻 **Technical Features**

- Django backend with RESTful architecture
- Google Gemini AI integration
- Real-time chat with typing indicators
- Command history & quick commands
- Export chat functionality
- Theme persistence with localStorage
- Fullscreen mode & responsive design

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get here](https://makersuite.google.com/app/apikey))
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/cyberguard-ai.git
cd cyberguard-ai

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 6. Apply migrations
python manage.py migrate

# 7. Create superuser (optional)
python manage.py createsuperuser

# 8. Run development server
python manage.py runserver
```
