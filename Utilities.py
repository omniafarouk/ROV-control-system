import cv2


class Utilities:

    # the class isn't used for creating instances only static methods
    def __init__(self):
        raise TypeError("This class cannot be instantiated")

    @staticmethod
    def detect_and_draw_Epipolar_lines_(left_image,right_image,win_name):
        # Initialize SIFT detector
        sift = cv2.SIFT.create()

        # Detect SIFT features and compute descriptors
        kp0, dest0 = sift.detectAndCompute(left_image, None)
        kp1, dest1 = sift.detectAndCompute(right_image, None)
        # Use BFMatcher or FLANN to match descriptors
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(dest0, dest1)
        '''

        # Create BFMatcher object
        bf = cv2.BFMatcher()
        # Match descriptors by KnnMatch first to match the object with its nearest neightbor first
        # to ensure best match
        matches_unfiltered = bf.knnMatch(self.descriptors[0], self.descriptors[1], k=2)

        # Apply ratio test
        self.matches = []
        for m, n in matches_unfiltered:
            if m.distance < 0.75 * n.distance:
                self.matches.append(n)
        '''

        # Sort the matches based on distance (best matches first)
        matches = sorted(matches, key=lambda x: x.distance)
        matched_image = cv2.drawMatches(left_image, kp0, right_image, kp1,
                                        matches[:50], None
                                        , flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        displayed_image = cv2.resize(matched_image, (1200, 600))
        cv2.imshow(win_name, displayed_image)
        # Set the window size and keep aspect ratio
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return kp0,kp1,matches
