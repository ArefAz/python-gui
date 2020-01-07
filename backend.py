import os
import sys

import cv2
from PyQt5 import QtWidgets, QtGui

from calib_4p import Ui_calib4p_window
from calib_horizon_ui import Ui_calibHorizon_window
from calib_window import CalibWindow
from main_window import MainWindow
from mainwindowui import Ui_MainWindow


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

        #         calibration_settings
        #         s;
        #         int
        #         status = readSettings("calib/settings.yaml", s);
        #         if (status < 0)
        #             return -1;
        #
        #         FileStorage
        #         fs("calib/intrinsics.xml", FileStorage::READ);
        #         if (!fs.isOpened())
        #         {
        #             printf("Failed to open intrinsics.xml file\n");
        #         return -1;
        #         }
        #         Mat
        #         intrinsics, distortion;
        #         fs["Camera_Matrix"] >> intrinsics;
        #         fs["Distortion_Coefficients"] >> distortion;
        #
        #         Mat
        #         frame;
        #
        #         // VideoCapture
        #         cap(s.camera_id);
        #         // if (!cap.isOpened())
        #         // {
        #
        #     // printf("Failed to open camera\n");
        #     // return -1;
        #     //}
        #
        #     // cap.set(CV_CAP_PROP_FRAME_WIDTH, s.frameSize.width);
        #     // cap.set(CV_CAP_PROP_FRAME_HEIGHT, s.frameSize.height);
        #
        #     bool
        #     freeze = false;
        #
        #     imshow("Select Points", i_frame);
        #     setMouseCallback("Select Points", CallBackFunc);
        #
        #     ptvec.clear();
        #     while (ptvec.size() < 4) {
        #     // cap >> frame;
        #     if (i_frame.empty()) {
        #     printf("Failed to read frames from the camera\n");
        #     return -1;
        #     }
        #
        #     if (!freeze)
        #     resize(i_frame, frame, Size(640, 480));
        #
        #     for (vector < Point2f >::
        #         iterator
        #     point = ptvec.begin();
        #     point != ptvec.end();
        #     point + +) {
        #     circle(frame, *point, 5, Scalar(0, 0, 255), -1);
        #
        # }
        #
        #
        # imshow("Select Points", frame);
        #
        # if ((waitKey(50) & 0XFF) == 32)
        # freeze = true;
        #
        # }
        #
        #
        # destroyWindow("Select Points");
        # vector < Point2f > ptvec_rectified;
        # undistortPoints(ptvec, ptvec_rectified, intrinsics, distortion, Mat(), intrinsics);
        #
        # vector < Point3f > boardPoints;
        # // boardPoints.push_back(Point3f(0.0, 0.0, 0.0));
        # // boardPoints.push_back(Point3f(0.0, 8 * s.squareSize, 0.0));
        # // boardPoints.push_back(Point3f(2 * s.squareSize, 8 * s.squareSize, 0.0));
        # // boardPoints.push_back(Point3f(2 * s.squareSize, 0.0, 0.0));
        #
        # / *double
        # dx = 4720; * /
        # / *double
        # dy = 2600; * /
        #
        # // A4
        # paper(
        # for test)
        # / * double dx = 5000; * /
        # / * double dy = 4100; * /
        #
        # // cout << "Enter width=dist(p1,p2) in mm: ";
        # // cin >> dy;
        #
        # // cout << "Enter depth=dist(p2,p3) in mm: ";
        # // cin >> dx;
        #
        # // cout << "Distance to front in mm: ";
        # // cin >> dist_to_front;
        #
        # // cout << "Distance to right in mm: ";
        # // cin >> dist_to_right;
        #
        # // cout << "Distance to left in mm: ";
        # // cin >> dist_to_left;
        #
        #
        #
        # boardPoints.push_back(Point3f(0.0, 0.0, 0.0));
        # boardPoints.push_back(Point3f(0.0, dy, 0.0));
        # boardPoints.push_back(Point3f(dx, dy, 0.0));
        # boardPoints.push_back(Point3f(dx, 0.0, 0.0));
        #
        #
        # Mat R, t;
        # solvePnP(Mat(boardPoints), Mat(ptvec_rectified), intrinsics, distortion, R, t, false, CV_ITERATIVE);
        #
        # Rodrigues(R, R);
        #
        # Mat C = -R.inv() * t;
        #
        # cout << "C= " << C << endl;
        #
        # Mat u = (Mat_ < double > (2, 1) << R.at < double > (2, 0), R.at < double > (2, 1));
        # u /= norm(u);
        #
        # Mat v = (Mat_ < double > (2, 1) << -R.at < double > (2, 1), R.at < double > (2, 0));
        # v /= norm(v);
        #
        # // Mat d = (Mat_ < double > (2, 1) << C.at < double > (0), C.at < double > (1));
        # // Mat temp, temp2;
        # // vconcat(u.t(), v.t(), temp);
        # // hconcat(temp, -d, temp);
        #
        # // temp2 = (Mat_ < double > (1, 3) << 0.0, 0.0, 1.0);
        # // vconcat(temp, temp2, temp);
        #
        # // Mat Homo = temp.clone();
        # // hconcat(R.col(0), R.col(1), temp);
        # // hconcat(temp, t, temp);
        # // Homo = Homo * (intrinsics * temp).inv();
        #
        #
        # Mat Qb;
        # vconcat(u.t(), v.t(), Qb);
        #
        # Mat zero21 = (Mat_ < double > (2, 1) << 0.0, 0.0);
        # Mat e3T    = (Mat_ < double > (1, 3) << 0.0, 0.0, 1.0);
        #
        # Mat Q;
        # hconcat(Qb, zero21, Q);
        # vconcat(Q, e3T, Q);
        #
        # // Mat Cz0 = C.clone();
        # // Cz0.at < double > (2, 0) = 0;
        #
        #
        # Mat d = -R(Range::
        #     all(), Range(2, 3)) *C.at < double > (2, 0);
        # Mat
        # S = R * Q.t();
        # Mat
        # P;
        # hconcat(S, d, P);
        # P = intrinsics * P;
        #
        # cout << P(Range::all(), Range(0, 2)) << endl;
        # cout << P(Range::all(), Range(3, 4)) << endl;
        #
        # Mat
        # HomoInv;
        # hconcat(P(Range::all(), Range(0, 2)), P(Range::all(), Range(3, 4)), HomoInv); // there
        # must
        # be
        # a
        # samrter
        # way
        # to
        # do
        # this!
        #
        # Mat
        # Homo = HomoInv.inv();
        #
        # cout << Homo << endl;
        #
        # status = writeExtrinsics(2, Homo, R, t, frame.size(),
        #                          dist_to_front, dist_to_right, dist_to_left);
        #
        # if (status < 0)
        # return -1;
        #
        # printf("Saved Results to extrinsics.xml\n");
        #
        # // Show
        # distances
        # char
        # text[255];
        # for (unsigned int i=0;i < 4;i++) {
        #     Mat coords = Homo * (Mat_ < double > (3, 1) << ptvec[i].x, ptvec[i].y, 1.0);
        # coords=coords / coords.at < double > (2);
        #
        # circle(frame, ptvec[i], 5, Scalar(0, 0, 255), -1);
        #
        # sprintf(text, "(%.2f m, %.2f m)", coords.at < double > (0) / 1000, coords.at < double > (1) / 1000);
        # putText(frame, text, ptvec[i], FONT_HERSHEY_SIMPLEX, 0.7, Scalar(0, 0, 255), 2);
        # }
        # imshow("Check", frame);
        # waitKey(20000);
        # destroyWindow("Check");
        # ptvec.clear();
        # return 1;
        pass

    def do_horizon_extrinsic(self, frame, calib_height, camera_dist_front, camera_dist_right,
                             camera_dist_left):

        # TODO

    #         bool
    #         startDrag;
    #         float
    #         horizon_y = 200.0
    #         f;
    #         Mat
    #         frame, displayFrame;
    #         int
    #         LineWidth = 2;
    #
    #         struct
    #         calibration_settings
    #         {
    #             Size
    #         frameSize;
    #         Size
    #         boardSize;
    #         float
    #         squareSize;
    #         int
    #         maxFrames;
    #         float
    #         scale_factor;
    #         int
    #         camera_id;
    #         };
    #
    #         int
    #         readSettings(string
    #         filename, calibration_settings & s)
    #         {
    #             FileStorage
    #         fs(filename, FileStorage::READ );
    #         if (!fs.isOpened())
    #         {
    #         // printf("Failed to open %s file\n", filename);
    #         return -1;
    #         }
    #
    #         s.frameSize.width = fs["FrameSize_Width"];
    #         s.frameSize.height = fs["FrameSize_Height"];
    #         s.boardSize.width = fs["BoardSize_Width"];
    #         s.boardSize.height = fs["BoardSize_Height"];
    #         s.squareSize = fs["Square_Size"];
    #         s.maxFrames = fs["NrOfFramesToUse"];
    #         s.scale_factor = fs["Scale_Factor"];
    #         s.camera_id = fs["Camera_ID"];
    #         fs.release();
    #
    #     return 1;
    #     }
    #
    #
    #
    #     Point2d
    #     applyHomography(Point2d
    #     input, Mat
    #     HomoInv)
    #     {
    #     Mat
    #     point = (Mat_ < double > (3, 1) << input.x, input.y, 1);
    #     Mat
    #     output = HomoInv * point;
    #     output /= output.at < double > (2); // normalize
    #     return Point2d(output.at < double > (0), output.at < double > (1));
    #
    # }
    #
    # void
    # draw_dist_lines(Mat
    # frame, vector < double > distList)
    # {
    # distList.push_back(999999); // adding
    # horizon
    # const
    # int
    # n = distList.size();
    #
    # // Read
    # Homography, dist_to_left and right
    # from extrinsics.xml
    #
    # static
    # Mat
    # homo;
    # static
    # double
    # dist_to_left, dist_to_right;
    #
    # static
    # FileStorage
    # fs("extrinsics.xml", FileStorage::READ);
    # fs["Homography_Matrix"] >> homo;
    # fs["Distance_To_Left"] >> dist_to_left;
    # fs["Distance_To_Right"] >> dist_to_right;
    #
    # Mat
    # HomoInv = homo.inv();
    #
    # char
    # text[50];
    # for (size_t i=0; i < n; i++)
    #     {
    #         Point2d
    #     imagePoint = applyHomography(Point2d(distList[i], 0.0), HomoInv);
    #     double
    #     y = imagePoint.y;
    #     line(frame, Point2d(0.
    #     d, y), Point2d(640.0, y), Scalar(0, 0, 255), LineWidth);
    #
    #     sprintf(text, "%0.1lfm", distList[i]);
    #     if (i == n - 1)
    #     sprintf(text, "%s", "Hor");
    #
    #     putText(frame, text, Point(0, y-5), CV_FONT_HERSHEY_COMPLEX, 0.4, Scalar(0, 0, 255), 1);
    #     }
    #
    # dist_to_left /= 1000.0;
    # dist_to_right /= 1000.0;
    #
    # double
    # dist1 = 0.01; // meters
    # double
    # dist2 = 0.20; // meters
    #
    # Point2d
    # Pc1 = applyHomography(Point2d(dist1, 0), HomoInv);
    # Point2d
    # Pc2 = applyHomography(Point2d(dist2, 0), HomoInv);
    #
    # Point2d
    # Pr1 = applyHomography(Point2d(dist1, -dist_to_right), HomoInv);
    # Point2d
    # Pr2 = applyHomography(Point2d(dist2, -dist_to_right), HomoInv);
    #
    # Point2d
    # Pl1 = applyHomography(Point2d(dist1, dist_to_left), HomoInv);
    # Point2d
    # Pl2 = applyHomography(Point2d(dist2, dist_to_left), HomoInv);
    #
    # line(frame, Pc1, Pc2, Scalar(0, 255, 0), LineWidth);
    # line(frame, Pr1, Pr2, Scalar(0, 255, 0), LineWidth);
    # line(frame, Pl1, Pl2, Scalar(0, 255, 0), LineWidth);
    # }
    #
    # void
    # HorizonCallBackFunc(int
    # event, int
    # x, int
    # y, int
    # flags, void * ustc)
    # {
    # frame.copyTo(displayFrame);
    #
    # if (event == EVENT_LBUTTONDOWN)
    #     {
    #     if (abs(y - horizon_y) < 5)
    #     startDrag = true;
    #     }
    #
    #     if (startDrag & & event == EVENT_MOUSEMOVE)
    #         {
    #             horizon_y = y;
    #         }
    #
    #         if (event == EVENT_LBUTTONUP)
    #             startDrag = false;
    #
    #         line(displayFrame, Point2f(0.
    #         f, horizon_y), Point(640.
    #         f, horizon_y), Scalar(0, 0, 255), LineWidth);
    #         imshow("Drag Horizon", displayFrame);
    #         }
    #
    #         int
    #         do_extrinsic_calibration_horizon()
    #         {
    #         float
    #         cameraHeight;
    #         cout << "Enter camera height(m)" << endl;
    #         cin >> cameraHeight;
    #
    #         calibration_settings
    #         s;
    #         int
    #         status = readSettings("settings.yaml", s);
    #         if (status < 0)
    #             return -1;
    #
    #         FileStorage
    #         fs("intrinsics.xml", FileStorage::READ);
    #         if (!fs.isOpened())
    #         {
    #             printf("Failed to open intrinsics.xml file\n");
    #         return -1;
    #         }
    #
    #         Mat
    #         intrinsics;
    #         fs["Camera_Matrix"] >> intrinsics;
    #         fs.release();
    #
    #         VideoCapture
    #         cap(s.camera_id);
    #         if (!cap.isOpened())
    #         {
    #         printf("Failed to open camera\n");
    #         return -1;
    #         }
    #
    #         cap.set(CV_CAP_PROP_FRAME_WIDTH, s.frameSize.width);
    #         cap.set(CV_CAP_PROP_FRAME_HEIGHT, s.frameSize.height);
    #
    #         while (cap.isOpened())
    #             {
    #                 cap >> frame;
    #             frame.copyTo(displayFrame);
    #             line(displayFrame, Point2f(0.
    #             f, horizon_y), Point(640.
    #             f, horizon_y), Scalar(0, 0, 255), LineWidth);
    #             imshow("Drag Horizon", displayFrame);
    #
    #             if ((waitKey(50) & 0XFF) == 32)
    #             break;
    #         else
    #         setMouseCallback("Drag Horizon", HorizonCallBackFunc);
    #         }
    #         destroyWindow("Drag Horizon");
    #
    #         double
    #         c_y = intrinsics.at < double > (1, 2);
    #         double
    #         alpha_y = intrinsics.at < double > (1, 1);
    #
    #         double
    #         theta = atan((c_y - horizon_y) / alpha_y);
    #         cout << "Camera Pith Angle " << theta * 180 / 3.14 << endl;
    #
    #         Mat
    #         R = (Mat_ < double > (3, 3) << 0, -1, 0,
    #         -sin(theta), 0, -cos(theta),
    #         cos(theta), 0, -sin(theta));
    #
    #         Mat
    #         t = (Mat_ < double > (3, 1) << 0, cameraHeight * cos(theta), cameraHeight * sin(theta));
    #
    #         Mat
    #         P;
    #         hconcat(R, t, P);
    #         P = intrinsics * P;
    #
    #         Mat
    #         HomoInv;
    #         vector < Mat > temp = {P.col(0), P.col(1), P.col(3)};
    #         hconcat(temp, HomoInv);
    #
    #         Mat
    #         Homo = HomoInv.inv();
    #
    #         double
    #         dist_to_left, dist_to_right, dist_to_front;
    #         cout << "Enter distance to left(mm)" << endl;
    #         cin >> dist_to_left;
    #         cout << "Enter distance to right(mm)" << endl;
    #         cin >> dist_to_right;
    #         cout << "Enter distance to front(mm)" << endl;
    #         cin >> dist_to_front;
    #
    #         // Save
    #         extrinsics.xml
    #         fs.open("extrinsics.xml", FileStorage::WRITE );
    #         if (!fs.isOpened())
    #         {
    #         printf("Failed to open extrinsics.xml\n");
    #         return -1;
    #         }
    #
    #         time_t
    #         tm;
    #         time( & tm );
    #         struct
    #         tm * t2 = localtime( & tm );
    #         char
    #         buf[1024];
    #         strftime(buf, sizeof(buf) - 1, "%c", t2);
    #
    #         fs << "calibration_Time" << buf;
    #         fs << "image_Width" << frame.cols;
    #         fs << "image_Height" << frame.rows;
    #         fs << "Rotation_Matrix" << R;
    #         fs << "Translation_Matrix" << t;
    #         fs << "Homography_Matrix" << Homo;
    #         fs << "Distance_To_Left" << dist_to_left;
    #         fs << "Distance_To_Right" << dist_to_right;
    #         fs << "Distance_To_Front" << dist_to_front;
    #         fs << "Camera_Height" << cameraHeight;
    #         fs << "Camera_Pitch_Angle" << theta;
    #         fs << "Horizon_Y_in_Pixel" << horizon_y;
    #         fs.release();
    #
    #         vector < double > distanceList = {0.05, 0.10, 0.20, 0.30, 0.50};
    #         while (cap.isOpened())
    #             {
    #                 cap >> frame;
    #             draw_dist_lines(frame, distanceList);
    #             imshow("Results", frame);
    #             waitKey(1);
    #             }
    #
    #             cap.release();
    #             return 1;
    #             }
    #
    #
    #
    #             int
    #             main()
    #             {
    #             do_extrinsic_calibration_horizon();
    #             return 0;
    #             }
    #
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
