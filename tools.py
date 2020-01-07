import cv2
import time
import datetime
import numpy as np
import os
import sys


# def intersection(self, a,b):
#     x = max(a[0], b[0])
#     y = max(a[1], b[1])
#     w = min(a[0]+a[2], b[0]+b[2]) - x
#     h = min(a[1]+a[3], b[1]+b[3]) - y
#     if w<0 or h<0: return (0,0,0,0)
#       return (x, y, w, h)

# def overlap(a,b):
#     A = self.intersection(a,b)
#     return float(A[2]*A[3])/(a[2]*a[3]) * 100


def IoU(bb1, bb2):
    X1, Y1, W1, H1 = bb1
    X2, Y2, W2, H2 = bb2

    w = max(0, min(X1 + W1 - X2, X2 + W2 - X1))
    h = max(0, min(Y1 + H1 - Y2, Y2 + H2 - Y1))

    S1 = W1 * H1
    S2 = W2 * H2

    s = w * h

    return s / float(S1 + S2 - s)


def ground_norm_dist(bb1, bb2):
    X1, Y1, W1, H1 = bb1
    X2, Y2, W2, H2 = bb2

    dx = (X1 + W1 / 2) - (X2 + W2 / 2)
    dy = (Y1 + H1) - (Y2 + H2)

    return (abs(dx) + abs(dy)) / float(min(W1, W2))


def has_display():
    """
    Determine if display is available
    """

    return os.name != 'posix' or ("DISPLAY" in os.environ)


def get_meta_file_names(video_fname):
    """
    returns 
    """

    fname, ext = os.path.splitext(video_fname)

    prefix = fname[:-4]

    videotime_fname = '%s_rec.tsp' % prefix

    calib_intrinsics_fname = '%s_intrinsics.xml' % prefix

    calib_extrinsics_fname = '%s_extrinsics.xml' % prefix

    fcw_log_fname = '%s_fcw.log' % prefix

    ldw_log_fname = '%s_ldw.log' % prefix

    return videotime_fname, calib_intrinsics_fname, calib_extrinsics_fname, fcw_log_fname, ldw_log_fname


def applyHomography(x, H):
    "applies the homography matrix H on vector x"
    return (H[:-1, :-1].dot(x) + H[:-1, -1]) / (H[-1, :-1].dot(x) + H[-1, -1])


def get_time_string():
    return "%.6f" % time.time()


def get_timestamp():
    timestamp = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-')[:-7]
    return timestamp


def get_date_time():
    date, time = str(datetime.datetime.now()).split()

    time = time.replace(':', '-')[:8]

    return date, time


def imshow(I, delay=0, winname='imshow'):
    I = np.float32(I) / I.max()
    cv2.imshow(winname, I)
    key = cv2.waitKey(delay) & 0xFF

    if key == ord('q'):
        exit()


class Timer:

    def __init__(self):
        self.t0 = 0
        self.t1 = 0

    def tic(self):
        self.t0 = time.time()

    def toc(self, msg='', verbose=True):
        self.t1 = time.time()

        self.dt = self.t1 - self.t0

        if verbose:
            print("%s: %.6f" % (msg, self.dt))

        self.t0 = self.t1

        return self.dt


def draw_lane_region(I, q1, q2, color=[0, 80, 0]):
    [m, n] = I.shape[:2]

    rng = np.arange(0, I.shape[0] - 1, dtype=int)
    y = 1 - np.float64(rng) / m
    x1 = np.int64((q1[0] * y ** 2 + q1[1] * y + q1[2]) * n)
    x2 = np.int64((q2[0] * y ** 2 + q2[1] * y + q2[2]) * n)

    for i in range(0, len(y)):
        cv2.line(I, (x1[i], rng[i]), (x2[i], rng[i]), color, 1)

# def draw_lane_region(I,q1,q2,color=[0,80,0]):
#     [m,n] = I.shape[:2]

#     rng = np.arange(0,I.shape[0]-1,dtype=int)
#     y = 1 - np.float64(rng) / m;
#     x1 = np.int64((q1[0]*y**2 + q1[1] * y + q1[2])*n)
#     x2 = np.int64((q2[0]*y**2 + q2[1] * y + q2[2])*n)

#     for i in range(0,len(y)):
#         cv2.line(I, (x1[i],rng[i]), (x2[i],rng[i]), color, 1)
