import cv2
import numpy as np
from matplotlib import pyplot as plt

from StereoVisionProcess import stereoVisionProcess
from Utilities import Utilities


class calibration(stereoVisionProcess):
    def __init__(self, left_image, right_image, cam1, cam2):
        self.right_image = right_image
        self.left_image = left_image
        self.K1 = cam1
        self.K2 = cam2

        self.kp0 = None
        self.kp1 = None
        self.matches = None
        self.T = None
        self.R = None

    def Decompose_Matrices(self):
        # Extract matched points
        self.pts1 = np.array([self.kp0[m.queryIdx].pt for m in self.matches])
        self.pts2 = np.array([self.kp1[m.trainIdx].pt for m in self.matches])

        # Estimate fundamental matrix using RANSAC
        self.fundamental_mat, mask = cv2.findFundamentalMat(self.pts1, self.pts2, cv2.FM_RANSAC)
        print("Fundamental Matrix:\n", self.fundamental_mat)

        # Estimate essential matrix (if camera intrinsics are known)
        # Assuming you have the intrinsic matrices K1 and K2
        self.essential_mat = np.dot(self.K2.T, np.dot(self.fundamental_mat, self.K1))

        # Select inlier points
        self.pts1_inliers = self.pts1[mask.ravel() == 1]
        self.pts2_inliers = self.pts2[mask.ravel() == 1]

        _, self.R, self.T, _ = cv2.recoverPose(self.essential_mat, self.pts1_inliers, self.pts2_inliers, self.K1,
                                               self.K2)
        print("Rotation Matrix:\n", self.R)
        print("Translation Vector:\n", self.T)

    def create(self):
        self.kp0,self.kp1,self.matches = Utilities.detect_and_draw_Epipolar_lines_(self.left_image,
                                                        self.right_image, "Calibration Matching Features")
        self.Decompose_Matrices()
