# UnpauseFFRK
Recordings of battles in Final Fantasy Record Keeper (mobile game) tend have lots of pausing because the game requires quick reactions.
These pauses can be an annoyance when watching the recording, so I wrote a script to remove them from recordings using Python and OpenCV. 

Ideally, this would be a website where you could upload your file and process it and get it back, but I've had 
no luck getting the website I made hosted. You can read about my issues [here](https://discuss.streamlit.io/t/website-crashes-during-file-upload/16130/7) and [here](https://github.com/streamlit/streamlit/issues/3722).
I tried Google Cloud Run (file upload max of ~30mb), Streamlit Sharing (1 GB Ram only), Digital Ocean (my Dock was too big for the registry, didn't want to spend credits before even hosting the site), Heroku (Ram limit again).
Currently, you need to know how to use the most basic Python features like how to install Python, installing requirements,
and using terminal commands. If that's okay, read the limitations below to see if it's right for you, and then read the instructions if you're undeterred.

# Limitations:
TLDR: Input mp4 file of just FFRK filling the video, outputs .mp4 with no audio. Pause frames are removed and some frames after pauses too, to help with stuttering.
- Some animations in FFRK persist while the game is paused (e.g. Soul Breaks), so if you pause for long during those, there will be a noticeable jump.
- It's difficult to extract the audio of particular frames, so the output does not have audio. Leave a pull request if you have a way of doing this, maybe with FFMPEG, or just add your own audio after.
- This script removes frames where the percentage of blue pixels (pause menu) crosses a threshold, so it will work best if the recording is of just the FFRK screen. If it only fills x% of width, you'll want to reduce the blue slider to 0.70*x.
- The script removes the pause frames and then a certain number of frames after because the game lags a bit after unpausing, 
and this number of frames could depend on your app/simulator's performance.
- Only tested with mp4 as input, other inputs might work, especially avi. Only outputs to mp4, only tested on Windows but according to [this](https://gist.github.com/takuma7/44f9ecb028ff00e2132e) this should work on Mac too.

# Instructions for using the website
1. Download any version of Python 3. I used Python 3.9, [here](https://realpython.com/installing-python/)'s a decent guide for installing Python.
Note: I tried making an exe but it was messy and you shouldn't run .exe from strangers probably
You'll know you installed Python correctly when running `python --version` in a freshly opened terminal tells you the version. 
2. If you know how to use Git, clone this repo. Otherwise, you can go to the [main page](https://github.com/kevinlinxc/UnpauseFFRK) of this repo. click the green Code download button,
Download as a Zip archive and extract it to somewhere you'll remember.
3. Navigate to this repository in a command line/terminal. For example, if I've downloaded to my Desktop on Windows, the command prompt opens to `C:\Users\Kevin` and I can use the command
`cd Desktop\UnpauseFFRK` to navigate to this repository.
4. Installing Python should also install Pip, a package manager for Python. Download the packages you need for this project by running `pip install -r requirements.txt` in the same terminal as above
5. Run the command `streamlit run app.py` in the same terminal above. It should tell you something in the terminal, and then open the website in your browser at http://localhost:8080.
6. Upload your .mp4 or .avi video file, (might be a brief pause after uploading), and then hit `Start unpausing`. You can tweak some numbers here if your video isn't filling the screen. 
7. It'll take a while to scan the frames. Once it's done, it'll play the video in the sidebar, where you'll be able to right click it and download it. 
8. This has been tested on Windows, but not Mac.

# Instructions for using the script directly
The main script is located in main.py, the website at app.py just serves as a frontend. You can read through main.py to see what the script does.
This script works for me, but it could require tweaking for you to work. Here are all the options that you can conveniently change at the top of `main.py` with your favourite text editor.
## toppercent and bottompercent
What percentage of the screen is ignored while looking for pauses, I added these because the top and bottom of the screen are useless and needlessly increase processing time.
Default are `30` and `30`, meaning the top and bottom 30% of the video are ignored.
## PERCENT_BLUE_FOR_PAUSED 
What percentage of the screen should be blue for the screen to be considered paused, default `70`. Decreasing this value will help with recordings where the game doesn't fill the screen, since there will be lower percentage of the screen that is blue.
## video_name
The name of the input video, default `video.mp4`
## output_name
The name of the ouput video, default `output.mp4`. The output should remain .mp4 unless you know what you are doing.
## FRAME_SKIP_AFTER_PAUSE
The number of frames to skip after an unpause, to skip the intentional lag that unpausing creates. I manually figured out it was around 8-14 frames for me, so I set it to `7`.


# Future features 
I'm pretty busy but if enough people ask for these features I'll consider working on them. Even better, if you can code them and submit a PR I'll happily review and merge. 
- Cropping on the horizontal sides, for videos that need that
- An image viewer so you can choose the cropping percentages with the help of a visual
- Audio