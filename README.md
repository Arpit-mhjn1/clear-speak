# 🌟 ClearSpeak: AI-Powered Indian Sign Language Interpreter

> **Bridging the communication gap with Real-Time Sign Language Translation & Generative Avatar Synthesis.**

[![Vercel Deployment](https://img.shields.io/badge/Deployed_on-Vercel-black?style=for-the-badge&logo=vercel)](https://clear-speak-iota.vercel.app)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github)](https://github.com/Arpit-mhjn1/clear-speak)

🔗 **Live Production URL:** [https://clear-speak-iota.vercel.app](https://clear-speak-iota.vercel.app)

---

## 🎯 The Mission
Over **430 million people worldwide** experience disabling hearing loss. Traditional communication requires human interpreters or slow typing. **ClearSpeak** transforms standard webcams into intelligent, bidirectional sign interpreters that run directly in the browser with sub-second latency.

---

## 🚀 Key Features

1. **📹 Real-Time Dual-Hand Sign Translation (`app.html`)**:
   - Leverages **Google MediaPipe** to simultaneously track both hands across 21 distinct 3D landmarks in real time.
   - Normalizes wrist relative coordinates and buffers gesture frames to translate Indian Sign Language (ISL) gestures into real-time spoken voice and text.

2. **✨ Generative AI Avatar (`text-to-sign.html`)**:
   - Converts English sentences into authentic Indian Sign Language (Subject-Object-Verb) gloss sequences using **Groq (Llama-3-8B)**.
   - Smoothly animates hand trajectories from a pre-extracted 3D spatial dictionary on an HTML5 canvas wireframe avatar.

3. **🔊 Dedicated Text-to-Speech Engine (`tts.html`)**:
   - Built using the native **Web Speech API** for crisp, zero-latency, on-device voice readout.

4. **📱 Fully Relative & Responsive UI**:
   - Fluid typography, dynamic flexbox panels, and mobile-friendly drawer navigation designed for desktop monitors, laptops, and mobile devices.

---

## 🛠️ Tech Stack & Dependencies

- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Fluid `clamp()` & modern CSS custom properties).
- **Vision & Landmark Tracking**: `@mediapipe/camera_utils`, `@mediapipe/hands`, `@mediapipe/drawing_utils`.
- **Generative Language Model**: [Groq API](https://groq.com) running `llama3-8b-8192`.
- **Speech Synthesis**: Browser Native `window.speechSynthesis`.
- **Data Pipeline**: Python 3.14, OpenCV, MediaPipe Tasks (`HandLandmarker`), NumPy.
- **Hosting**: Deployed on **Vercel** with global edge CDN caching.

---

## 💻 Local Setup & Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Arpit-mhjn1/clear-speak.git
   cd clear-speak
   ```

2. **Run with any local HTTP server:**
   ```bash
   python -m http.server 8000
   ```
   Open `http://localhost:8000` in Google Chrome or any modern browser.

---

## 👥 Team Logic Lords
Developed by:
- **Arpit Mahajan**
- **Mannat Sharma**
- **Devanshu Thakur**
- **Akshita**
