# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calib_4p.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_calib4p_window(object):
    def __init__(self):
        super().__init__()
        self.width = 0
        self.depth = 0

    def setupUi(self, calib4p_window):
        calib4p_window.setObjectName("calib4p_window")
        calib4p_window.resize(250, 250)
        self.calib4p_window = calib4p_window
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(calib4p_window.sizePolicy().hasHeightForWidth())
        calib4p_window.setSizePolicy(sizePolicy)
        calib4p_window.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(calib4p_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 60, 128, 131))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setVerticalSpacing(40)
        self.formLayout.setObjectName("formLayout")
        self.width_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.width_label.sizePolicy().hasHeightForWidth())
        self.width_label.setSizePolicy(sizePolicy)
        self.width_label.setObjectName("width_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.width_label)
        self.width_sbx = QtWidgets.QSpinBox(self.layoutWidget)
        self.width_sbx.setMinimum(100)
        self.width_sbx.setMaximum(1000)
        self.width_sbx.setProperty("value", 100)
        self.width_sbx.setDisplayIntegerBase(10)
        self.width_sbx.setObjectName("width_sbx")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.width_sbx)
        self.depth_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.depth_label.sizePolicy().hasHeightForWidth())
        self.depth_label.setSizePolicy(sizePolicy)
        self.depth_label.setObjectName("depth_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.depth_label)
        self.depth_sbx = QtWidgets.QSpinBox(self.layoutWidget)
        self.depth_sbx.setMinimum(100)
        self.depth_sbx.setMaximum(1000)
        self.depth_sbx.setProperty("value", 100)
        self.depth_sbx.setObjectName("depth_sbx")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.depth_sbx)
        self.verticalLayout.addLayout(self.formLayout)
        self.next_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.next_btn.setObjectName("next_btn")
        self.verticalLayout.addWidget(self.next_btn)
        calib4p_window.setCentralWidget(self.centralwidget)

        self.set_connection()

        self.retranslateUi(calib4p_window)
        QtCore.QMetaObject.connectSlotsByName(calib4p_window)

    def retranslateUi(self, calib4p_window):
        _translate = QtCore.QCoreApplication.translate
        calib4p_window.setWindowTitle(_translate("calib4p_window", "Calibration"))
        self.width_label.setText(_translate("calib4p_window", "Width (cm)"))
        self.depth_label.setText(_translate("calib4p_window", "Depth (cm)"))
        self.next_btn.setText(_translate("calib4p_window", "Next"))

    def set_connection(self):
        self.next_btn.clicked.connect(self.on_next_btn_clicked)

    def on_next_btn_clicked(self):
        self.width = int(self.width_sbx.text())
        self.depth = int(self.depth_sbx.text())

        self.calib4p_window.calib_width = self.width
        self.calib4p_window.calib_depth = self.depth
        self.calib4p_window.close()
        return self.width, self.depth


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    calib4p_window = QtWidgets.QMainWindow()
    ui = Ui_calib4p_window()
    ui.setupUi(calib4p_window)
    calib4p_window.show()
    sys.exit(app.exec_())
