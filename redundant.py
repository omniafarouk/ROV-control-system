import numpy as np
import cv2
import matplotlib.pyplot as plt

def estimate_disparity(left_image, right_image, window_size=5):
    """
    Estimates disparity using the block matching algorithm.

    Args:
        left_image: The left image.
        right_image: The right image.
        window_size: The size of the matching window.

    Returns:
        The estimated disparity map.
    """

    height, width = left_image.shape[:2]
    disparity_map = np.zeros((height, width))

    for y in range(window_size // 2, height - window_size // 2):
        for x in range(window_size // 2, width - window_size // 2):
            left_window = left_image[y - window_size // 2:y + window_size // 2 + 1,
                                     x - window_size // 2:x + window_size // 2 + 1]
            best_disparity = 0
            min_ssd = np.inf

            for d in range(1, window_size):
                right_window = right_image[y - window_size // 2:y + window_size // 2 + 1,
                                          x - window_size // 2 - d:x + window_size // 2 - d + 1]
                ssd = np.sum((left_window - right_window) ** 2)

                if ssd < min_ssd:
                    min_ssd = ssd
                    best_disparity = d

            disparity_map[y, x] = best_disparity

    return disparity_map

def rescale_disparity(disparity_map):
    """
    Rescales the disparity map to the range [0, 255].

    Args:
        disparity_map: The disparity map.

    Returns:
        The rescaled disparity map.
    """

    min_disparity = np.min(disparity_map)
    max_disparity = np.max(disparity_map)

    rescaled_disparity_map = (disparity_map - min_disparity) / (max_disparity - min_disparity) * 255
    rescaled_disparity_map = rescaled_disparity_map.astype(np.uint8)

    return rescaled_disparity_map

def save_disparity_images(disparity_map, filename):
    """
    Saves the disparity map as grayscale and color images.

    Args:
        disparity_map: The disparity map.
        filename: The filename for the saved images.
    """

    # Grayscale image
    cv2.imwrite(filename + "_grayscale.png", disparity_map)

    # Color image (heat map)
    plt.imshow(disparity_map, cmap='jet', interpolation='nearest')
    plt.colorbar()
    plt.savefig(filename + "_color.png")
    plt.close()

# Load images
left_image = cv2.imread('left_image.jpg')
right_image = cv2.imread('right_image.jpg')

# Estimate disparity
disparity_map = estimate_disparity(left_image, right_image)

# Rescale disparity
rescaled_disparity_map = rescale_disparity(disparity_map)

# Save disparity images
save_disparity_images(rescaled_disparity_map, 'disparity')
