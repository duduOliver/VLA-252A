from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QApplication, QLabel, QSlider, \
    QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt

import numpy as np
from scipy.io import wavfile
from LCSecOrd_BPF import SecondOrderBandPass
import matplotlib.pyplot as plt

class MainWindow(QMainWindow):
    s1value = s2value = s3value = s4value = s5value = s6value = s7value = 0

    def __init__(self):
        super().__init__()

        self.center_frequencies = [50, 130, 320, 800, 2000, 5000, 12500]

        self.input_filepath = "/path/to/file"
        self.output_filepath = "/path/to/file"

        self.choose_input_button = QPushButton("Choose Input File", self)
        self.choose_input_button.clicked.connect(self.choose_input_file)
        self.choose_input_button.setGeometry(50, 50, 200, 30)
        self.choose_input_button.setStyleSheet("QPushButton"
                                           "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")

        self.choose_output_button = QPushButton("Choose Output File", self)
        self.choose_output_button.clicked.connect(self.choose_output_file)
        self.choose_output_button.setGeometry(50, 100, 200, 30)
        self.choose_output_button.setStyleSheet("QPushButton"
                                           "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")
        #SLIDER 1
        self.slider1 = QSlider(Qt.Vertical, self)
        self.slider1.setMinimum(-12)
        self.slider1.setMaximum(12)
        self.slider1.setValue(0)
        self.slider1.setFixedHeight(250)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider1.setTickInterval(2)
        self.slider1.setStyleSheet('QSlider::groove:vertical {} '
                                   'QSlider::handle:vertical {height: 2px; '
                                   'background: rgb(255, 79, 68); '
                                   'border-width: 1px; '
                                   'border-radius: 5px;}')
        self.slider1.valueChanged.connect(self.slider1_value_changed)

        #SLIDER 2
        self.slider2 = QSlider(Qt.Vertical, self)
        self.slider2.setMinimum(-12)
        self.slider2.setMaximum(12)
        self.slider2.setValue(0)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.slider2.setTickInterval(2)
        self.slider2.setStyleSheet('QSlider::groove:vertical {} '
                                   'QSlider::handle:vertical {height: 2px; '
                                   'background: rgb(255, 79, 68); '
                                   'border-width: 1px; '
                                   'border-radius: 5px;}')
        self.slider2.valueChanged.connect(self.slider2_value_changed)

        #SLIDER 3
        self.slider3 = QSlider(Qt.Vertical, self)
        self.slider3.setMinimum(-12)
        self.slider3.setMaximum(12)
        self.slider3.setValue(0)
        self.slider3.setTickPosition(QSlider.TicksBelow)
        self.slider3.setTickInterval(2)
        self.slider3.setStyleSheet('QSlider::groove:vertical {} '
                                   'QSlider::handle:vertical {height: 2px; '
                                   'background: rgb(255, 79, 68); '
                                   'border-width: 1px; '
                                   'border-radius: 5px;}')
        self.slider3.valueChanged.connect(self.slider3_value_changed)

        #SLIDER 4
        self.slider4 = QSlider(Qt.Vertical, self)
        self.slider4.setMinimum(-12)
        self.slider4.setMaximum(12)
        self.slider4.setValue(0)
        self.slider4.setTickPosition(QSlider.TicksBelow)
        self.slider4.setTickInterval(2)
        self.slider4.setStyleSheet('QSlider::groove:vertical {} '
                                   'QSlider::handle:vertical {height: 2px; '
                                   'background: rgb(255, 79, 68); '
                                   'border-width: 1px; '
                                   'border-radius: 5px;}')
        self.slider4.valueChanged.connect(self.slider4_value_changed)

        #SLIDER 5
        self.slider5 = QSlider(Qt.Vertical, self)
        self.slider5.setMinimum(-12)
        self.slider5.setMaximum(12)
        self.slider5.setValue(0)
        self.slider5.setTickPosition(QSlider.TicksBelow)
        self.slider5.setTickInterval(2)
        self.slider5.setStyleSheet('QSlider::groove:vertical {} '
                                   'QSlider::handle:vertical {height: 2px; '
                                   'background: rgb(255, 79, 68); '
                                   'border-width: 1px; border-radius: 5px;}')
        self.slider5.valueChanged.connect(self.slider5_value_changed)

        #SLIDER 6
        self.slider6 = QSlider(Qt.Vertical, self)
        self.slider6.setMinimum(-12)
        self.slider6.setMaximum(12)
        self.slider6.setValue(0)
        self.slider6.setTickPosition(QSlider.TicksBelow)
        self.slider6.setTickInterval(2)
        self.slider6.setStyleSheet('QSlider::groove:vertical {} '
                                   'QSlider::handle:vertical {height: 2px; '
                                   'background: rgb(255, 79, 68); '
                                   'border-width: 1px; '
                                   'border-radius: 5px;}')
        self.slider6.valueChanged.connect(self.slider6_value_changed)

        #SLIDER 7
        self.slider7 = QSlider(Qt.Vertical, self)
        self.slider7.setMinimum(-12)
        self.slider7.setMaximum(12)
        self.slider7.setValue(0)
        self.slider7.setTickPosition(QSlider.TicksBelow)
        self.slider7.setTickInterval(2)
        self.slider7.setStyleSheet('QSlider::groove:vertical {} '
                                   'QSlider::handle:vertical {height: 2px; '
                                   'background: rgb(255, 79, 68); '
                                   'border-width: 1px; '
                                   'border-radius: 5px;}')
        self.slider7.valueChanged.connect(self.slider7_value_changed)

        #SLIDER 1 LABEL
        self.slider1_label = QLabel("50 Hz", self)
        self.slider1_label.setAlignment(Qt.AlignHCenter)
        self.slider1_label.setStyleSheet('color: white')

        # SLIDER 2 LABEL
        self.slider2_label = QLabel("130 Hz", self)
        self.slider2_label.setAlignment(Qt.AlignHCenter)
        self.slider2_label.setStyleSheet('color: white')

        # SLIDER 3 LABEL
        self.slider3_label = QLabel("320 Hz", self)
        self.slider3_label.setAlignment(Qt.AlignHCenter)
        self.slider3_label.setStyleSheet('color: white')

        # SLIDER 4 LABEL
        self.slider4_label = QLabel("800 Hz", self)
        self.slider4_label.setAlignment(Qt.AlignHCenter)
        self.slider4_label.setStyleSheet('color: white')

        # SLIDER 5 LABEL
        self.slider5_label = QLabel("2000 Hz", self)
        self.slider5_label.setAlignment(Qt.AlignHCenter)
        self.slider5_label.setStyleSheet('color: white')

        # SLIDER 6 LABEL
        self.slider6_label = QLabel("5000 Hz", self)
        self.slider6_label.setAlignment(Qt.AlignHCenter)
        self.slider6_label.setStyleSheet('color: white')

        # SLIDER 7 LABEL
        self.slider7_label = QLabel("12500 Hz", self)
        self.slider7_label.setAlignment(Qt.AlignHCenter)
        self.slider7_label.setStyleSheet('color: white')

        slider1_layout = QVBoxLayout()
        slider1_layout.addWidget(self.slider1)
        slider1_layout.addWidget(self.slider1_label)

        slider2_layout = QVBoxLayout()
        slider2_layout.addWidget(self.slider2)
        slider2_layout.addWidget(self.slider2_label)

        slider3_layout = QVBoxLayout()
        slider3_layout.addWidget(self.slider3)
        slider3_layout.addWidget(self.slider3_label)

        slider4_layout = QVBoxLayout()
        slider4_layout.addWidget(self.slider4)
        slider4_layout.addWidget(self.slider4_label)

        slider5_layout = QVBoxLayout()
        slider5_layout.addWidget(self.slider5)
        slider5_layout.addWidget(self.slider5_label)

        slider6_layout = QVBoxLayout()
        slider6_layout.addWidget(self.slider6)
        slider6_layout.addWidget(self.slider6_label)

        slider7_layout = QVBoxLayout()
        slider7_layout.addWidget(self.slider7)
        slider7_layout.addWidget(self.slider7_label)

        slider_container = QWidget()
        slider_container.setStyleSheet('background-color: rgb(99, 99, 99); '
                                       'border-width: 2px; '
                                       'border-radius:5px')
        slider_container_layout = QHBoxLayout(slider_container)
        slider_container_layout.addLayout(slider1_layout)
        slider_container_layout.addLayout(slider2_layout)
        slider_container_layout.addLayout(slider3_layout)
        slider_container_layout.addLayout(slider4_layout)
        slider_container_layout.addLayout(slider5_layout)
        slider_container_layout.addLayout(slider6_layout)
        slider_container_layout.addLayout(slider7_layout)

        self.start_processing_button = QPushButton("Process", self)
        self.start_processing_button.clicked.connect(self.start_processing)
        self.start_processing_button.setGeometry(50, 400, 200, 30)
        self.start_processing_button.setStyleSheet("QPushButton"
                                           "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")

        self.original_sound_button = QPushButton("Original Sound", self)
        self.original_sound_button.setCheckable(True)
        self.original_sound_button.clicked.connect(self.original_button_clicked)
        self.original_sound_button.setStyleSheet("QPushButton"
                                           "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")

        self.resulting_sound_button = QPushButton("Resulting Sound", self)
        self.resulting_sound_button.setCheckable(True)
        self.resulting_sound_button.clicked.connect(self.resulting_button_clicked)
        self.resulting_sound_button.setStyleSheet("QPushButton"
                                           "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")

        self.load_preset_button = QPushButton("Load Preset", self)
        self.load_preset_button.clicked.connect(self.load_preset)
        self.load_preset_button.setStyleSheet("QPushButton"
                                           "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")

        self.save_preset_button = QPushButton("Save Preset", self)
        self.save_preset_button.clicked.connect(self.save_preset)
        self.save_preset_button.setStyleSheet("QPushButton"
                                           "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_sound)
        self.play_button.setStyleSheet("QPushButton"
                                       "{""background-color : rgb(255, 79, 68);"
                                           "color: white;"
                                           "border-color: gray;"
                                           "border-radius: 5px;}"
                                           "QPushButton::pressed""{""background-color : red;""}")

        button_group1_layout = QHBoxLayout()
        slider_container.setStyleSheet('background-color: rgb(99, 99, 99); '
                                       'border-width: 2px; '
                                       'border-radius:5px')
        button_group1_layout.addWidget(self.choose_input_button)
        button_group1_layout.addWidget(self.choose_output_button)

        button_group2_layout = QHBoxLayout()
        button_group2_layout.addWidget(self.load_preset_button)
        button_group2_layout.addWidget(self.save_preset_button)

        button_group3_layout = QHBoxLayout()
        button_group3_layout.addWidget(self.original_sound_button)
        button_group3_layout.addWidget(self.resulting_sound_button)

        # Create a separate container widgets for button groups
        button_group1_container = QWidget()
        button_group1_container.setStyleSheet('background-color: rgb(99, 99, 99); '
                                              'border-width: 2px; '
                                              'border-radius:5px')
        button_group1_container.setLayout(button_group1_layout)

        button_group2_container = QWidget()
        button_group2_container.setStyleSheet('background-color: rgb(99, 99, 99); '
                                              'border-width: 2px; '
                                              'border-radius:5px')
        button_group2_container.setLayout(button_group2_layout)

        button_group3_container = QWidget()
        button_group3_container.setStyleSheet('background-color: rgb(99, 99, 99); '
                                              'border-width: 2px; '
                                              'border-radius:5px')
        button_group3_container.setLayout(button_group3_layout)

        layout = QVBoxLayout()
        layout.addWidget(button_group1_container)
        layout.addWidget(button_group2_container)
        layout.addWidget(slider_container, alignment=Qt.AlignCenter)
        layout.addWidget(self.start_processing_button)
        layout.addWidget(button_group3_container)
        layout.addWidget(self.play_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(200, 200, 800, 500)  # Set the window geometry (x, y, width, height)
        self.media_player = QMediaPlayer()  # Create a QMediaPlayer instance
        self.setStyleSheet('background-color: rgb(38, 38, 38)')
        #self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255))')
        #self.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.495 rgba(255, 255, 255, 255), stop:0.505 rgba(255, 0, 0, 255), stop:1 rgba(255, 0, 0, 255))')

    def slider1_value_changed(self, value):
        MainWindow.s1value = value
        print('Slider 1 Value:', value)
    def slider2_value_changed(self, value):
        MainWindow.s2value = value
    def slider3_value_changed(self, value):
        MainWindow.s3value = value
    def slider4_value_changed(self, value):
        MainWindow.s4value = value
    def slider5_value_changed(self, value):
        MainWindow.s5value = value
    def slider6_value_changed(self, value):
        MainWindow.s6value = value
    def slider7_value_changed(self, value):
        MainWindow.s7value = value


    def original_button_clicked(self):
        if self.original_sound_button.isChecked():
            self.resulting_sound_button.setChecked(False)  # Uncheck resulting button if original button is checked
            self.original_sound_button.setStyleSheet('background-color: red; color: white')
            self.resulting_sound_button.setStyleSheet('background-color: rgb(255, 79, 68); color: white')


    def resulting_button_clicked(self):
        if self.resulting_sound_button.isChecked():
            self.original_sound_button.setChecked(False)  # Uncheck original button if resulting button is checked
            self.resulting_sound_button.setStyleSheet('background-color: red; color: white')
            self.original_sound_button.setStyleSheet('background-color: rgb(255, 79, 68); color: white')


    def play_sound(self):
        if self.original_sound_button.isChecked():
            content = QMediaContent(QUrl.fromLocalFile(self.input_filepath))  # Load the original audio file
        else:
            content = QMediaContent(QUrl.fromLocalFile(self.output_filepath))  # Load the resulting audio file
        self.media_player.setMedia(content)
        self.media_player.play()  # Play the audio file

    def choose_input_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        filepath, _ = file_dialog.getOpenFileName(self, "Choose Input File", self.input_filepath)
        if filepath:
            self.input_filepath = filepath
            print("Input File Path:", self.input_filepath)

    def choose_output_file(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        filepath, _ = file_dialog.getSaveFileName(self, "Choose Output File", self.output_filepath)
        if filepath:
            self.output_filepath = filepath
            print("Output File Path:", self.output_filepath)

    def load_preset(self):
        pass  # UPDATE TO ADD A WAY TO LOAD PRESET

    def save_preset(self):
        pass  # UPDATE TO ADD A WAY TO SAVE PRESET
    
    def bpf_processing(self, data, samplerate, fy):
        # SAMPLERATE = int(48e3)
        frequency = fy #@param [50, 130, 320, 800, 2000, 5000, 12500]
        center_frequency = int(frequency)
        bpf = SecondOrderBandPass(samplerate, center_frequency)
        processed_wav = []
        for sample in data:
            processed_wav.append(bpf.process_sample(sample))
        processed_wav = np.array(processed_wav)
        return processed_wav
        

    def start_processing(self):
        samplerate, data = wavfile.read(self.input_filepath)
        for cf in range(7):
            if cf == 0:
                center_frequency_modified = 50# + MainWindow.s1value
                scaled_wav = self.bpf_processing(data, samplerate, center_frequency_modified) * pow(10, MainWindow.s1value/20)
                # print(f'{pow(10, MainWindow.s1value/20)}')
            if cf == 1:
                center_frequency_modified = 130
                scaled_wav = self.bpf_processing(data, samplerate, center_frequency_modified) * pow(10, MainWindow.s2value/20) + scaled_wav
            if cf == 2:
                center_frequency_modified = 320
                scaled_wav = self.bpf_processing(data, samplerate, center_frequency_modified) * pow(10, MainWindow.s3value/20) + scaled_wav
            if cf == 3:
                center_frequency_modified = 800
                scaled_wav = self.bpf_processing(data, samplerate, center_frequency_modified) * pow(10, MainWindow.s4value/20) + scaled_wav
            if cf == 4:
                center_frequency_modified = 2000
                scaled_wav = self.bpf_processing(data, samplerate, center_frequency_modified) * pow(10, MainWindow.s5value/20) + scaled_wav
            if cf == 5:
                center_frequency_modified = 5000
                scaled_wav = self.bpf_processing(data, samplerate, center_frequency_modified) * pow(10, MainWindow.s6value/20) + scaled_wav
            if cf == 6:
                center_frequency_modified = 12500
                scaled_wav = self.bpf_processing(data, samplerate, center_frequency_modified) * pow(10, MainWindow.s7value/20) + scaled_wav
        scaled_wav = np.int16(scaled_wav / np.max(np.abs(scaled_wav)) * 32767)
        # plt.figure()
        # plt.plot(scaled_arr)
        # plt.show()
        wavfile.write(self.output_filepath+'_filltered.wav', samplerate, scaled_wav.astype(np.int16))
        print('Done!')  


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
