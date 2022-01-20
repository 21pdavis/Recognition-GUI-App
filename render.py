import tkinter
import tkinter as tk
from tkinter import messagebox
from time import sleep

from PIL import ImageTk, Image
import detections
import cv2


# TODO: add scrollbar
class MainGUI(tk.Frame):
    """
    MainGUI class initializes the tkinter GUI window and handles event listening
    """
    # init dimension consts
    IMAGE_WIDTH = 100
    IMAGE_HEIGHT = 133

    # reference COLORS dict
    COLORS = {
        'window_bg': '#3C3C3C',
        'button_bg': '#676767',
        'button_fg': '#FFFFFF',
        'label_bg': '#3C3C3C',
        'label_fg': '#FFFFFF',
        'image_bg': '#000000'
    }

    def __init__(self, parent_root: tk.Tk) -> None:
        """ Initializes Tkinter window and starts mainloop() """
        # call superclass, tk.Frame, __init__
        super().__init__(master=parent_root)

        # init PIL PhotoImage objects (to be displayed in labels)
        self._images: dict = {
            'face_image': ImageTk.PhotoImage(Image.open('./images/face.gif').resize((MainGUI.IMAGE_WIDTH,
                                                                                     MainGUI.IMAGE_HEIGHT),
                                                                                    Image.ANTIALIAS)),
            'hand_image': ImageTk.PhotoImage(Image.open('./images/hand.gif').resize((MainGUI.IMAGE_WIDTH,
                                                                                     MainGUI.IMAGE_HEIGHT),
                                                                                    Image.ANTIALIAS)),
            # size of video_frame_default_image = 920x520 pixels
            'video_frame_default_image': ImageTk.PhotoImage(Image.open('./images/video_frame_default.gif'))
        }

        # init labels
        self._labels: dict = {
            'title_label': tk.Label(self, bg=MainGUI.COLORS['label_bg'], fg=MainGUI.COLORS['label_fg'],
                                    text='Welcome to the Recognition Suite!', font='none 20 bold'),
            'face_image_label': tk.Label(self, image=self._images['face_image'], height=0, width=0,
                                         borderwidth=2, bg=MainGUI.COLORS['image_bg']),
            'hand_image_label': tk.Label(self, image=self._images['hand_image'], height=0, width=0,
                                         borderwidth=2, bg=MainGUI.COLORS['image_bg']),
            'video_frame_label': tk.Label(self, image=self._images['video_frame_default_image'],
                                          bg=MainGUI.COLORS['image_bg'], height=576, width=1024, borderwidth=2),
        }

        # detection objects for later use
        self._detections = {
            'face_detection': detections.FaceDetection(video_frame=self._labels['video_frame_label']),
            'hand_detection': detections.HandDetection(video_frame=self._labels['video_frame_label'])
        }

        # init buttons
        self._buttons: dict = {
            'face_button': tk.Button(self, bg=MainGUI.COLORS['button_bg'], command=lambda: self._detection_click(self._detections['face_detection']),
                                     fg=MainGUI.COLORS['button_fg'], text='Toggle Facial Recognition', width=0),
            'hand_button': tk.Button(self, bg=MainGUI.COLORS['button_bg'], command=lambda: self._detection_click(self._detections['hand_detection']),
                                     fg=MainGUI.COLORS['button_fg'], text='Toggle Hand Recognition', width=0),
            'exit_button': tk.Button(self, bg=MainGUI.COLORS['button_bg'], command=self._exit_click,
                                     fg=MainGUI.COLORS['button_fg'], text='Exit', width=15)
        }


        # additional window configuration and widget placement
        parent_root.title("Recognition Suite")
        self.configure(bg=MainGUI.COLORS['window_bg'], height=0, width=0)
        self._place_elements()

    def _place_elements(self) -> None:
        # ROW 0
        self._labels['title_label'].grid(row=0, column=0, padx=(25, 0), sticky=tk.W)  # title label
        # ROW 1
        self._labels['face_image_label'].grid(row=1, column=0, padx=(25, 0), sticky=tk.W)  # face img
        self._labels['hand_image_label'].grid(row=1, column=0, padx=(0, 25), sticky=tk.E)  # hand img
        # ROW 2
        self._buttons['face_button'].grid(row=2, column=0, padx=(25, 0), sticky=tk.W)  # face detection bt
        self._buttons['hand_button'].grid(row=2, column=0, padx=(0, 25), sticky=tk.E)  # hand detection bt
        # ROW 3
        self._labels['video_frame_label'].grid(row=3, column=0, padx=(25, 25), pady=(10, 0), sticky=tk.N)  # video frame
        # ROW 4
        self._buttons['exit_button'].grid(row=4, column=0, padx=(25, 0), pady=(15, 10), sticky=tk.NW)  # exit bt

    def _detection_click(self, detection: detections.Detection):
        for detection_type in self._detections:
            if self._detections[detection_type] == detection:
                continue
            self._detections[detection_type].detections_running = False
            self._labels['video_frame_label'].configure(image=self._images['video_frame_default_image'])

        if detection.detections_running:
            detection.detections_running = False
            self._labels['video_frame_label'].configure(image=self._images['video_frame_default_image'])
        else:
            detection.detections_running = True
            detection.begin_detection()

    def _exit_click(self) -> None:
        """ Safely stop execution of program """
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    # root window's height x width are set to 0x0 by default, but just explicitly declaring it here for debugging
    root.configure(width=0, height=0)
    MainGUI(root).grid(row=0, column=0, sticky=tk.NW)
    root.mainloop()
