import matplotlib.pyplot as plt
import pickle

def load_obj(path):
    if path.endswith('.pickle') or path.endswith('.pkl'):
        with open(path, 'rb') as f:
            return pickle.load(f)

class DynamicUpdate():
    #Suppose we know the x range
    # min_x = -1
    # max_x = 4

    def __init__(self, min_x: int = -10, max_x=10, min_y: int = None, max_y=None):
        #Set up plot
        self.figure, self.ax = plt.subplots(2, figsize=(10, 8))
        self.fignum = self.figure.number
        # self.figure.canvas.set_window_title('Measurements')

        self.lines, = self.ax[0].plot([0],[0], 'r.', markersize=1)
        self.lines.set_label('Laser distances')
        
        self.ax[0].invert_xaxis()
        self.ax[0].invert_yaxis()
        self.lines2, = self.ax[1].plot([0],[0], 'b-', markersize=1)
        #Autoscale on unknown axis and known lims on the other
        self.ax[0].set_autoscaley_on(True)
        self.ax[0].set_xlim(min_x, max_x)
        if min_y and max_y:
            self.ax[0].set_ylim(min_y, max_y)
        #Other stuff
        self.ax[0].grid()

        self.lines.xlabel = 'X'
        self.ax[0].set_ylabel('Z mm')
        self.ax[0].set_xlabel('X mm')
        self.ax[0].set_title('Laser scan & Pressure readings')
        # self.ax[1].set_title('Pressure kPa')
        self.ax[1].set_xlabel('s')
        self.ax[1].set_ylabel('kPa')

        ...

    def __call__(self, xdata, ydata, xdata2, ydata2, ):
        if not plt.fignum_exists(self.fignum): return False

        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        self.lines2.set_xdata(xdata2)
        self.lines2.set_ydata(ydata2)
        #Need both of these in order to rescale
        

        self.ax[0].relim()
        self.ax[0].autoscale_view()
        self.ax[1].relim()
        self.ax[1].autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

        return True
    

class ReaderUpdate():
    #Suppose we know the x range
    # min_x = -1
    # max_x = 4

    def __init__(self, min_x: int = -10, max_x=10):
        #Set up plot
        self.figure, self.ax = plt.subplots(2, figsize=(10, 8))
        self.fignum = self.figure.number
        # self.figure.canvas.set_window_title('Measurements')

        self.lines, = self.ax[0].plot([0],[0], 'r-', markersize=1)
        # self.lines.set_label('Laser distances')
        
        # self.ax[0].invert_xaxis()
        # self.ax[0].invert_yaxis()
        self.lines2, = self.ax[1].plot([0],[0], 'b-', markersize=1)
        #Autoscale on unknown axis and known lims on the other
        # self.ax[0].set_autoscaley_on(True)
        # self.ax[0].set_xlim(min_x, max_x)
        #Other stuff
        self.ax[0].grid()

        self.lines.xlabel = 'X'
        self.ax[0].set_ylabel('$d_o$ mm')
        # self.ax[0].set_xlabel('X mm')
        self.ax[0].set_title('Laser scan & Pressure readings')
        # self.ax[1].set_title('Pressure kPa')
        self.ax[1].set_xlabel('s')
        self.ax[1].set_ylabel('Pressure kPa')

        ...

    def __call__(self, xdata, ydata, xdata2, ydata2, ):
        if not plt.fignum_exists(self.fignum): return False

        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        self.lines2.set_xdata(xdata2)
        self.lines2.set_ydata(ydata2)
        #Need both of these in order to rescale
        

        self.ax[0].relim()
        self.ax[0].autoscale_view()
        self.ax[1].relim()
        self.ax[1].autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

        return True