import time
import tkinter as tk

import cv2
from PIL import Image

from GUI.Label import Lab
from GUI.default_parameters import WIDTH, HEIGHT
from GUI.image import get_image

detector = cv2.CascadeClassifier('/home/saboni/rpi/models/haarcascade_frontalface_default.xml')
FACE_MIN_SIZE = 250


class GUI:
    def __init__(self, root):
        super().__init__()
        self.first_face_image = None
        self.face_images_list = list()
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor="none", bg="white")

        self.stop = False

        self.end_face_detection = False
        self.is_welcome_screen = False
        self.face_detect_time = None
        self.face_label = tk.Label(self.root, bg='white')

        # Face detection
        self.cap = None
        self.ret = None
        self.frame = None
        self.face_image = None
        self.face_photo = None
        self.face_detect_time = None
        self.end_face_detection = False
        self.face_images_list = list()
        self.first_face_image = None
        self.face_image_width = 1280
        self.face_image_height = 720
        self.face_searching_time = 300
        # Face detection

        self.place_labels_list = list()

    def create_text(self, text: str, x: int, y: int, size: int):
        label = Lab(self, x, y, None, text, size)
        label.show()

    def pl(self, label, x: int, y: int, save: bool = True) -> None:
        label.place(x=x, y=y)
        if save:
            self.place_labels_list.append(label)

    def remove_all(self):
        for i in self.place_labels_list:
            i.place_forget()
        self.place_labels_list = list()

    def start(self):
        self.show_face()

    def show_face(self) -> None:
        try:
            self.face_images_list = list()
            self.first_face_image = None
            self.end_face_detection = False
            self.is_welcome_screen = False
            self.face_detect_time = None

            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.face_image_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.face_image_height)

            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.face_image = Image.fromarray(frame)
            self.face_photo = get_image(self.face_image)

            self.remove_all()
            image_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            image_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            x = int((WIDTH - image_width) / 2)
            y = int((HEIGHT - image_height) / 2)

            self.pl(self.face_label, x, y)
            self.face_label.configure(image=self.face_photo)

            recognition_end_time = time.time() + self.face_searching_time

            self.root.after(0, self.update_face_frame, False, recognition_end_time)
        except Exception as e:
            self.close_camera()
            self.stop = True
            pass

    def update_face_frame(self, end_face_detection=False, recognition_end_time=time.time()) -> None:
        if self.stop:
            return
        try:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                rects = detector.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(FACE_MIN_SIZE, FACE_MIN_SIZE),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                for (x, y, w, h) in rects:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if rects != tuple():
                    end_face_detection = True
                    image = cv2.resize(
                        frame,
                        (self.face_image_width, self.face_image_height),
                        interpolation=cv2.INTER_AREA)

                    _, buffer = cv2.imencode('.jpeg', image)

                    self.face_images_list.append(buffer)

                    if self.face_detect_time is None:
                        self.face_detect_time = time.time()

                if (end_face_detection and time.time() > self.face_detect_time + 302) or \
                        time.time() > recognition_end_time:
                    self.end_face_detection = True
                    self.close_camera()
                    return

                self.face_image = Image.fromarray(frame)
                self.face_photo = get_image(self.face_image)
                self.face_label.configure(image=self.face_photo)

        except Exception as e:
               print("33")

        self.root.after(50, self.update_face_frame, end_face_detection, recognition_end_time)

    def close_camera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
