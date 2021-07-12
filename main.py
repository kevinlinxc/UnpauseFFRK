import cv2
import numpy as np
import sys
import streamlit as st
import time

# user options, see README.md for details on how to use
TOP_PERCENT = 30
BOTTOM_PERCENT = 30
PERCENT_BLUE_FOR_PAUSED = 70
VIDEO_NAME = "video.mp4"
OUTPUT_NAME = "output.mp4" # must end in mp4 unless you know how to change the fourcc code appropriately on line 27
FRAME_SKIP_AFTER_PAUSE = 7

class UnpauseFFRK():


    # progress bar for command line
    def progress(self, purpose, currentcount, maxcount, skipped, website, bar, textprogress, start):
        end = time.time()
        message1 = "{}: {} of {} ({:.1f}%)".format(purpose,currentcount, maxcount, (100/(maxcount)*currentcount))
        message2 = "{} paused frames skipped".format(skipped)
        message3 = "{} seconds elapsed".format(round(end-start))
        message = message1 + ", " + message2 + ", " + message3
        if (website):
            bar.progress(currentcount/maxcount)
            textprogress.text(message)

        else:
            sys.stdout.write('\r')
            sys.stdout.write(message)
            sys.stdout.flush()

    def __init__(self, toppercent, bottompercent, PERCENT_BLUE_FOR_PAUSED, video_name, output_name, FRAME_SKIP_AFTER_PAUSE, website=False):
        # get input video data and set up variables for output video
        cap = cv2.VideoCapture(video_name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        insize = (int (cap.get(cv2.CAP_PROP_FRAME_WIDTH)) ,int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        topheight = int(toppercent/100 * insize[1])
        bottomheight = int((100-bottompercent)/100 * insize[1])
        out = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'avc1'), fps, insize) #mp4v

        counter = 0
        skippedcounter = 0
        afterskip = 0
        bar = ''
        textprogress = ''
        start = time.time()
        if website:
            st.write(f"Processing...this usually takes around the video duration length to complete.")
            textprogress = st.empty()
            bar = st.progress(0)
        while cap.isOpened():
            self.progress("Scanning frames", counter, frame_count, skippedcounter, website, bar, textprogress, start)
            counter += 1
            ret, frame = cap.read()
            if frame is None:
                break

            # resize by <1 to speed up processing dramatically, make a copy so the original can be added to output
            rewidth = frame.shape[0]//5
            reheight = frame.shape[1]//5
            framec = frame.copy()[topheight:bottomheight, :]
            framec = cv2.resize(framec, (rewidth, reheight))
            # looking for blue from pause menu. Essentially masks everything except blue, thresholds so blue becomes white, counts white pixels
            lower_blue = np.array([110, 100, 100])
            upper_blue = np.array([130, 255, 255])
            hsv = cv2.cvtColor(framec, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            result = cv2.bitwise_and(framec, framec, mask=mask)
            gray_img = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
            count = np.count_nonzero(thresh)
            percentblue = round(count/(rewidth*reheight)*100, 2)

            if percentblue > PERCENT_BLUE_FOR_PAUSED:
                skippedcounter += 1
                afterskip = FRAME_SKIP_AFTER_PAUSE
                continue
            elif afterskip > 0:
                afterskip -= 1
            else:
                out.write(frame)

        cap.release()
        out.release()

# good practice for Python
if __name__ == "__main__":
    UnpauseFFRK(TOP_PERCENT, BOTTOM_PERCENT, PERCENT_BLUE_FOR_PAUSED, VIDEO_NAME, OUTPUT_NAME, FRAME_SKIP_AFTER_PAUSE)
