# UnpauseFFRK
Recordings of battles in Final Fantasy Record Keeper (mobile game) tend have lots of pausing because the game requires quick reactions.
These pauses can be an annoyance when watching the recording, so I wrote a script to remove them from recordings using Python and OpenCV. 

Read the limitations below to see if it's right for you, and then read the instructions if you're undeterred. If you're familiar with Git and Python, you can download the code and play around with
`main.py` for customizability, but otherwise the website should be sufficient for you. 

# Limitations:
TLDR: Input mp4 file of just FFRK filling the video, outputs .mp4 with no audio. Pause frames are removed and some frames after pauses are also removed to help with stuttering.
- Some animations in FFRK persist while the game is paused (e.g. Soul Breaks), so if you pause for long during those, there will be a noticeable jump.
- It's difficult to extract the audio of particular frames, so the output does not have audio. Leave a pull request if you have a way of doing this, maybe with FFMPEG, or just add your own audio after.
- This script removes frames where the percentage of blue pixels (pause menu) crosses a threshold, so it will only work if the recording is of just the FFRK screen.
- The script removes the pause frames and then a certain number of frames after because the game lags a bit after unpausing, 
and this number of frames could depend on your app/simulator's performance.
- Only tested with mp4 as input, other inputs might work since I'm using OpenCV. Only outputs to mp4, only tested on Windows but according to [this](https://gist.github.com/takuma7/44f9ecb028ff00e2132e) this should work on Mac too.

# Instructions
1. Download any version of Python 3. I used Python 3.9, [here](https://realpython.com/installing-python/)'s a decent guide for installing Python.
Note: I hesitate to make a non-programmer friendly .exe because you generally shouldn't run executable files from strangers on the internet.
You'll know you installed Python correctly when running `python --version` in a terminal tells you the version. 
2. If you know how to use Git, clone this repo. Otherwise, you can go to the [main page](https://github.com/kevinlinxc/UnpauseFFRK) of this repo. click the green Code download button,
Download as a Zip archive and extract it to somewhere you'll remember.
3. Navigate to this repository in a command line/terminal. For example, if I've downloaded to my Desktop on Windows, the command prompt opens to `C:\Users\Kevin` and I can use the command
`cd Desktop\UnpauseFFRK` to navigate to this repository.
4. Installing Python should also install Pip, a package manager for Python. Download the packages you need for this project by running `pip install -r requirements.txt` in the same terminal as above
5. Move the video you want unpaused into the UnpauseFFRK folder, and rename it to video.mp4.
6. Run the command `python main.py` in the same terminal as above. The video will take a while to process and it'll tell you the progress. The video will be output to UnfreezeFFRK/output.mp4 by default.

# Extra options
This script works for me, but it could require tweaking for you to work. Here are all the options that you can conveniently change at the top of `main.py` with your favourite text editor.
## toppercent and bottompercent
What percentage of the screen is ignored while looking for pauses, I added these because the top and bottom of the screen are useless and needlessly increase processing time.
Default are `30` and `30`, meaning the top and bottom 30% of the video are ignored.
## PERCENT_BLUE_FOR_PAUSED 
What percentage of the screen should be blue for the screen to be considered paused, default `70`. It might help to decrease this value if the script is not working. 
## video_name
The name of the input video, default `video.mp4`
## output_name
The name of the ouput video, default `output.mp4`. The output should remain .mp4 unless you know what you are doing.
## FRAME_SKIP_AFTER_PAUSE
The number of frames to skip after an unpause, to skip the intentional lag that unpausing creates. I manually figured out it was around 8-14 frames for me, so I set it to `7`.


# Future features 
I'm pretty busy but if enough people ask for these features I'll consider working on them. Even better, if you can make them happen I'll happily review and merge. 
- Cropping on the horizontal sides, for videos that need that
- An image viewer so you can choose the cropping percentages with the help of a visual
- Audio