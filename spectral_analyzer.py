import numpy as np
from scipy.io import wavfile as wf
import matplotlib.pyplot as plt
import time as t

class Analyzer:
    def __init__(self, wav, sample_rate, plotter, track_length):
        self.sample_rate = sample_rate
        wf = []
        for sample in wav:
            wf.append(sample[0])
        self.waveform = np.array(wf)
        self.plt = plotter

        self.WAITTIME = 0.08
        self.WINDOWTIME = 0.01
        self.TRACKTIME = track_length

        self.DELTATIME = (self.WAITTIME * (self.TRACKTIME - self.WINDOWTIME))/self.TRACKTIME
    def draw(self):
        plot_window = int(self.sample_rate*self.WINDOWTIME)
        start = 0

        x = np.linspace(start, plot_window, plot_window-start)
        y = self.waveform[start:plot_window]

        self.plt.ion()
        fig = self.plt.figure()
        wave_plot = fig.add_subplot(111)
        wave_plot.set_xticks([])
        wave_plot.set_yticks([])
        line, = wave_plot.plot(x, y, "b-")

        a = t.time()
        while(plot_window < len(self.waveform)):
            st = t.time()
            line.set_ydata(self.waveform[start:plot_window])
            fig.canvas.draw()
            fig.canvas.flush_events()

            start += int(self.sample_rate * self.DELTATIME)
            plot_window += int(self.sample_rate * self.DELTATIME)
            et = t.time()

            if (et-st) < self.WAITTIME:
                rem_wait_time = self.WAITTIME - (et-st)
                t.sleep(rem_wait_time)

        b = t.time()
        print(b-a)

        
    def get_wave(self):
        return self.waveform
        
rate, file = wf.read("test_file.wav")
a = Analyzer(wav=file, sample_rate=rate, plotter=plt, track_length=8)
a.draw()
