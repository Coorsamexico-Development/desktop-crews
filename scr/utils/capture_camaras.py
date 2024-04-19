
import cv2
from PIL import Image, ImageTk
import os

class CaptureCameras:
    camaras = []
    cap = None
    def __init__(self, size = (256,256)):
        self.size = size
    
    def start(self):
        total_camaras=  self.count_cameras()
        if total_camaras > 0:
            self.set_camera(self.camaras[0])

    def count_cameras(self):
        self.camaras = []
        for i in range(10):
            capture = cv2.VideoCapture(i)
            if not capture.isOpened():
                continue
            self.camaras.append({f"Camará {i}": i})
            capture.release()
        return len(self.camaras)

    def set_camera(self, camara):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(list(camara.values())[0])

    
    def capture_frame(self):
        with_image = False
        if self.cap is not None:
            with_image, frame = self.cap.read()

        if not with_image:
            print(os.getcwd())
            captured_image = Image.open(os.path.join(os.getcwd(), "assets", "images", "image_not_available.png"))
            captured_image = captured_image.resize(self.size)
            photo_image = ImageTk.PhotoImage(captured_image)
        else:
            # Convert image from one color space to other
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # Capture the latest frame and transform to image
            captured_image = Image.fromarray(opencv_image)
            captured_image = captured_image.resize(self.size)
            # Convert captured image to photoimage
            photo_image = ImageTk.PhotoImage(captured_image, size=self.size)

        return with_image, photo_image