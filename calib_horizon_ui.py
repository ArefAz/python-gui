# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calib_horizon.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from camera_window import CameraWindow
from camera_window_ui import Ui_camera_window


class Ui_calibHorizon_window(object):
    def __init__(self):
        super().__init__()
        self.calib_height = 0
        self.camera_window = CameraWindow()
        self.camera_dist_right = 0
        self.camera_dist_left = 0
        self.camera_dist_front = 0

    def setupUi(self, calibHorizon_window):
        calibHorizon_window.setObjectName("calibHorizon_window")
        calibHorizon_window.resize(250, 250)
        self.calibHorizon_window = calibHorizon_window
        self.centralwidget = QtWidgets.QWidget(calibHorizon_window)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 70, 131, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.height_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.height_label.sizePolicy().hasHeightForWidth())
        self.height_label.setSizePolicy(sizePolicy)
        self.height_label.setObjectName("height_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.height_label)
        self.height_sbx = QtWidgets.QSpinBox(self.layoutWidget)
        self.height_sbx.setMinimum(100)
        self.height_sbx.setMaximum(1000)
        self.height_sbx.setProperty("value", 100)
        self.height_sbx.setDisplayIntegerBase(10)
        self.height_sbx.setObjectName("height_sbx")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.height_sbx)
        self.verticalLayout.addLayout(self.formLayout)
        self.next_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.next_btn.setObjectName("next_btn")
        self.verticalLayout.addWidget(self.next_btn)
        calibHorizon_window.setCentralWidget(self.centralwidget)

        self.set_connection()

        self.retranslateUi(calibHorizon_window)
        QtCore.QMetaObject.connectSlotsByName(calibHorizon_window)

    def retranslateUi(self, calibHorizon_window):
        _translate = QtCore.QCoreApplication.translate
        calibHorizon_window.setWindowTitle(_translate("calibHorizon_window", "Calibration"))
        self.height_label.setText(_translate("calibHorizon_window", "Height (cm)"))
        self.next_btn.setText(_translate("calibHorizon_window", "Next"))

    def set_connection(self):
        self.next_btn.clicked.connect(self.on_next_btn_clicked)

    def on_next_btn_clicked(self):
        self.calib_height = int(self.height_sbx.text())
        self.calibHorizon_window.calib_height = self.calib_height
        self.calibHorizon_window.close()

        return self.calib_height

    def do_calib(self, points, width, depth, dist_to_right, dist_to_left, dist_to_front):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    calibHorizon_window = QtWidgets.QMainWindow()
    ui = Ui_calibHorizon_window()
    ui.setupUi(calibHorizon_window)
    calibHorizon_window.show()
    sys.exit(app.exec_())
