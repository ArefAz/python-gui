import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QImage

import imagezmq


class WebCamThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.running = True
        self.width = 640
        self.height = 480
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.running:
            ret, self.frame = self.cap.read()
            if ret:
                # self.out.write(frame)
                rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.resize(rgbImage, (self.width, self.height))

                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(
                    rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)

                self.changePixmap.emit(convertToQtFormat)

        # self.changePixmap.emit(convertToQtFormat)


class SockThread(QThread):
    changePixmap = pyqtSignal(QImage)
    imageHub = imagezmq.ImageHub()

    def __init__(self):
        super().__init__()
        self.running = True
        self.width = 640
        self.height = 480

    def run(self):
        while self.running:
            name, self.frame = self.imageHub.recv_image()
            print(name)
            self.imageHub.send_reply(b'OK')
            rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            rgbImage = cv2.resize(rgbImage, (self.width, self.height))
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QtGui.QImage(
                rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)

            self.changePixmap.emit(convertToQtFormat)
