# autonomous-BD-project
A modular, offline-first robotics framework robot, inspired by and highly based on the BD-1 droid. Features real-time speech recognition (Vosk), local LLM intent parsing (Ollama), and asynchronous motor control with future components in progress or planned.


This component specifically deals with processing user input, essentially following the model:

      Microphone → SoundDevice (Stream) → Vosk (STT Engine) → Threaded Queue → Ollama (LLM Intent) → Action Controller


## Part 1 - Speech recognition - Semester 0
Relevant files:\
Sem0codes folder --> contains relevant code files, including:\
Semester0final.py

### Installation Guide:
  In addition to a working microphone and Python 3:\
  pip install vosk sounddevice\
  __Download the Vosk model from alphacephei.com/vosk/models. Extract it into the root directory and rename the folder to model_.

###  How to run:
    python main.py
    Expected Output:
      BD-1 is listening...
      Listening: hello robot...
      Recognized: hello robot move forward
      [AI THREAD ACTIVE]: Processing command: hello robot move forward
  
  
 ### Lessons learned:
    Challenge: Audio buffer overflows during heavy processing.
        Solution: Implemented a thread-safe queue.Queue system to decouple the STT engine from the AI processing thread, ensuring 100% audio capture.
        
