from PyQt5 import QtWidgets

from camera_window import CameraWindow
from camera_window_ui import Ui_camera_window


class CalibWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.calib_height = 0
        self.calib_width = 0
        self.calib_depth = 0
        self.camera_window = CameraWindow()

    def closeEvent(self, event):
        super().closeEvent(event)
        print('calibration height = ', self.calib_height, ', calibration depth = ', self.calib_depth,
              ', calibration width = ',
              self.calib_width)
        self.ui = Ui_camera_window()
        self.ui.setupUi(self.camera_window)
        self.camera_window.show()
