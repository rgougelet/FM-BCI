import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()

# plot peak alpha as a function of time

class Plot():
    #Suppose we know the x range
    min_x = 0
    max_x = 10

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], 'o')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
        self.ax.grid()
        # ...

    def on_running(self, x_time, y_paf):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(x_time)
        self.lines.set_ydata(y_paf)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        self.on_launch()
        x_time = []
        y_paf = []
        for x in np.arange(0,10,0.5):
            x_time.append(x)
            y_paf.append(1.0/x)
            self.on_running(x_time, y_paf)
            time.sleep(1)
        return x_time, y_paf

d = Plot()
d()