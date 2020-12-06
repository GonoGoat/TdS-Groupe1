# Program To Read video
# and Extract Frames
import numpy
import cv2
from tkinter import filedialog

# Function to extract frames
def FrameCapture():
    # Path to video file
    file = filedialog.askopenfilename(initialdir="C:",
                                      title="Choisissez un fichier vidéo",
                                      filetypes=(("mp4 files", "*.mp4"), ("avi files", "*.avi"), ("mov files", "*.mov"), ("mkv files", "*.mkv"), ("all files", "*")));

    vidObj = cv2.VideoCapture(file)

    # vidObj object calls read
    # function extract frames
    success, image = vidObj.read()

    # Saves the frames with frame-count
    cv2.imwrite("image\\frame_%d.jpg" % 0, image)
    return file