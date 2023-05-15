import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QLineEdit, QFileDialog, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QPixmap, QPalette


class Langevin252A(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fader GUI")
        self.setGeometry(100, 100, 600, 600)

        # Create a central widget and set it as the main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a vertical layout for the faders, labels, and graph
        layout = QVBoxLayout(central_widget)

        # Define the fader values and associated frequencies
        fader_values = [
            ("50Hz", 50),
            ("130Hz", 130),
            ("320Hz", 320),
            ("800Hz", 800),
            ("2000Hz", 2000),
            ("5000Hz", 5000),
            ("12500Hz", 12500)
        ]

        # Create a fader for each value
        self.sliders = []
        for value, frequency in fader_values:
            # Create a label for the fader
            label = QLabel(value, self)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

            # Create a slider for the fader
            slider = QSlider(Qt.Horizontal, self)
            slider.setMinimum(-8)
            slider.setMaximum(8)
            slider.setValue(0)
            slider.valueChanged.connect(lambda value, freq=frequency: self.update_graph())
            layout.addWidget(slider)

            self.sliders.append((slider, frequency))

        # Create a drop-down menu for presets
        self.presets_dropdown = QComboBox(self)
        self.presets_dropdown.addItems(["Preset 1", "Preset 2"])
        self.presets_dropdown.currentIndexChanged.connect(self.change_preset)
        layout.addWidget(self.presets_dropdown)

        # Create a figure and canvas for the graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.canvas.setStyleSheet("background-color: black;")  # Set the canvas background to black

        # Create a button and line edit for saving presets
        self.save_preset_button = QPushButton("Save Preset", self)
        self.save_preset_button.clicked.connect(self.save_preset)
        layout.addWidget(self.save_preset_button)
        self.save_preset_line_edit = QLineEdit(self)
        layout.addWidget(self.save_preset_line_edit)

        # Create a button to load presets
        self.load_presets_button = QPushButton("Load Presets", self)
        self.load_presets_button.clicked.connect(self.load_presets)
        layout.addWidget(self.load_presets_button)

        # Create a button to process audio
        self.process_audio_button = QPushButton("Process Audio", self)
        self.process_audio_button.clicked.connect(self.process_audio)
        layout.addWidget(self.process_audio_button)

        # Create a progress bar for audio processing
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Initialize the graph
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(20, 20000)
        self.ax.set_ylim(-8, 8)
        self.ax.set_facecolor('black')
        line_props = {'linewidth': 0.5, 'color': 'white'}
        self.line, = self.ax.plot([], [], **line_props)
        self.ax.tick_params(axis='x', labelsize=3)
        self.ax.tick_params(axis='y', labelsize=3)

        self.update_graph()

    def update_graph(self):
        # Update the graph based on the fader values
        frequencies = []
        gains = []
        for slider, frequency in self.sliders:
            gain = slider.value()
            if gain != 0:
                frequencies.append(frequency)
                gains.append(gain)

        t = np.logspace(np.log10(20), np.log10(20000), 1000)
        signal = np.sum([np.sin(2 * np.pi * f * t) * (10 ** (g / 20)) for f, g in zip(frequencies, gains)], axis=0)

        self.line.set_data(t, signal)
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.canvas.draw()

    def load_presets(self):
        # Open a file selection dialog to choose the presets file
        print("Loading presets:")

    def process_audio(self):
        # Start the audio processing and update the progress bar
        self.progress_bar.setValue(0)

        # Simulating audio processing using a timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start(100)  # Timer interval in milliseconds

    def onTimeout(self):
        current_value = self.progress_bar.value()
        if current_value >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.progress_bar.setValue(current_value + 1)

    def save_preset(self):
        # Get the text from the line edit widget
        preset_name = self.save_preset_line_edit.text()
        # Do something with the preset name (e.g., save it to a file or store it in a data structure)
        print(f"Saving preset: {preset_name}")
        # Add the preset name to the drop-down menu
        self.presets_dropdown.addItem(preset_name)
        # Clear the line edit widget
        self.save_preset_line_edit.clear()
        print(f"Done saving")

    def change_preset(self, index):
        # Define the preset values for each fader
        presets = [
            [0, 2, -4, 0, 1, 0, -3],  # Preset 1
            [-3, 4, 6, 0, -2, 0, 0]  # Preset 2
        ]

        # Set the slider values based on the selected preset
        preset_values = presets[index]
        for i, (slider, _) in enumerate(self.sliders):
            slider.setValue(preset_values[i])

        self.update_graph()

    def show(self):
        super().show()
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication([])
    gui = Langevin252A()
    gui.show()
    sys.exit(app.exec_())