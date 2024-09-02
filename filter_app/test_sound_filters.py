# -*- coding: utf-8 -*-
import unittest
import numpy as np
import sys
import os
import sounddevice as sd
from scipy.signal import butter, lfilter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSoundFilters(unittest.TestCase):

    def setUp(self):
        self.sample_rate = 44100
        self.duration = 5  
        self.t = np.linspace(0, self.duration, self.sample_rate * self.duration, endpoint=False)
        self.frequency = 1000  
        self.signal = np.sin(2 * np.pi * self.frequency * self.t)

    def play_sound(self, signal, description):
        """Utility function to play a sound signal."""
        print(f"Playing {description}...")
        sd.play(signal, self.sample_rate)
        sd.wait()  # Wait until the sound has finished playing

    def butter_lowpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def test_play_original_signal(self):
        """Test to play the original signal."""
        self.play_sound(self.signal, "original signal")

    def test_low_pass_filter(self):
        cutoff = 400  
        filtered_signal = self.butter_lowpass_filter(self.signal, cutoff, self.sample_rate, order=6)

        print("Original Signal (first 10 values):", self.signal[:10])
        print("Filtered Signal (first 10 values):", filtered_signal[:10])

        self.assertNotEqual(self.signal.tolist(), filtered_signal.tolist())

        # Play the filtered signal
        self.play_sound(filtered_signal, "filtered signal")

if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(TestSoundFilters('test_play_original_signal'))
    suite.addTest(TestSoundFilters('test_low_pass_filter'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
















