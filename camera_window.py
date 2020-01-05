from PyQt5 import QtWidgets


class CameraWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.camera_dist_right = 0
        self.camera_dist_left = 0
        self.camera_dist_front = 0

    def closeEvent(self, event):
        super().closeEvent(event)
        print('front dist = ', self.camera_dist_front, ', right dist = ', self.camera_dist_right, ', left dist = ',
              self.camera_dist_left)


