from tkinter import *

from PIL import ImageTk, Image

import detections


class MainGUI:
    """
    MainGUI class initializes the tkinter GUI window and handles event listening
    """
    # init dimension consts
    IMAGE_WIDTH = 150
    IMAGE_HEIGHT = 200

    # reference COLORS dict
    COLORS = {
        'window_bg': '#3C3C3C',
        'button_bg': '#676767',
        'button_fg': '#FFFFFF',
        'label_bg': '#3C3C3C',
        'label_fg': '#FFFFFF',
        'image_bg': '#000000'
    }

    def __init__(self) -> None:
        """ Initializes Tkinter window and starts mainloop() """
        # init window
        self._window: Tk = Tk()

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

        # init widgets
        self._buttons: dict = {
            'face_button': Button(self._window, bg=MainGUI.COLORS['button_bg'], command=self._face_click,
                                  fg=MainGUI.COLORS['button_fg'], text='Toggle Facial Recognition', width=0),
            'hand_button': Button(self._window, bg=MainGUI.COLORS['button_bg'], command=self._hand_click,
                                  fg=MainGUI.COLORS['button_fg'], text='Toggle Hand Recognition', width=0),
            'exit_button': Button(self._window, bg=MainGUI.COLORS['button_bg'], command=self._exit_click,
                                  fg=MainGUI.COLORS['button_fg'], text='Exit', width=15)
        }

        self._labels: dict = {
            'title_label': Label(self._window, bg=MainGUI.COLORS['label_bg'], fg=MainGUI.COLORS['label_fg'],
                                 text='Welcome to the Recognition Suite!', font="none 12 bold"),
            'face_image_label': Label(self._window, image=self._images['face_image'], height=0, width=0, borderwidth=2,
                                      bg=MainGUI.COLORS['image_bg']),
            'hand_image_label': Label(self._window, image=self._images['hand_image'], height=0, width=0, borderwidth=2,
                                      bg=MainGUI.COLORS['image_bg']),
            'video_frame_label': Label(self._window, image=self._images['video_frame_default_image'],
                                       bg=MainGUI.COLORS['image_bg'], height=520, width=920, borderwidth=2)
        }

        # additional window configuration and widget placement
        self._window.title("Recognition Suite")
        self._window.configure(bg=MainGUI.COLORS['window_bg'], height=0, width=0)
        self._place_elements()

        # start the mainloop() to open the GUI and begin event listening
        self._window.mainloop()

    def _place_elements(self) -> None:
        # ROW 0
        self._labels['title_label'].grid(row=0, column=0, sticky=W)  # title label
        # ROW 1
        self._labels['face_image_label'].grid(row=1, column=0, pady=(10, 10), sticky=W)  # face image
        self._labels['hand_image_label'].grid(row=1, column=0, pady=(10, 10), sticky=N)  # hand image
        # ROW 2
        self._buttons['face_button'].grid(row=2, column=0, pady=(0, 20), sticky=W)  # face detection button
        self._buttons['hand_button'].grid(row=2, column=0, pady=(0, 20), sticky=N)  # hand detection button
        # ROW 3
        self._labels['video_frame_label'].grid(row=3, column=0, padx=(50, 50), pady=(50, 50), sticky=N)  # video frame
        # ROW 4
        self._buttons['exit_button'].grid(row=4, column=0, padx=(50, 0), sticky=W)  # exit button

    def _face_click(self) -> None:
        face_detection = detections.FaceDetection(video_frame=self._labels['video_frame_label'])

    def _hand_click(self) -> None:
        pass

    def _exit_click(self) -> None:
        """ Safely stop execution of program """
        pass
