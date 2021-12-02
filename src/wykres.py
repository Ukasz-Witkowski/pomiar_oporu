import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Fig_Can
from matplotlib.figure import Figure

class wykres(Fig_Can):

    def __init__(self, parent=None, width=21, height=37, dpi=10):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(wykres, self).__init__(fig)