import numpy as np
import sounddevice as sd
import matplotlib as matplotlib
import matplotlib.pyplot as plt


fs = 44100 #Sampling rate
duration = 3 #Duration of recording in seconds 
print("Recording...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait() #Wait until recording is finished
print("Recording finished.")

print("Replaying.")
sd.play(recording, fs) #Play the recording
sd.wait() #Wait until playback is finished
print("Replay done")

print(f"Recording shape: {recording.shape}")
print(f"Recording data type: {recording.dtype}")
print(f"First 10 samples of recording: {recording[:10]}")

fft_data = np.fft.fft(recording.flatten())             # perform FFT on the recorded data
magnitudes = np.abs(fft_data)                          # get the magnitudes
frequencies = np.fft.fftfreq(len(recording), 1/fs)     # get the corresponding frequencies

positive_frequencies = frequencies[:len(frequencies)//2]  # consider only positive frequencies
positive_magnitudes = magnitudes[:len(magnitudes)//2]  # corresponding magnitudes for positive frequencies

print(f"Strongest frequency component: {frequencies[np.argmax(magnitudes)]} Hz with magnitude {np.max(magnitudes)}")

#--plotting the frequency spectrum
plt.figure(figsize=(10, 6))

#subplot 1 = time domain (waveform)
plt.subplot(2, 1, 1)
plt.plot(fft_data, color='blue')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Time Domain (Waveform)')

#subplot 2 = frequency domain (spectrum)
plt.subplot(2, 1, 2)
plt.plot(positive_frequencies, positive_magnitudes, color='red')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Frequency Domain (Spectrum)')
plt.xlim(0, 5000) # limit x-axis to 5000 Hz for better visibility

plt.tight_layout()
plt.show()

#print(sd.query_devices())
#print(sd.default.device)


