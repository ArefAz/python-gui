import os
import sys

import cv2
from PyQt5 import QtWidgets, QtGui

from calib_window import CalibWindow
from main_window import MainWindow
from mainwindowui import Ui_MainWindow
from calib_4p import Ui_calib4p_window
from calib_horizon_ui import Ui_calibHorizon_window


class UIBackend(Ui_MainWindow):
    def __init__(self, main_window):

        super().__init__()
        super().setupUi(main_window)

        self.main_window = main_window

        self.calib_height = 0
        self.calib_width = 0
        self.calib_depth = 0
        self.camera_dist_right = 0
        self.camera_dist_left = 0
        self.camera_dist_front = 0
        self.calib_frame = []

        self.calib_window = CalibWindow()

        self.set_connections()
        self.set_setting()

    def set_setting(self):
        settings = self.readWrite_settings(mode='read')
        checks = []

        for setting in settings[2:]:
            checks.append((setting.split(' ')[0], setting.split(' ')[-1]))

        self.FCW_chb.setChecked(True) if checks[0][1] == 'Checked' else self.FCW_chb.setChecked(False)
        self.ldw_chb.setChecked(True) if checks[1][1] == 'Checked' else self.ldw_chb.setChecked(False)
        self.save_in_chb.setChecked(True) if checks[2][1] == 'Checked' else self.save_in_chb.setChecked(False)
        self.save_out_chb.setChecked(True) if checks[3][1] == 'Checked' else self.save_out_chb.setChecked(False)
        self.save_fcw_chb.setChecked(True) if checks[4][1] == 'Checked' else self.save_fcw_chb.setChecked(False)
        self.save_ldw_chb.setChecked(True) if checks[5][1] == 'Checked' else self.save_ldw_chb.setChecked(False)
        self.alaram_chb.setChecked(True) if checks[6][1] == 'Checked' else self.alaram_chb.setChecked(False)
        self.roi_chb.setChecked(True) if checks[7][1] == 'Checked' else self.roi_chb.setChecked(False)
        self.tracker_chb.setChecked(True) if checks[8][1] == 'Checked' else self.tracker_chb.setChecked(False)
        self.show_detect_chb.setChecked(True) if checks[9][1] == 'Checked' else self.show_detect_chb.setChecked(False)
        self.show_ttc_chb.setChecked(True) if checks[10][1] == 'Checked' else self.show_ttc_chb.setChecked(False)
        self.show_dist_chb.setChecked(True) if checks[11][1] == 'Checked' else self.show_dist_chb.setChecked(False)
        self.display_chb.setChecked(True) if checks[12][1] == 'Checked' else self.display_chb.setChecked(False)
        self.regressor_chb.setChecked(True) if checks[13][1] == 'Checked' else self.regressor_chb.setChecked(False)

    def set_connections(self):

        self.install_btn.clicked.connect(self.on_install_btn_clicked)
        self.run_btn.clicked.connect(self.on_run_btn_clicked)
        self.stop_btn.clicked.connect(self.on_stop_btn_clicked)
        self.reboot_btn.clicked.connect(self.on_reboot_btn_clicked)

        self.calib4p_btn.clicked.connect(self.on_calib4p_btn_clicked)
        self.calibHorizon_btn.clicked.connect(self.on_calibHorizon_btn_clicked)

        self.calib_4p_ok_btn.clicked.connect(self.on_calib_4p_ok_btn_clicked)
        self.calib_horizon_ok_btn.clicked.connect(self.on_calib_horizon_ok_btn_clicked)

        self.main_window.stream_thread.changePixmap.connect(self.setImage)

        self.FCW_chb.stateChanged.connect(self.on_check_change)
        self.ldw_chb.stateChanged.connect(self.on_check_change)
        self.save_in_chb.stateChanged.connect(self.on_check_change)
        self.save_out_chb.stateChanged.connect(self.on_check_change)
        self.save_fcw_chb.stateChanged.connect(self.on_check_change)
        self.save_ldw_chb.stateChanged.connect(self.on_check_change)
        self.alaram_chb.stateChanged.connect(self.on_check_change)
        self.show_dist_chb.stateChanged.connect(self.on_check_change)
        self.show_detect_chb.stateChanged.connect(self.on_check_change)
        self.show_ttc_chb.stateChanged.connect(self.on_check_change)
        self.display_chb.stateChanged.connect(self.on_check_change)
        self.regressor_chb.stateChanged.connect(self.on_check_change)
        self.tracker_chb.stateChanged.connect(self.on_check_change)

    def on_check_change(self):
        self.readWrite_settings(mode='save')
        return

    def on_calib4p_btn_clicked(self):

        self.points = []
        self.points_count = 0

        cv2.namedWindow('Select Points')
        cv2.setMouseCallback('Select Points', self.call_back_func_4p)
        while True:
            display_frame = self.main_window.stream_thread.frame.copy()
            for point in self.points:
                cv2.circle(display_frame, point, 5, (255, 0, 255), -1)
            cv2.imshow('Select Points', display_frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord(' ') and self.points_count >= 4:
                cv2.destroyWindow('Select Points')
                self.ui = Ui_calib4p_window()
                self.ui.setupUi(self.calib_window)
                self.calib_frame = display_frame
                self.calib_window.show()

                break

        return self.points

    def on_calibHorizon_btn_clicked(self):

        self.horizon_height = 200
        self.dragging = False

        cv2.namedWindow('Set Horizon')
        line_width = 2
        cv2.setMouseCallback('Set Horizon', self.call_back_func_horizon)
        while True:
            display_frame = self.main_window.stream_thread.frame.copy()
            cv2.line(display_frame, (0, self.horizon_height), (640, self.horizon_height), (255, 255, 0),
                     line_width)
            cv2.imshow('Set Horizon', display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                cv2.destroyWindow('Set Horizon')
                self.ui = Ui_calibHorizon_window()
                self.ui.setupUi(self.calib_window)
                self.calib_frame = display_frame
                self.calib_window.show()

                break
            # elif key == ord(' '):
            #     stopped_frame = self.webCam_thread.frame.copy()
            #     cv2.line(stopped_frame, (0, self.horizon_height), (640, self.horizon_height), (255, 255, 0),
            #              line_width)
            #     cv2.imshow('Set Horizon', stopped_frame)
            #     cv2.waitKey()
        return self.horizon_height

    def call_back_func_4p(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP and self.points_count < 4:
            point = (x, y)
            self.points.append(point)
            self.points_count += 1
        elif self.points_count >= 4:
            pass
        return

    def call_back_func_horizon(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN and abs(y - self.horizon_height) < 5:
            self.dragging = True

        if event == cv2.EVENT_MOUSEMOVE and self.dragging:
            self.horizon_height = y

        if event == cv2.EVENT_LBUTTONUP:
            self.dragging = False

    def on_install_btn_clicked(self):
        self.create_startup()
        self.status.setText('status: installing')
        cmd = 'python remote.py ' + self.username_text.text() + '@' + self.user_IP_text.text() + ' install &'
        print(cmd)
        os.system(cmd)
        self.status.setText('status: installed')

    def on_run_btn_clicked(self):
        cmd = 'python remote.py ' + self.username_text.text() + '@' + self.user_IP_text.text() + ' run &'
        print(cmd)
        os.system(cmd)
        self.status.setText('status: running')

    def on_stop_btn_clicked(self):
        cmd = 'python remote.py ' + self.username_text.text() + '@' + self.user_IP_text.text() + ' stop &'
        print(cmd)
        os.system(cmd)
        self.status.setText('status: stopped')

    def on_reboot_btn_clicked(self):
        cmd = 'python remote.py ' + self.username_text.text() + '@' + self.user_IP_text.text() + ' reboot &'
        print(cmd)
        os.system(cmd)
        self.status.setText('status: ready')

    def on_calib_4p_ok_btn_clicked(self):
        self.calib_width = self.calib_window.calib_width
        self.calib_depth = self.calib_window.calib_depth
        self.calib_height = self.calib_window.calib_height
        self.camera_dist_left = self.calib_window.camera_window.camera_dist_left
        self.camera_dist_right = self.calib_window.camera_window.camera_dist_right
        self.camera_dist_front = self.calib_window.camera_window.camera_dist_front

        print()
        print('calibration height =  ', self.calib_height, ', calibration depth =  ', self.calib_depth,
              'calibration width =  ', self.calib_width)
        print('left dist = ', self.camera_dist_left, ', right dist = ', self.camera_dist_right, ', front dist = ',
              self.camera_dist_front)
        print()

        self.do_4p_extrinsic(self.calib_frame, self.calib_depth, self.calib_width, self.camera_dist_front,
                             self.camera_dist_right, self.camera_dist_left)

    def on_calib_horizon_ok_btn_clicked(self):
        self.calib_width = self.calib_window.calib_width
        self.calib_depth = self.calib_window.calib_depth
        self.calib_height = self.calib_window.calib_height
        self.camera_dist_left = self.calib_window.camera_window.camera_dist_left
        self.camera_dist_right = self.calib_window.camera_window.camera_dist_right
        self.camera_dist_front = self.calib_window.camera_window.camera_dist_front

        print()
        print('calibration height =  ', self.calib_height, ', calibration depth =  ', self.calib_depth,
              'calibration width =  ', self.calib_width)
        print('left dist = ', self.camera_dist_left, ', right dist = ', self.camera_dist_right, ', front dist = ',
              self.camera_dist_front)
        print()

        self.do_horizon_extrinsic(self.calib_frame, self.calib_height, self.camera_dist_front, self.camera_dist_right,
                                  self.camera_dist_left)

    def do_4p_extrinsic(self, frame, calib_depth, calib_width, camera_dist_front, camera_dist_right, camera_dist_left):
        # TODO
        pass

    def do_horizon_extrinsic(self, frame, calib_height, camera_dist_front, camera_dist_right,
                             camera_dist_left):
        # TODO
        pass

    def setImage(self, image):
        self.stream_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def create_startup(self):
        with open('startup.sh', 'w') as file:
            file.write("#! /bin/bash\n")
            file.write("echo ------------------------------------ &>> i-drive.log\n")
            file.write("echo \"starting i-drive...\" &>> i-drive.log\n")
            file.write("date &>> i-drive.log\n")
            file.write("sudo killall -q -9 python \n")
            file.write("cd /home/%s/i-drive/ \n" % self.username_text.text())
            file.write("export DISPLAY=:0\n")
            file.write("while true; do\n")
            file.write("    echo \"starting program...\" &>> i-drive.log \n")
            file.write("    python main.pyc")

            if self.FCW_chb.isChecked():
                file.write(" --fcw on ")
            else:
                file.write(" --fcw off")

            if self.ldw_chb.isChecked():
                file.write(" --ldw on")
            else:
                file.write(" --ldw off")

            if self.alaram_chb.isChecked():
                file.write(' --alaram on')
            else:
                file.write(' --alarm off')

            if self.regressor_chb.isChecked():
                file.write(' --regressor on')
            else:
                file.write(' --regressor off')

            if self.tracker_chb.isChecked():
                file.write(' --tracker fast')
            else:
                file.write(' --tracker off')

            if self.display_chb.isChecked():
                file.write(' --gui on')
            else:
                file.write(' --gui off')

            if self.roi_chb.isChecked():
                file.write(' --show-roi')

            if self.save_fcw_chb.isChecked():
                file.write(' --save-fcw')

            if self.save_ldw_chb.isChecked():
                file.write(' --save-ldw')

            if self.save_in_chb.isChecked():
                file.write(' --save-input')

            if self.save_out_chb.isChecked():
                file.write(' --save-output')

            if self.show_detect_chb.isChecked():
                file.write(' --show-detections')

            if self.show_dist_chb.isChecked():
                file.write(' --show-dist')

            if self.show_ttc_chb.isChecked():
                file.write(' --show-real-ttc')

            file.write("&>> i-drive.log\n")
            file.write("    echo \"program ended (status: $?)\" &>> i-drive.log\n")
            file.write('done\n')

            file.close()

    def readWrite_settings(self, mode='read', filename='default_values.yaml'):

        if mode == 'read':
            with open(filename, 'r') as file:
                text = file.read()
                setting = text.splitlines()
        elif mode == 'save':
            with open(filename, 'w') as file:
                setting = ''
                setting += 'user = ' + self.username_text.text() + '\n'
                setting += 'ip = ' + self.user_IP_text.text() + '\n'
                setting += 'FCW = ' + ('Checked' if self.FCW_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'LDW = ' + ('Checked' if self.ldw_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Save-Input = ' + ('Checked' if self.save_in_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Save-Output = ' + ('Checked' if self.save_out_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Save-FCW = ' + ('Checked' if self.save_fcw_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Save-LDW = ' + ('Checked' if self.save_ldw_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Alarm = ' + ('Checked' if self.alaram_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Show-ROI = ' + ('Checked' if self.roi_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Tracker = ' + ('Checked' if self.tracker_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Show-Detections = ' + (
                    'Checked' if self.show_detect_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Show-TTC = ' + ('Checked' if self.show_ttc_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Show-dist = ' + ('Checked' if self.show_dist_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Display = ' + ('Checked' if self.display_chb.isChecked() else 'Unchecked') + '\n'
                setting += 'Regressor = ' + ('Checked' if self.regressor_chb.isChecked() else 'Unchecked') + '\n'
                file.write(setting)
        else:
            print('Wrong mode entered!')
            exit(-1)

        return setting

    # def closeEvent(self):


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()

    ui_backend = UIBackend(main_window)
    main_window.ui = ui_backend

    main_window.show()

    sys.exit(app.exec_())
