import cv2
import numpy as np
from matplotlib import pyplot as plt

from StereoVisionProcess import stereoVisionProcess


class disparity(stereoVisionProcess):
    def __init__(self, vmin, vmax, ndisp, rectified):
        self.rescaled_disparity_Map = None
        self.disparity_map = None
        self.filename = "Disparity_Map"
        self.vmin = vmin
        self.vmax = vmax
        self.left_img = rectified.rectified_left
        self.right_img = rectified.rectified_right
        self.block_size = 5
        self.ndisp = ndisp

    def setBlockSize(self, block_size):
        self.block_size = block_size

    def setFilename(self, fileName):
        self.filename = fileName

    def compute_disparity_bm(self):
        # Ensure that both images are grayscale
        if self.left_img.ndim == 3 and self.left_img.shape[2] == 3:
            self.left_img = cv2.cvtColor(self.left_img, cv2.COLOR_BGR2GRAY)
        if self.right_img.ndim == 3 and self.right_img.shape[2] == 3:
            self.right_img = cv2.cvtColor(self.right_img, cv2.COLOR_BGR2GRAY)
        # Create StereoBM object
        print("creating object")
        stereo = cv2.StereoBM.create(numDisparities=self.ndisp, blockSize=self.block_size)

        # Compute disparity map
        print("Calculating disparity map...")
        disparity_map = stereo.compute(self.left_img, self.right_img).astype(np.float32) / 16.0
        self.disparity_map = disparity_map

    def block_matching(self, block_size):
        height, width = self.left_img.shape[:2]
        disparity_map = np.zeros((height, width), dtype=np.float32)

        for y in range(block_size, height - block_size):
            for x in range(block_size, width - block_size):
                block = self.left_img[y - block_size:y + block_size + 1, x - block_size:x + block_size + 1]
                min_ssd = float('inf')
                best_disp = 0

                for disp in range(self.vmin, self.vmax):
                    if x - disp >= block_size:  # Ensure valid block position
                        right_block = self.right_img[y - block_size:y + block_size + 1,
                                      x - disp - block_size:x - disp + block_size + 1]
                        ssd = np.sum((block - right_block) ** 2)
                        if ssd < min_ssd:
                            min_ssd = ssd
                            best_disp = disp

                disparity_map[y, x] = best_disp
                print(f"Best disparity at ({y}, {x}) is {best_disp}")

        print("Disparity Map computation complete.")
        self.disparity_map = disparity_map

    def rescale_disparity(self):
        # Rescales the disparity map to the range [0, 255].

        min_disparity = np.min(self.disparity_map)
        max_disparity = np.max(self.disparity_map)

        rescaled_disparity_map = (self.disparity_map - min_disparity) / (max_disparity - min_disparity) * 255
        rescaled_disparity_map = rescaled_disparity_map.astype(np.uint8)

        self.rescaled_disparity_Map = rescaled_disparity_map

    def save_disparity_images(self):
        # Saves the disparity map as grayscale and color images

        # Grayscale image
        cv2.imwrite(self.filename + "_grayscale.png", self.disparity_map)

        # Color image (heat map)
        plt.imshow(self.disparity_map, cmap='jet', interpolation='nearest')
        plt.colorbar()
        plt.savefig(self.filename + "_color.png")
        plt.close()

        cv2.imshow("depth Map", self.disparity_map)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def create(self):
        # self.block_matching(self.block_size)
        self.compute_disparity_bm()
        self.rescale_disparity()
        self.save_disparity_images()
