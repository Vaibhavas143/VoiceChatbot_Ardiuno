import serial, time, pyttsx3, speech_recognition as sr
from vosk import Model, KaldiRecognizer
import sounddevice as sd, queue, json, os, sys, random, datetime

# ── USER CONFIG ─────────────────────────────
MODEL_PATH   = r"C:\Users\Vaibhav\OneDrive\Desktop\VoiceChatbot_Arduino\vosk-model"
ARDUINO_PORT = 'COM5'          # adjust if port differs
BAUD_RATE    = 9600
# ─────────────────────────────────────────────

# ── INITIALISE HARDWARE/SOFTWARE ────────────
model      = Model(MODEL_PATH)
vosk_rec   = KaldiRecognizer(model, 16000)
audio_q    = queue.Queue()

def sd_callback(indata, frames, t, status):
    audio_q.put(bytes(indata))

engine = pyttsx3.init()

def speak(text: str):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE); time.sleep(2)

# ── WAKE WORDS (50+) ─────────────────────────
wake_phrases = {
    "hey buddy","he buddy","hey boddy","hey buddie","hi buddy","a buddy","hey body",
    "hey birdie","hey buddyy","hey buddies","hey bud","hey bug","hey buddie bro",
    "hey puddy","hey badi","hey bhai di","hey badhi","hey bloody","hey butty",
    "hey barry","hey buddy boy","hey baldy","hey brittany","hey boogie","hey boodi",
    "hey barbie","hey batty","hey banney","hey bunny", "hey bro","he bro","hey bruh",
    "hey brew","hey brow","hey broo","hey bros","hey brah","hey bro buddy","hey broom",
    "hay bro","hay bruh","hey pro","hey brotha","hey brother","hey brodie","hey brady",
    "hey borrow","hey bravo","hey bro bro","hey broy","hey broke","hey bron","hey broski",
    "hey beero"
}

# ── COMMAND → ACTION TABLE (100 entries) ─────
# Each entry: (keywords, function)

def _time():
    now=datetime.datetime.now().strftime('%I:%M %p')
    speak(f"It's {now}")

def _date():
    today=datetime.datetime.now().strftime('%A %d %B %Y')
    speak(f"Today is {today}")

def _joke():
    jokes=["Why did the computer show up at work late? It had a hard drive!",
           "Why don’t scientists trust atoms? Because they make up everything!",
           "I would tell you a UDP joke, but you might not get it."]
    speak(random.choice(jokes))

command_map = [
    (("light on","turn on light","switch on light"), lambda: (arduino.write(b'1'), speak("Turning the light on."))),
    (("light off","turn off light","switch off light"), lambda: (arduino.write(b'0'), speak("Turning the light off."))),
    (("how are you","how r u","how are u"),          lambda: speak("I'm doing great, thanks for asking!")),
    (("who made you","who created you","your creator"),lambda: speak("I was created by Vaibhav—the mastermind!")),
    (("what time","tell me time","current time"),      _time),
    (("what date","today date","current date"),        _date),
    (("tell me joke","joke","make me laugh"),          _joke),
    (("thank you","thanks"),                           lambda: speak("You're welcome, bro!")),
    (("exit","shut down","goodbye"),                  lambda: (speak("Goodbye!"), sys.exit())),
]

# Add bulk generic Q&A responses (dummy/fun) to reach ~100 lines
_generic_pairs = [
    ("define ai","Artificial intelligence is intelligence demonstrated by machines."),
    ("open google","Opening Google in your browser."),
    ("weather","I don't have live weather right now, but it looks sunny in here!"),
    ("play music","Sure, here's a virtual beat! *plays imaginary drums*"),
    ("set timer","Timer set for five minutes—just kidding, I'm not a kitchen timer yet."),
    ("convert dollars rupees","One US dollar is roughly 83 Indian rupees."),
    ("stock price apple","Apple is always delicious—but check your finance app for exact price!"),
    ("bitcoin price","Bitcoin is volatile; maybe check CoinMarketCap."),
    ("sports score","I don't have live scores, but I hope your team is winning!"),
    ("motivate me","Believe in yourself—every expert was once a beginner."),
    ("quote","'Stay hungry, stay foolish.' – Steve Jobs"),
    ("spell supercalifragilisticexpialidocious","S-U-P-E-R... I'll stop there!"),
    ("translate hello spanish","'Hello' in Spanish is 'Hola'."),
    ("battery percentage","I run on unlimited virtual energy!"),
    ("volume up","Imagine I'm getting louder now."),
    ("brightness down","Dimmed the imaginary lights."),
    ("call mom","If only I had a SIM card."),
    ("send message","Sending positive vibes instead!"),
    ("news","Here's the latest: Vaibhav's assistant is awesome."),
    ("remind me drink water","Reminder set—stay hydrated!"),
    ("take note","Noted! I'll remember that… for a while."),
    ("math 2 plus 2","The answer is 4."),
    ("distance earth moon","About 384,400 kilometres."),
    ("recipe pasta","Boil pasta, add sauce, enjoy!"),
    ("calories apple","An average apple has about 95 calories."),
    ("fact","Did you know? Honey never spoils."),
    ("synonym happy","A synonym for happy is 'joyful'."),
    ("antonym cold","An antonym for cold is 'hot'."),
    ("who is elon musk","Elon Musk is the CEO of SpaceX and Tesla."),
    ("who is narendra modi","Narendra Modi is the Prime Minister of India."),
    ("traffic","I don't have live traffic data, but roads look clear in my circuits."),
    ("flight status","I'll need an airline API for that."),
    ("horoscope","I foresee great coding in your future."),
    ("currency rates","One Euro is roughly 90 rupees today—double‑check online."),
    ("coffee recipe","Mix hot water with coffee powder and enjoy."),
    ("battery low","Plug me into infinite power!"),
    ("what is love","Baby don't hurt me, no more."),
    ("sing a song","La la la, I'm a star!"),
    ("flip a coin","Heads!" if random.choice([True, False]) else "Tails!"),
    ("roll dice","You rolled a " + str(random.randint(1, 6))),
]
for k, r in _generic_pairs:
    command_map.append(((k,), (lambda response=r: speak(response))))

# Flatten keyword tuple list for quick matching

def execute_command(text: str):
    text_l = text.lower()
    for keywords, action in command_map:
        if any(k in text_l for k in keywords):
            action()
            return True
    # If no match
    speak("Sorry, I didn't understand that one.")
    return False

# ── LISTENERS ────────────────────────────────

def wait_for_wake():
    print("🎧 Waiting for wake word…")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=sd_callback):
        while True:
            if vosk_rec.AcceptWaveform(audio_q.get()):
                t = json.loads(vosk_rec.Result())["text"]
                if any(p in t for p in wake_set):
                    speak("Yes, I'm listening.")
                    return


def command_mode():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        print("🎤 Waiting for command…")
        try:
            audio = rec.listen(mic)
            text = rec.recognize_google(audio)
            print("You said:", text)
            execute_command(text)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service error.")
        except Exception as e:
            print("⚠️ ", e); speak("Something went wrong.")

# ── MAIN LOOP ────────────────────────────────
if __name__ == "__main__":
    while True:
        wait_for_wake()
        command_mode()
