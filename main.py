import cv2
import numpy as np
import sys

# user options, see README.md for details on how to use
toppercent = 0.3
bottompercent = 0.7
PERCENT_BLUE_FOR_PAUSED = 70
video_name = "video.mp4"
output_name = "output.mp4" # must end in mp4 unless you know how to change the fourcc code appropriately on line 27
FRAME_SKIP_AFTER_PAUSE = 7


# progress bar for command line
def progress(purpose, currentcount, maxcount, skipped):
    sys.stdout.write('\r')
    sys.stdout.write("{}: {} of {} ({:.1f}%), {} paused frames skipped ".format(purpose,currentcount, maxcount, (100/(maxcount-1)*currentcount), skipped))
    sys.stdout.flush()

def main(toppercent, bottompercent, PERCENT_BLUE_FOR_PAUSED, video_name, output_name, FRAME_SKIP_AFTER_PAUSE):
    # get input video data and set up variables for output video
    cap = cv2.VideoCapture(video_name)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    insize = (int (cap.get(cv2.CAP_PROP_FRAME_WIDTH)) ,int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    topheight = int(toppercent * insize[1])
    bottomheight = int(bottompercent * insize[1])
    out = cv2.VideoWriter('output'+str(FRAME_SKIP_AFTER_PAUSE)+'.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, insize)

    counter = 0
    skippedcounter = 0
    afterskip = 0
    while cap.isOpened():
        progress("Scanning frames", counter, frame_count, skippedcounter)
        counter += 1
        ret, frame = cap.read()
        if frame is None:
            break

        # resize by 0.5 to speed up processing dramatically, make a copy so the original can be added to output
        rewidth = frame.shape[0]//2
        reheight = frame.shape[1]//2
        pixels = rewidth*reheight
        framec = frame.copy()[topheight:bottomheight, :]
        framec = cv2.resize(framec, (rewidth, reheight))
        bw = cv2.cvtColor(framec, cv2.COLOR_BGR2GRAY)
        # looking for blue from pause menu. Essentially masks everything except blue, thresholds so blue becomes white, counts white pixels
        lower_blue = np.array([110, 100, 100])
        upper_blue = np.array([130, 255, 255])
        hsv = cv2.cvtColor(framec, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        result = cv2.bitwise_and(framec, framec, mask=mask)
        gray_img = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
        white = [255, 255, 255]
        count = np.count_nonzero(thresh)
        percentblue = round(count/(rewidth*reheight)*100, 2)
        # some debugging you can uncomment for tweaking if you know what you're doing
        # print(f'Blue pixels: {count}/{pixels}, {percentblue}%')
        # output = np.hstack([thresh, bw])
        # cv2.namedWindow('a', cv2.WINDOW_NORMAL)
        # cv2.imshow("a", output)
        # cv2.resizeWindow("a", rewidth//2, reheight[1]//2)
        # cv2.waitKey(0)

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
    main(toppercent ,bottompercent, PERCENT_BLUE_FOR_PAUSED, video_name, output_name, FRAME_SKIP_AFTER_PAUSE)
