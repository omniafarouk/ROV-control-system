import pathlib
import sys
import threading
import time
from PyQt6.QtWidgets import QApplication
from FIleExplorerDialogue import FileDialogue
import cv2

# to improve code functionality , use multithreading , error handle any crashes,
# write the resulted video if needed, for faster processing , can use lower resolution or drop frames
# for speed’s sake , calculate the best wait time frame rate between the videos synchronization
# can use cv2.INTER_LINEAR instead of cv2.INTER_AREA for more optimization (**see the difference)


# for the Algorithm stitch library in opencv package is used for simplicity as there is no major processing
# or usage for objects controlling

def stitch_frames(frame_left, frame_right):
    # Resize frames to the desired dimension
    # * different from the previous resizing for flexibility of different displays and processing
    dim = (1024, 738)
    frame_left_resized = cv2.resize(frame_left, dim, interpolation=cv2.INTER_LINEAR)
    frame_right_resized = cv2.resize(frame_right, dim, interpolation=cv2.INTER_LINEAR)

    try:
        images = [frame_left_resized, frame_right_resized]
        stitcher = cv2.Stitcher.create()
        ret, stitched_image = stitcher.stitch(images)
    except Exception as e:
        print(f"error occurred in creating a stitcher: {e}")
        return

    if ret == cv2.Stitcher_OK:
        final_stitched_image = cv2.resize(stitched_image, (1024, 738), interpolation=cv2.INTER_LINEAR)
        return final_stitched_image
    else:
        print("ret value was not ok")
        return None


def display_video_stream(video_path, window_name):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_resized = cv2.resize(frame, (600, 600))
            cv2.imshow(window_name, frame_resized)

            if cv2.waitKey(50) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyWindow(window_name)


def stitch_and_display(video_left_path, video_right_path):
    cap_left = cv2.VideoCapture(video_left_path)
    cap_right = cv2.VideoCapture(video_right_path)

    fps_left = cap_left.get(cv2.CAP_PROP_FPS)
    fps_right = cap_right.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / max(fps_left, fps_right))  # Frame delay in milliseconds

    if not cap_left.isOpened() or not cap_right.isOpened():
        print("Error opening video files")
        return

    frame_skip = 2  # Skip every 2 frames
    frame_count = 0

    while cap_left.isOpened() and cap_right.isOpened():
        start_time = time.time()
        ret_left, frame_left = cap_left.read()
        ret_right, frame_right = cap_right.read()

        if frame_count % frame_skip == 0:
            if ret_left and ret_right:
                stitched_frame = stitch_frames(frame_left, frame_right)
                if stitched_frame is not None:
                    cv2.imshow('Stitched Frame', stitched_frame)
                    # Calculate processing time and adjust waitKey delay accordingly
                    elapsed_time = (time.time() - start_time) * 1000
                    wait_time = max(1, frame_delay - int(elapsed_time))
                    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                        break
        frame_count += 1

    cap_left.release()
    cap_right.release()
    cv2.destroyWindow('Stitched Frame')


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
    while True:
        left_video_path = Select_video_path()
        if left_video_path is not None:
            try:
                fixed_left_path = fix_video_path(left_video_path)
                print(f"left path after pathlib is {fixed_left_path}")
                break
            except Exception as e:
                print(f"error occurred during fixing path{e}")
        else:
            print("repeat reading left video path")

    while True:
        right_video_path = Select_video_path()
        if right_video_path is not None:
            try:
                fixed_right_path = fix_video_path(right_video_path)
                print(f"right path after pathlib is {fixed_right_path}")
                break
            except Exception as e:
                print(f"error occurred during fixing path{e}")
        else:
            print("repeat reading right video path")

    # Start threads for displaying individual video streams
    thread_left = threading.Thread(target=display_video_stream, args=(fixed_left_path, 'Left Frame'))
    thread_right = threading.Thread(target=display_video_stream, args=(fixed_right_path, 'Right Frame'))
    thread_stitch = threading.Thread(target=stitch_and_display, args=(fixed_left_path, fixed_right_path))

    thread_left.start()
    thread_right.start()
    thread_stitch.start()

    # Wait for all threads to finish
    thread_left.join()
    thread_right.join()
    thread_stitch.join()
