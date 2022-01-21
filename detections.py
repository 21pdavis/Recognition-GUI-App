import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageOps, ImageTk


class Detection(ABC):
    @abstractmethod
    def __init__(self, video_frame: tk.Label) -> None:
        self._detections_running: bool = False
        self._video_frame: tk.Label = video_frame
        self._current_frame: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open('./images/video_frame_default.gif'))
        self._webcam_feed = None

    @property
    def detections_running(self) -> bool:
        """ Getter for the bool flag used to start and stop detections """
        return self._detections_running

    @detections_running.setter
    def detections_running(self, detections_running: bool) -> None:
        """ Setter for the bool flag used to start and stop detections """
        self._detections_running = detections_running

    def begin_detection(self, webcam_feed: cv2.VideoCapture = None) -> None:
        """ public function for starting detection """
        if webcam_feed:
            self._webcam_feed = webcam_feed
            self._video_frame.after(1, self._detect, webcam_feed)
        else:
            self._webcam_feed = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self._video_frame.after(1, self._detect, self._webcam_feed)

    def switch_detection(self, detection):
        self._detections_running = False
        detection.begin_detection(self._webcam_feed)

    def _detect(self, webcam_feed: cv2.VideoCapture) -> None:
        """ Begin image processing and detection

        Use opencv and/or mediapipe pre-made solutions to run real-time
        detection algorithms based on which kind of detections the user
        specifies.

        Will then convert the final img NumPy arrays into PhotoImage
        objects to post to the GUI
        """
        if self.detections_running:
            img_array_with_detections: np.ndarray = self._analyze_image(webcam_feed)
            if img_array_with_detections is not None:
                self._current_frame: ImageTk.PhotoImage = Detection._to_photo_image(img_array_with_detections)
                self._update_frame()
                # recursively call _detect() method to perform detections on next frame
                self._video_frame.after(1, self._detect, webcam_feed)

    def _update_frame(self) -> None:
        """ Update the image label with the current frame with detections drawn on """
        self._video_frame.configure(image=self._current_frame)

    @abstractmethod
    def _analyze_image(self, webcam_feed: cv2.VideoCapture) -> np.ndarray:
        """ Reads and performs detections on the current video feed frame

        Implementation of this method will differ between different
        types of detections (e.g., face vs. hand detection).

        Returns the img object NumPy array with detections drawn on
        """

    @staticmethod
    def _to_photo_image(img_array: np.ndarray) -> tk.PhotoImage:
        # color-shift image to standard RGB colorspace
        shifted_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        # translate image from ndarray -> PIL Image object
        pil_image = Image.fromarray(shifted_img, mode="RGB")

        # mirror image for user convenience then resize to fit video frame
        mirrored_img = ImageOps.mirror(image=pil_image).resize((1024, 576), Image.ANTIALIAS)

        # convert mirrored_img to ImageTk.PhotoImage object
        final_img = ImageTk.PhotoImage(image=mirrored_img)

        return final_img


class FaceDetection(Detection):
    FACE_CASCADE = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

    def __init__(self, video_frame: tk.Label) -> None:
        super().__init__(video_frame)

    def _analyze_image(self, webcam_feed: cv2.VideoCapture) -> np.ndarray:
        try:
            # read() returns a tuple of a read success flag and a 3D ndarray
            flag, img = webcam_feed.read()

            # shift color for detection
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Detection step: find faces in the image using haar cascade .xml file and detectMultiScale() function
            faces = FaceDetection.FACE_CASCADE.detectMultiScale(image=img_rgb, scaleFactor=1.1, minNeighbors=6)

            # draw rectangle around detected face(s)
            for (x, y, w, h) in faces:
                cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2, lineType=cv2.FILLED)

            return img
        except cv2.error:
            messagebox.showinfo(title='No Camera', message='No compatible camera is plugged in')
            self._detections_running = False


class HandDetection(Detection):
    # Initialize class-level Hands object used for hand identification
    HANDS_OBJ = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )  # default initialization values

    # Initialize class-level version of HAND_CONNECTIONS set constant used during detection
    HANDS_CONNECTIONS = mp.solutions.hands.HAND_CONNECTIONS

    # Initialize class-level reference to module containing mediapipe drawing tools
    MP_DRAW_MODULE = mp.solutions.drawing_utils

    def __init__(self, video_frame: tk.Label) -> None:
        super().__init__(video_frame)

    def _analyze_image(self, webcam_feed: cv2.VideoCapture) -> np.ndarray:
        try:
            # read() returns a tuple of a read success flag and a 3D ndarray
            flag, img = webcam_feed.read()

            # shift color for detection
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Detection step: use mediapipe library to identify hands in the image
            results = HandDetection.HANDS_OBJ.process(img_rgb)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(img=img, center=(cx, cy), radius=6, color=(255, 255, 255),
                                   lineType=cv2.FILLED)  # draw landmark circles

                    HandDetection.MP_DRAW_MODULE.draw_landmarks(img, handLms, HandDetection.HANDS_CONNECTIONS)

            return img
        except cv2.error:
            messagebox.showinfo(title='No Camera', message='No compatible camera is plugged in')
            self._detections_running = False
