import cv2
from tkinter import *
from threading import Thread
from PIL import ImageTk, Image
from abc import ABC, abstractmethod
import numpy as np


# TODO: Implement inheritance structure and basic initialization code for detections
class Detection(ABC):
    @abstractmethod
    def _detect(self) -> None:
        """ Begin image processing and detection

        Use opencv and/or mediapipe pre-made solutions to run real-time
        detection algorithms based on which kind of detections the user
        specifies.

        Will then convert the final img ndarrays into PhotoImage objects
        to post to the GUI
        """

    @abstractmethod
    def _to_photo_image(self, rgb_array: np.ndarray) -> PhotoImage:
        """ Converts image with drawn-on detections to usable PhotoImage object

        Takes in 3D np ndarray of RGB values and performs necessary
        color shift, mirroring, and PhotoImage conversion operations
        to ready the image for passing to the GUI
        """

    @abstractmethod
    def _update_frame(self, final_img: PhotoImage) -> None:
        """ Update the image label to simulate live video

        Difficult part of this task is updating the video frame label
        in a way that is compatible with the thread of the GUI and the
        thread of the detections
        """


class FaceDetection(Detection):
    FACE_CASCADE = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

    def __init__(self, video_frame: Label) -> None:
        self._detection_thread = Thread(target=self._detect)
        self._video_frame = video_frame
        self._detection_thread.start()

    def _detect(self) -> None:
        pass

    def _to_photo_image(self, rgb_array: np.ndarray) -> PhotoImage:
        pass

    def _update_frame(self, final_img: PhotoImage) -> None:
        pass


class HandDetection(Detection):
    def __init__(self, video_frame: Label) -> None:
        self._detection_thread = Thread(target=self._detect)
        self._video_frame = video_frame
        self._detection_thread.start()

    def _detect(self) -> None:
        pass

    def _to_photo_image(self, rgb_array: np.ndarray) -> PhotoImage:
        pass

    def _update_frame(self, final_img: PhotoImage) -> None:
        pass
