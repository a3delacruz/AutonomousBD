import queue
import sys
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import threading

# ---- Load the Vosk model
model = Model("model")
audio_queue = queue.Queue()
ai_queue = queue.Queue()  # Queue for passing recognized text to the AI portion

# ---- Settings
fs = 16000  # Sample rate
recognizer = KaldiRecognizer(model, fs)
block_size = 8000  # Block size for audio processing (0.5 seconds at 16kHz)

def ai_processing(): ###--------EVENTUALLY REPLACE THIS WITH A MORE SOPHISTICATED AI RESPONSE GENERATION FUNCTION
    while True:
        text_to_process = ai_queue.get()  # Get the recognized text from the AI queue
        if text_to_process is None: break

        print(f"AI processing: {text_to_process}")  # Placeholder for AI processing logic
        ##-----FUTURE WORK: Implement AI response generation based on the recognized text
        ## response = ollama.chat(model='llama3', messages=[...])

        ai_queue.task_done()  # Mark the task as done


threading.Thread(target=ai_processing, daemon=True).start()  # Start the AI processing thread
    

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    # put the raw data into the queue for processing
    audio_queue.put(bytes(indata))

# ---- Start the audio stream
try:
    with sd.RawInputStream(samplerate=fs, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("Listening... Press Ctrl+C to stop.")
        while True:
            data = audio_queue.get()  # Get the raw audio data from the queue
            if recognizer.AcceptWaveform(data):
                # triggers if a full sentence is recognized
                result_dict = json.loads(recognizer.Result())  # Get the final result as a dictionary
                user_text = result_dict.get('text', '')  # Extract the recognized text
                if user_text: 
                    print(f"Recognized: {user_text}")  # Print the recognized text
                #------hand off the text to the AI portion
                    wake_words = ["robot", "hey BD", "BD", "bd-1"]  # List of wake words
                    if any(wake_word in user_text.lower() for wake_word in wake_words):  # Check for wake words (case-insensitive)
                        ai_queue.put(user_text)  # Put the recognized text into the AI queue for processing
                    else:
                        print("No wake word detected. Ignoring input.")  # Print a message if no wake word is detected
            else:
                #shows partial results while speaking
                partial = json.loads(recognizer.PartialResult())
                if partial['partial']:
                    print(partial)  # Print the partial result as JSON

except KeyboardInterrupt:
    print("\nStopped by user")

