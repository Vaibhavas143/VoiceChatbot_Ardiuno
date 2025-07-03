🔊 Smart Voice-Controlled Assistant with Arduino Integration
An AI-powered voice assistant built using Python, Vosk (offline speech recognition), and Arduino that listens for wake words like "Hey Buddy" or "Hey Bro", and responds to over 100 natural voice commands — from turning lights on/off to telling jokes, date, time, facts, and more!

✨ Features
Wake Word Detection (Offline)
Listens in the background using Vosk speech recognition for custom wake words (50+ variants like “Hey Buddy”, “Hey Bro”, etc.)

Voice Command Processing
Uses speech_recognition and Google API to handle spoken commands with smart response handling.

Arduino Integration
Communicates with Arduino via serial (USB COM port) to control hardware (e.g., LED light on/off).

100+ Natural Language Commands
Includes time, date, jokes, conversions, facts, motivational quotes, fun replies, and custom Vaibhav-themed answers 😄

Offline Friendly
Wake-word listening works fully offline using Vosk STT.

Modular & Expandable
Easy to plug in gestures (IR sensor), Bluetooth, or camera-based input in the future.

🛠️ Tech Stack
Python 3.12

Vosk (offline speech recognition)

Pyttsx3 (text-to-speech)

speech_recognition (Google STT API for post-wake command)

Arduino UNO (with serial communication)

LED & 330Ω resistor for light control
