from PyQt5 import QtWidgets

from calib_window import CalibWindow
from threads import WebCamThread, SockThread


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.calib_window = CalibWindow()

        # self.webCam_thread = WebCamThread()
        #
        # self.webCam_thread.start()

        self.stream_thread = WebCamThread()
        self.stream_thread.start()
        self.ui = object()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.stream_thread.running = False
        exit(0)

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        self.stream_thread.width = int(self.ui.stream_label.width())
        self.stream_thread.height = int(self.ui.stream_label.height())

