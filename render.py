from tkinter import *


class TkinterGUI:
    """
    TkinterGUI class initializes the tkinter GUI window and handles event listening
    """

    def __init__(self):
        """ Initializes Tkinter window and starts mainloop() """
        # init window
        self._window = Tk()
        self._window.title("Recognition Suite")
        self._window.configure(background=self._colors['window_bg'], height=400, width=600)

        # init reference values & images
        self._colors = {
            'window_bg': '#3C3C3C',
            'button_bg': '#3C3C3C',
            'button_fg': '#FFFFFF',
            'label_bg': '#3C3C3C',
            'label_fg': '#FFFFFF'
        }
        self.images = {
            'face_image': Image(master=self._window),
            'hand_image': Image(master=self._window)
        }

        # init widgets
        self._buttons = {
            'face_button': Button(self._window, background=self._colors['button_bg'], command=self.__face_click,
                                  foreground=self._colors['button_fg'], text='Facial Recognition', width=0),
            'hand_button': Button(self._window, background=self._colors['button_bg'], command=self.__hand_click,
                                  foreground=self._colors['button_fg'], text='Hand Recognition', width=0)
        }
        self.labels = {
            'title_label': Label(self._window, background=self._colors['label_bg'], foreground=self._colors['label_fg'],
                                 text='Welcome to the Recognition Suite!', font="none 12 bold")
        }

        # place the generated elements in the grid
        self.__place_elements()

        # start the mainloop() to open the GUI and begin event listening
        self._window.mainloop()

    def __place_elements(self):
        self.labels['title_label'].grid(row=0, column=0, sticky=W)
        self._buttons['face_button'].grid(row=2, column=0, sticky=W)

    def __face_click(self):
        pass

    def __hand_click(self):
        pass
