# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_camera_window(object):
    def setupUi(self, camera_window):
        camera_window.setObjectName("camera_window")
        camera_window.resize(250, 300)
        self.camera_window = camera_window
        self.centralwidget = QtWidgets.QWidget(camera_window)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 60, 183, 181))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(-1, -1, -1, 0)
        self.formLayout.setVerticalSpacing(40)
        self.formLayout.setObjectName("formLayout")
        self.front_dist_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.front_dist_label.sizePolicy().hasHeightForWidth())
        self.front_dist_label.setSizePolicy(sizePolicy)
        self.front_dist_label.setObjectName("front_dist_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.front_dist_label)
        self.front_dist_sbx = QtWidgets.QSpinBox(self.layoutWidget)
        self.front_dist_sbx.setMinimum(0)
        self.front_dist_sbx.setMaximum(1000)
        self.front_dist_sbx.setProperty("value", 50)
        self.front_dist_sbx.setDisplayIntegerBase(10)
        self.front_dist_sbx.setObjectName("front_dist_sbx")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.front_dist_sbx)
        self.right_dist_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_dist_label.sizePolicy().hasHeightForWidth())
        self.right_dist_label.setSizePolicy(sizePolicy)
        self.right_dist_label.setObjectName("right_dist_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.right_dist_label)
        self.right_dist_sbx = QtWidgets.QSpinBox(self.layoutWidget)
        self.right_dist_sbx.setMinimum(0)
        self.right_dist_sbx.setMaximum(1000)
        self.right_dist_sbx.setProperty("value", 50)
        self.right_dist_sbx.setObjectName("right_dist_sbx")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.right_dist_sbx)
        self.left_dist_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_dist_label.sizePolicy().hasHeightForWidth())
        self.left_dist_label.setSizePolicy(sizePolicy)
        self.left_dist_label.setObjectName("left_dist_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.left_dist_label)
        self.left_dist_sbx = QtWidgets.QSpinBox(self.layoutWidget)
        self.left_dist_sbx.setMinimum(0)
        self.left_dist_sbx.setMaximum(1000)
        self.left_dist_sbx.setProperty("value", 50)
        self.left_dist_sbx.setObjectName("left_dist_sbx")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.left_dist_sbx)
        self.verticalLayout.addLayout(self.formLayout)
        self.next_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.next_btn.setObjectName("next_btn")
        self.verticalLayout.addWidget(self.next_btn)
        camera_window.setCentralWidget(self.centralwidget)

        self.set_connection()

        self.retranslateUi(camera_window)
        QtCore.QMetaObject.connectSlotsByName(camera_window)

    def set_connection(self):
        self.next_btn.clicked.connect(self.on_next_btn_clicked)

    def on_next_btn_clicked(self):
        self.dist_right = int(self.right_dist_sbx.text())
        self.dist_left = int(self.left_dist_sbx.text())
        self.dist_front = int(self.front_dist_sbx.text())
        self.camera_window.camera_dist_right = self.dist_right
        self.camera_window.camera_dist_left = self.dist_left
        self.camera_window.camera_dist_front = self.dist_front

        self.camera_window.close()


    def retranslateUi(self, camera_window):
        _translate = QtCore.QCoreApplication.translate
        camera_window.setWindowTitle(_translate("camera_window", "Camera"))
        self.front_dist_label.setText(_translate("camera_window", "Distance to Front (cm)"))
        self.right_dist_label.setText(_translate("camera_window", "Distance to Right (cm)"))
        self.left_dist_label.setText(_translate("camera_window", "Distance to Left (cm)"))
        self.next_btn.setText(_translate("camera_window", "Finish"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    camera_window = QtWidgets.QMainWindow()
    ui = Ui_camera_window()
    ui.setupUi(camera_window)
    camera_window.show()
    sys.exit(app.exec_())
