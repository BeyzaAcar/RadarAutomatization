# common functions for radar data processing eg: visualizing
import matplotlib.pyplot as plt

def plot_signal(data, title):
    plt.plot(data)
    plt.title(title)
    plt.show()

def plot_spectrogram(frequencies, times, magnitude_spectrum):
    plt.pcolormesh(times, frequencies, magnitude_spectrum, shading='gouraud')
    plt.title("Spectrogram")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")
    plt.colorbar(label="Intensity")
    plt.show()
