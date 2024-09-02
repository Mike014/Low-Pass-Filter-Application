# filter_app/views.py

from django.shortcuts import render
from django.views import generic
import numpy as np
from scipy.signal import butter, lfilter
import json
import tempfile
import soundfile as sf
import os

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def save_temp_audio_file(data, fs):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    sf.write(temp_file.name, data, fs)
    print(f"Audio file saved at: {temp_file.name}")
    return temp_file.name

class IndexView(generic.TemplateView):
    template_name = 'filter_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fs = 44100  
        t = np.linspace(0, 1, fs, endpoint=False)  

        f1 = float(self.request.GET.get('frequency', 440))
        signal = np.sin(2 * np.pi * f1 * t)

        cutoff = float(self.request.GET.get('cutoff', 1000))
        resonance = float(self.request.GET.get('resonance', 0.5))

        filtered_signal = butter_lowpass_filter(signal, cutoff, fs, order=6)

        print("Original Signal (first 10 values):", signal[:10])
        print("Filtered Signal (first 10 values):", filtered_signal[:10])

        max_val = max(abs(min(filtered_signal)), max(filtered_signal))
        if max_val > 0:
            filtered_signal = [x / max_val for x in filtered_signal]

        audio_file_path = save_temp_audio_file(filtered_signal, fs)
        print(f"Audio file path in context: {audio_file_path}")

        context.update({
            'cutoff': cutoff,
            'resonance': resonance,
            'frequency': f1,
            'signal': json.dumps(signal.tolist()),
            'filtered_signal': json.dumps(filtered_signal),
            't': json.dumps(t.tolist()),
            'audio_file_path': audio_file_path,
        })
        return context












