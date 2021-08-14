import cv2
import numpy as np
import sys
import streamlit as st
import time
import av

# user options, see README.md for details on how to use
TOP_PERCENT = 30
BOTTOM_PERCENT = 30
PERCENT_BLUE_FOR_PAUSED = 70
VIDEO_NAME = "video.mp4"
OUTPUT_NAME = "output.mp4"  # must end in mp4 unless you know how to change the fourcc code appropriately on line 27
FRAME_SKIP_AFTER_PAUSE = 7


class UnpauseFFRK:

    # progress bar for command line
    def progress(self, purpose, current_count, max_count, skipped, website, bar, text_progress, start):
        end = time.time()
        message1 = "{}: {} of {} ({:.1f}%)".format(purpose, current_count, max_count, (100 / max_count * current_count))
        message2 = "{} paused frames skipped".format(skipped)
        message3 = "{} seconds elapsed".format(round(end-start))
        message = message1 + ", " + message2 + ", " + message3
        if website:
            bar.progress(current_count/max_count)
            text_progress.text(message)

        else:
            sys.stdout.write('\r')
            sys.stdout.write(message)
            sys.stdout.flush()

    def __init__(self, top_percent, bottom_percent, percent_blue_for_paused, video_name, output_name, frame_skip_after_pause, website=False):
        # get input video data and set up variables for output video
        cap = cv2.VideoCapture(video_name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        in_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        top_height = int(top_percent / 100 * in_size[1])
        bottom_height = int((100 - bottom_percent) / 100 * in_size[1])
        # opencv can't encode h.264 so use PyAV instead https://stackoverflow.com/questions/68779760
        output = av.open(output_name, 'w')
        stream = output.add_stream('h264', fps)
        stream.width = in_size[0]
        stream.height = in_size[1]

        counter = 0
        skipped_counter = 0
        after_skip = 0
        bar = ''
        text_progress = ''
        start = time.time()
        if website:
            st.write(f"Processing...this can take a while, go take a shower or try to use Kite's shop.")
            text_progress = st.empty()
            bar = st.progress(0)
        while cap.isOpened():
            self.progress("Scanning frames", counter, frame_count, skipped_counter, website, bar, text_progress, start)
            counter += 1
            ret, frame = cap.read()
            if frame is None:
                break

            # resize by <1 to speed up processing dramatically, make a copy so the original can be added to output
            re_width = frame.shape[0] // 5
            re_height = frame.shape[1] // 5
            frame_c = frame.copy()[top_height:bottom_height, :]
            frame_c = cv2.resize(frame_c, (re_width, re_height))
            # looking for blue from pause menu. masks everything except blue, thresholds so blue becomes white, counts white pixels
            lower_blue = np.array([110, 100, 100])
            upper_blue = np.array([130, 255, 255])
            hsv = cv2.cvtColor(frame_c, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            result = cv2.bitwise_and(frame_c, frame_c, mask=mask)
            gray_img = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
            count = np.count_nonzero(thresh)
            percent_blue = round(count / (re_width * re_height) * 100, 2)

            if percent_blue > percent_blue_for_paused:
                skipped_counter += 1
                after_skip = frame_skip_after_pause
                continue
            elif after_skip > 0:
                after_skip -= 1
            else:
                frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
                packet = stream.encode(frame)
                output.mux(packet)

        cap.release()
        for packet in stream.encode():
            output.mux(packet)
        output.close()


# This makes it so if you run python main.py, you can manually run the script
if __name__ == "__main__":
    UnpauseFFRK(TOP_PERCENT, BOTTOM_PERCENT, PERCENT_BLUE_FOR_PAUSED, VIDEO_NAME, OUTPUT_NAME, FRAME_SKIP_AFTER_PAUSE)
