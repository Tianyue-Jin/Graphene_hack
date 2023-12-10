import sys
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import threading
import socket
import numpy as np
from logger import getmylogger
import matplotlib.colors as colors



log = getmylogger(__name__)

DEBUG = True

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.topic = ""
        self.subAddr = '192.168.4.2'
        self.x_len = 10  # Number of bars
        self.y_range = [0.7, 1.8]  # Adjusted y-axis limits
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.canvas = FigureCanvas(self.fig)

        self.receiver = UDPReceiver(self.topic, self.subAddr)
        self.receiver.socketDataSig.connect(self._updateData)
        self.receiver.start()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.xs = list(range(0, self.x_len))
        self.bars = self.ax.bar(self.xs, [0] * self.x_len, color='gray')  # Create gray bars initially

        # Create a colormap for the data range
        cmap = plt.get_cmap('viridis')  # You can choose a different colormap
        norm = colors.Normalize(vmin=min(self.y_range), vmax=max(self.y_range))

        # Create scalar mappable to map data values to colors
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # Dummy array to use colormap with Normalize

        self.colorbar = plt.colorbar(sm, ax=self.ax, label='Color Map')  # Add colorbar to the plot

    @QtCore.pyqtSlot(str)
    def _updateData(self, msg):
        try:
            values = [float(val) for val in msg.split(":")[1:4]]  # Extract three values from the message
            if DEBUG:
                print(values)

            # Update bar heights and colors based on the values
            for bar, value in zip(self.bars, values):
                bar.set_height(value)
                bar.set_color(self.colorbar.to_rgba(value))

        except Exception as e:
            log.error("Exception in UpdateData: ", e)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Real-time Bar Chart with PyQt and Matplotlib')
        central_widget = MatplotlibWidget(self)
        self.setCentralWidget(central_widget)

class UDPReceiver(QObject):
    socketDataSig = QtCore.pyqtSignal(str)

    def __init__(self, topic, subAddr):
        super().__init__()
        self.subAddr = subAddr
        self.topic = topic.encode()

    def start(self):
        threading.Thread(target=self._execute, daemon=True).start()

    def _execute(self):
        log.info("Started UDP Receiver")
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.subAddr, 12345))

        while True:
            try:
                data, addr = udp_socket.recvfrom(1024)
                data = data.decode()
                self.socketDataSig.emit(data)
            except Exception as e:
                log.error(f"Exception in UDP Receiver: {e}")
                break
        log.info(f"exit UDP Thread Sub: {self.topic}")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
