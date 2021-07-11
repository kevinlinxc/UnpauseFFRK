import main
import streamlit as st
import tempfile
import os
import cv2

st.write("# Welcome to UnpauseFFRK!")
st.write("### This site is a frontend for the Python script that I've written on my [Github](https://github.com/kevinlinxc/UnpauseFFRK).")
st.write('### You can use this site to remove paused frames from Final Fantasy Record Keeper gameplay videos, but be aware of the limitations '
         'mentioned on Github.')


uploaded_file = st.file_uploader("Choose a file", type=['mp4', 'avi'])
stframe = st.empty()



if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    output_name = os.path.join(tempfile.gettempdir(), "output.mp4")
    st.write("### Options (defaults work well for a recording of just the screen)")
    col1, col2 = st.beta_columns(2)

    top_percent = col1.slider("% of screen to cut from top while processing", 0, 49, 30, 1, help="Cutting parts of the screen that don't show the pause menu decreases processing time. This won't crop the output video.")
    bottom_percent = col2.slider("% of screen to cut from bottom while processing", 0, 49, 30, 1, help="Cutting parts of the screen that won't have the pause menu decreases processing time. This won't crop the output video.")
    frames_skip = col1.slider("Number of frames to skip after unpausing", 0, 20, 7, 1, help="The game is frozen for a few frames after unpausing. Removing some of these frames amkes the game output seem less stuttery.")
    percentage = col2.slider("% of screen that has to be blue for a frame to be considered paused", 0 , 100, 70, 1, help="If this was 0, all frames would be considered paused. Decrease if paused frames aren't being deleted. If you crop the top and bottom properly, the default should be fine. If your video is 1920x1080 with FFRK in the middle, lower this dramatically.")
    button = st.button("Start unpausing!")
    if button:
        unpauser = main.UnpauseFFRK(top_percent, bottom_percent, percentage, tfile.name, output_name, frames_skip, True)
        video_file = open(output_name, 'rb')
        video_bytes = video_file.read()
        st.sidebar.write("Completed! Right click the video below->Save Video As to download it, or upload a new video/refresh to restart.")
        st.sidebar.video(video_bytes)
