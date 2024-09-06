import cv2
import numpy as np
import matplotlib.pyplot as plt

from StereoVisionProcess import stereoVisionProcess


class depthComputation(stereoVisionProcess):
    def __init__(self, disparity, Cam0, baseline):
        self.disparity_map = disparity.disparity_map
        self.K = Cam0  # to calculate focal length in pixels
        self.baseline = baseline/1000  # baseline in mm so change it into m
        self.filename = "depth"

    def setFileName(self,fileName):
        self.filename = fileName

    def calculate_and_display_depth(self):
        focal_length = self.K[0][0]
        # Calculate depth
        depth_map = self.baseline * focal_length / self.disparity_map

        # Normalize depth
        min_depth = np.min(depth_map)
        max_depth = np.max(depth_map)
        normalized_depth_map = (depth_map - min_depth) / (max_depth - min_depth) * 255

        # Save grayscale image
        cv2.imwrite(f"{self.filename}_grayscale.png", normalized_depth_map.astype(np.uint8))

        # Save color image (heat map)
        plt.imshow(normalized_depth_map, cmap='jet', interpolation='nearest')
        plt.colorbar()
        plt.savefig(f"{self.filename}_color.png")
        plt.close()

    def create(self):
        self.calculate_and_display_depth()
