from tkinter import *

from PIL import ImageTk, Image


class MainGUI:
    """
    MainGUI class initializes the tkinter GUI window and handles event listening
    """
    # init dimension consts
    IMAGE_WIDTH = 150
    IMAGE_HEIGHT = 200

    # reference colors dict
    colors = {
        'window_bg': '#3C3C3C',
        'button_bg': '#676767',
        'button_fg': '#FFFFFF',
        'label_bg': '#3C3C3C',
        'label_fg': '#FFFFFF',
        'image_bg': '#000000'
    }

    def __init__(self):
        """ Initializes Tkinter window and starts mainloop() """
        # init window
        self._window = Tk()

        self._images = {
            'face_image': ImageTk.PhotoImage(
                Image.open('./images/face.gif').resize((MainGUI.IMAGE_WIDTH, MainGUI.IMAGE_HEIGHT),
                                                       Image.ANTIALIAS)),
            'hand_image': ImageTk.PhotoImage(
                Image.open('./images/hand.gif').resize((MainGUI.IMAGE_WIDTH, MainGUI.IMAGE_HEIGHT),
                                                       Image.ANTIALIAS))
        }

        # init widgets
        self._buttons = {
            'face_button': Button(self._window, bg=MainGUI.colors['button_bg'], command=self.__face_click,
                                  fg=MainGUI.colors['button_fg'], text='Facial Recognition', width=0),
            'hand_button': Button(self._window, bg=MainGUI.colors['button_bg'], command=self.__hand_click,
                                  fg=MainGUI.colors['button_fg'], text='Hand Recognition', width=0)
        }
        self._labels = {
            'title_label': Label(self._window, bg=MainGUI.colors['label_bg'], fg=MainGUI.colors['label_fg'],
                                 text='Welcome to the Recognition Suite!', font="none 12 bold"),
            'face_image_label': Label(self._window, image=self._images['face_image'], height=0, width=0, borderwidth=2,
                                      bg=MainGUI.colors['image_bg']),
            'hand_image_label': Label(self._window, image=self._images['hand_image'], height=0, width=0, borderwidth=2,
                                      bg=MainGUI.colors['image_bg'])
        }

        # additional window configuration and widget placement
        self._window.title("Recognition Suite")
        self._window.configure(bg=MainGUI.colors['window_bg'], height=0, width=0)
        self.__place_elements()

        # start the mainloop() to open the GUI and begin event listening
        self._window.mainloop()

    def __place_elements(self):
        # title
        self._labels['title_label'].grid(row=0, column=0, sticky=W)
        # face image and button
        self._labels['face_image_label'].grid(row=1, column=0, pady=(10, 20), sticky=W)
        self._buttons['face_button'].grid(row=2, column=0, sticky=W)
        # hand image and button
        self._labels['hand_image_label'].grid(row=1, column=1, pady=(10, 20), sticky=W)
        self._buttons['hand_button'].grid(row=2, column=1, sticky=W)

    def __face_click(self):
        pass

    def __hand_click(self):
        pass
