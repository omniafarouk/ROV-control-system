# import the require packages.
import time

import cv2
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread


class Create_view(QThread):

    def __init__(self, video_paths, window_name, gui_view) -> None:
        super(Create_view, self).__init__()
        # Declare and initialize instance variables.
        self.video_path = video_paths
        self.gui_view = gui_view
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False
        self.window_name = window_name
        print("starting thread from class")
        self.openedCaptures = []

    def run(self) -> None:
        print("run thread")
        if len(self.video_path) == 1:
            print("1 video path")
            self.display_view_stream()
        else:
            self.stitch_views_stream()

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False

    def display_view_stream(self):
        print(f"displaying view of {self.video_path[0]}")
        cap = cv2.VideoCapture(self.video_path[0])
        if not cap.isOpened():
            print(f"Error opening video file: {self.video_path[0]}")
            return
        while cap.isOpened():
            self.openedCaptures.append(cap)
            print("cap is opened")
            while self.__thread_active:
                if not self.__thread_pause:
                    ret, frame = cap.read()
                    if ret:
                        frame_resized = cv2.resize(frame, (400, 400))
                        qimg = QImage(frame_resized.data, frame_resized.shape[1], frame_resized.shape[0],
                                      QImage.Format.Format_RGB888)
                        pixmap = QPixmap.fromImage(qimg)
                        self.gui_view.label.setPixmap(pixmap)
                        if cv2.waitKey(30) & 0xFF == ord('q'):
                            cap.release()
                            return
                else:
                    print("thread is paused")

    def stitch_views_stream(self):
        cap_left = cv2.VideoCapture(self.video_path[0])
        cap_right = cv2.VideoCapture(self.video_path[1])

        fps_left = cap_left.get(cv2.CAP_PROP_FPS)
        fps_right = cap_right.get(cv2.CAP_PROP_FPS)
        frame_delay = int(1000 / max(fps_left, fps_right))  # Frame delay in milliseconds

        if not cap_left.isOpened() or not cap_right.isOpened():
            print("Error opening video files")
            return

        frame_skip = 2  # Skip every 2 frames
        frame_count = 0

        while cap_left.isOpened() and cap_right.isOpened():
            self.openedCaptures.append(cap_right)
            self.openedCaptures.append(cap_left)
            while self.__thread_active:
                if not self.__thread_pause:
                    start_time = time.time()
                    ret_left, frame_left = cap_left.read()
                    ret_right, frame_right = cap_right.read()

                    if frame_count % frame_skip == 0:
                        if ret_left and ret_right:
                            stitched_frame = self.stitch_frames(frame_left, frame_right)
                            if stitched_frame is not None:
                                frame_resized = cv2.resize(stitched_frame, (400, 400))
                                qimg = QImage(frame_resized.data, frame_resized.shape[1], frame_resized.shape[0],
                                              QImage.Format.Format_RGB888)
                                pixmap = QPixmap.fromImage(qimg)
                                self.gui_view.label.setPixmap(pixmap)
                                # Calculate processing time and adjust waitKey delay accordingly
                                elapsed_time = (time.time() - start_time) * 1000
                                wait_time = max(1, frame_delay - int(elapsed_time))
                                if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                                    cap_left.release()
                                    cap_right.release()
                                    return
                    frame_count += 1

    def stitch_frames(self, frame_left, frame_right):
        dim = (1024, 738)
        frame_left_resized = cv2.resize(frame_left, dim, interpolation=cv2.INTER_AREA)
        frame_right_resized = cv2.resize(frame_right, dim, interpolation=cv2.INTER_AREA)

        images = [frame_left_resized, frame_right_resized]
        stitcher = cv2.Stitcher.create()
        ret, stitched_image = stitcher.stitch(images)

        if ret == cv2.Stitcher_OK:
            final_stitched_image = cv2.resize(stitched_image, (1024, 738), interpolation=cv2.INTER_AREA)
            return final_stitched_image
        else:
            print("Error during stitching")
            return None


    def ReleaseALlCaptures(self):
        for cap in self.openedCaptures:
            cap.release()
        cv2.destroyAllWindows()
