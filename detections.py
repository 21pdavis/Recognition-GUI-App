import tkinter as tk
from abc import ABC, abstractmethod
from threading import Thread

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageTk


class Detection(ABC):
    @property
    @abstractmethod
    def run_detections(self) -> bool:
        """ Getter for the bool flag used to start and stop detections """

    @run_detections.setter
    @abstractmethod
    def run_detections(self, run_detections: bool) -> None:
        """ Setter for the bool flag used to start and stop detections """

    @abstractmethod
    def _detect(self, webcam_feed: cv2.VideoCapture) -> None:
        """ Begin image processing and detection

        Use opencv and/or mediapipe pre-made solutions to run real-time
        detection algorithms based on which kind of detections the user
        specifies.

        Will then convert the final img NumPy arrays into PhotoImage
        objects to post to the GUI
        """

    @abstractmethod
    def _analyze_image(self, webcam_feed: cv2.VideoCapture) -> np.ndarray:
        """ Reads and performs detections on the current video feed frame

        Implementation of this method will differ between different
        types of detections (e.g., face vs. hand detection).

        Returns the img object NumPy array with detections drawn on
        """

    @abstractmethod
    def _to_photo_image(self, img_array: np.ndarray) -> tk.PhotoImage:
        """ Converts image with drawn-on detections to usable PhotoImage object

        Takes in 3D np ndarray of RGB values and performs necessary
        color shift, mirroring, and PhotoImage conversion operations
        to ready the image for passing to the GUI
        """

    @abstractmethod
    def _update_frame(self) -> None:
        """ Update the image label with the current frame with detections drawn on """


class FaceDetection(Detection):
    FACE_CASCADE = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

    def __init__(self, video_frame: tk.Label) -> None:
        self._run_detections: bool = True
        self._video_frame: tk.Label = video_frame
        self._current_frame: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open('./images/video_frame_default.gif'))
        self._video_frame.after(0, self._detect, cv2.VideoCapture(0, cv2.CAP_DSHOW))

    @property
    def run_detections(self) -> bool:
        return self._run_detections

    @run_detections.setter
    def run_detections(self, run_detections: bool) -> None:
        self._run_detections = run_detections

    def _detect(self, webcam_feed: cv2.VideoCapture) -> None:
        if self._run_detections:
            img_array_with_detections: np.ndarray = self._analyze_image(webcam_feed)
            self._current_frame: ImageTk.PhotoImage = self._to_photo_image(img_array_with_detections)
            self._update_frame()

        # recursively call _detect() method to perform detections on next frame
        self._video_frame.after(1, self._detect, webcam_feed)

    def _analyze_image(self, webcam_feed: cv2.VideoCapture) -> np.ndarray:
        # read() returns a tuple of a read success flag and a 3D ndarray
        flag, img = webcam_feed.read()

        # shift color for proper multi-scale detection
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # find faces in the image using haar cascade .xml file and detectMultiScale() function
        faces = FaceDetection.FACE_CASCADE.detectMultiScale(image=img_rgb, scaleFactor=1.1, minNeighbors=8)

        # draw rectangle around detected face(s)
        for (x, y, w, h) in faces:
            cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2, lineType=cv2.FILLED)

        return img

    def _to_photo_image(self, img_array: np.ndarray) -> tk.PhotoImage:
        # color-shift image to standard RGB colorspace
        shifted_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        # mirror image for user convenience then
        mirrored_img = ImageOps.mirror(image=Image.fromarray(shifted_img, mode="RGB")).resize((920, 520),
                                                                                              Image.ANTIALIAS)

        # convert mirrored_img to ImageTk.PhotoImage object
        final_img = ImageTk.PhotoImage(image=mirrored_img)

        return final_img

    # def _update_frame(self, final_img: tk.PhotoImage) -> None:
    def _update_frame(self):
        self._video_frame.configure(image=self._current_frame)


class HandDetection(Detection):
    def __init__(self, video_frame: tk.Label) -> None:
        self._run_detections = False

        self._detection_thread = Thread(target=self._detect)
        self._video_frame = video_frame
        self._detection_thread.start()

    @property
    def run_detections(self) -> bool:
        return self._run_detections

    @run_detections.setter
    def run_detections(self, run_detections: bool) -> None:
        self._run_detections = run_detections

    def _detect(self, webcam_feed: cv2.VideoCapture) -> None:
        pass

    def _analyze_image(self, webcam_feed: cv2.VideoCapture) -> np.ndarray:
        pass

    def _to_photo_image(self, img_array: np.ndarray) -> tk.PhotoImage:
        pass

    def _update_frame(self) -> None:
        pass
