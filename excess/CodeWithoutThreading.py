import pathlib
import sys
import time
from PyQt6.QtWidgets import QApplication
from FIleExplorerDialogue import FileDialogue
import cv2
import numpy as np


def stitch_frames(frame_left, frame_right):
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


def display_Videos(left_video_path, right_video_path):
    cap_left = cv2.VideoCapture(left_video_path)
    cap_right = cv2.VideoCapture(right_video_path)

    if not cap_left.isOpened():
        print("Error opening left video file")
        return
    if not cap_right.isOpened():
        print("Error opening right video file")
        return

    fps_left = cap_left.get(cv2.CAP_PROP_FPS)
    fps_right = cap_right.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / max(fps_left, fps_right))  # Frame delay in milliseconds

    while cap_left.isOpened() and cap_right.isOpened():
        start_time = time.time()

        ret_left, frame_left = cap_left.read()
        ret_right, frame_right = cap_right.read()

        if ret_left:
            frame_left_resized = cv2.resize(frame_left, (1024, 738))
            cv2.imshow('Left Frame', frame_left_resized)

        if ret_right:
            frame_right_resized = cv2.resize(frame_right, (1024, 738))
            cv2.imshow('Right Frame', frame_right_resized)

        if ret_left and ret_right:
            stitched_frame = stitch_frames(frame_left, frame_right)
            if stitched_frame is not None:
                cv2.imshow('Stitched Frame', stitched_frame)

            # Calculate processing time and adjust waitKey delay accordingly
            elapsed_time = (time.time() - start_time) * 1000
            wait_time = max(1, frame_delay - int(elapsed_time))

            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                break

    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()


def Select_video_path():
    app = QApplication(sys.argv)
    window = FileDialogue()
    video_path = FileDialogue().Open_File_dialogue()
    window.show()
    return video_path


def handle_video_path(path_tuple):
    video_path, _ = path_tuple
    return pathlib.Path(video_path[0])


def fix_video_path(video_path):
    new_path = handle_video_path(video_path)
    video_path_string = str(new_path)
    fixed_path = video_path_string.replace("/", "\\\\")
    return fixed_path


if __name__ == "__main__":
    left_video_path = Select_video_path()
    fixed_left_path = fix_video_path(left_video_path)
    print(f"left path after pathlib is {fixed_left_path}")

    right_video_path = Select_video_path()
    fixed_right_path = fix_video_path(right_video_path)
    print(f"right path after pathlib is {fixed_right_path}")

    display_Videos(fixed_left_path, fixed_right_path)
