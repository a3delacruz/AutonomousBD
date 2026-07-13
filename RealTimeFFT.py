import numpy as np
import sounddevice as sd
import matplotlib as matplotlib
import matplotlib.pyplot as plt

fs = 44100 #Sampling rate
block_size = 2048 #Size of each block for FFT
print("Recording...")

#----Create the plot window
plt.ion() #Turn on interactive mode for real-time plotting
fig, ax = plt.subplots()
x_freqs = np.fft.rfftfreq(block_size, 1/fs) #Frequencies corresponding to the FFT bins
line, = ax.plot(x_freqs, np.zeros(len(x_freqs))) #Initialize the empty line for the spectrum
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude')
ax.set_title('Real-Time Frequency Spectrum')
ax.set_xlim(0, 5000) # limit x-axis to 5000 Hz for better visibility
ax.set_ylim(0, 50) # set y-axis limits for better visibility

#-----Start the stream loop
def audio_callback(indata, frames, time, status):
    # Calculate the FFT
    fft_data = np.fft.rfft(indata[:, 0]) # Perform FFT on the current block of audio data

    # Update the line data without redrawing the whole window
    line.set_ydata(np.abs(fft_data)) # Update the magnitudes of the spectrum

#while sd.InputStream(channels=1, samplerate=fs, blocksize=block_size, callback=audio_callback):
    # Refresh the drawing
 #   plt.pause(0.001) # Pause briefly to allow the plot to update

try:
    with sd.InputStream(channels=1, samplerate=fs, blocksize=block_size, callback=audio_callback):
        print("Recording... Close the plot window to stop.")
        while plt.fignum_exists(fig.number):
            fig.canvas.draw_idle()
            fig.canvas.flush_events()
            plt.pause(0.01) # Small pause to keep the UI responsive
except Exception as e:
    print(f"Error: {e}")

