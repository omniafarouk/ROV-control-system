import cv2
import numpy as np
from StereoVisionProcess import stereoVisionProcess
from Utilities import Utilities


class rectification(stereoVisionProcess):
    def __init__(self, calibrated):
        self.calibrated = calibrated
        self.K1 = self.calibrated.K1
        self.K2 = self.calibrated.K2

        self.left_image = self.calibrated.left_image
        self.right_image = self.calibrated.right_image

        # self.dist0 = np.zeros(5)
        # self.dist1 = np.zeros(5)
        self.image_size = (self.left_image.shape[1], self.left_image.shape[0])
        self.rectified_right = None
        self.rectified_left = None
        self.H2 = None
        self.H1 = None

    def create(self):
        self.Decompose_rectified_images()
        Utilities.detect_and_draw_Epipolar_lines_(self.rectified_left, self.rectified_right,
                                                  "After Rectification Epipolar lines")

    # implementing rectification using uncalibrated methods
    def Decompose_rectified_images(self):
        # Compute homography matrices using stereoRectifyUncalibrated
        homographies = cv2.stereoRectifyUncalibrated(self.calibrated.pts1_inliers, self.calibrated.pts2_inliers,
                                                     self.calibrated.fundamental_mat,
                                                     self.image_size)

        _, self.H1, self.H2 = homographies
        print("Homography Matrix for Left Image with uncalibrated camera:\n", self.H1)
        print("Homography Matrix for Right Image with uncalibrated camera:\n", self.H2)

        # Warp the images to get rectified images
        self.rectified_left = cv2.warpPerspective(self.left_image, self.H1, self.image_size)
        self.rectified_right = cv2.warpPerspective(self.right_image, self.H2, self.image_size)

        print("Rectified Left Image:", np.min(self.rectified_left), np.max(self.rectified_left))
        print("Rectified Right Image:", np.min(self.rectified_right), np.max(self.rectified_right))

        # for showing rectified images
        '''
        rectified_left_resize = cv2.resize(self.rectified_left, (1200, 600))
        rectified_right_resize = cv2.resize(self.rectified_right, (1200, 600))

        
        cv2.imshow('Rectified Left', rectified_left_resize)
        cv2.imshow('Rectified Right', rectified_right_resize)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

    # implement rectification using calibrated methods
    '''
    def Calculate_Homography_Mats(self):
        # Assume you've already computed the following using stereoRectify
        self.R1, self.R2, self.P1, self.P2, self.Q, _, _ = cv2.stereoRectify(self.K1, self.dist0, self.K2,
                                                                             self.dist1, self.image_size,
                                                                             self.calibrated.R,
                                                                             self.calibrated.T,
                                                                             alpha=1)

        # Compute the homography matrices for rectification
        self.H1 = np.dot(np.dot(self.K2, self.R1), np.linalg.inv(self.K1))
        self.H2 = np.dot(np.dot(self.K2, self.R2), np.linalg.inv(self.K2))

        print("Homography Matrix for Left Image:\n", self.H1)
        print("Homography Matrix for Right Image:\n", self.H2)
    

    def get_rectifications(self):
        # Compute the rectification map
        map1x, map1y = cv2.initUndistortRectifyMap(self.K1, self.dist0, self.R1, self.P1, self.image_size, cv2.CV_32FC1)
        map2x, map2y = cv2.initUndistortRectifyMap(self.K2, self.dist1, self.R2, self.P2, self.image_size, cv2.CV_32FC1)

        # Remap the original images to rectify them
        self.rectified_left = cv2.remap(self.calibrated.left_image, map1x, map1y, cv2.INTER_LINEAR)
        self.rectified_right = cv2.remap(self.calibrated.right_image, map2x, map2y, cv2.INTER_LINEAR)

        print(self.Q)
        self.rectified_left = cv2.resize(self.rectified_left, (1200, 600))
        self.rectified_right = cv2.resize(self.rectified_right, (1200, 600))

        print("Map1x range:", np.min(map1x), np.max(map1x))
        print("Map1y range:", np.min(map1y), np.max(map1y))
        print("Map2x range:", np.min(map2x), np.max(map2x))
        print("Map2y range:", np.min(map2y), np.max(map2y))
        print("Rectified Left Image:", np.min(self.rectified_left), np.max(self.rectified_left))
        print("Rectified Right Image:", np.min(self.rectified_right), np.max(self.rectified_right))
        cv2.imshow('Rectified Left', self.rectified_left)
        cv2.imshow('Rectified Right', self.rectified_right)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return self.rectified_left, self.rectified_right, self.Q
        '''
