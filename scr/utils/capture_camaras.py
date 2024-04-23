
import cv2
from PIL import Image, ImageTk
import os

CAPTURE_WIDTH = 640
CAPTURE_HEIGTH = 640

class CaptureCameras:
    camaras = {}
    cap = None
    camara_index = None
    camara_open = False
    def __init__(self):
        pass
    
    def start(self):
        total_camaras=  self.count_cameras()
        if total_camaras > 0:
            first_camara = list(self.camaras.keys())[0]
            self.set_camera(self.camaras[first_camara])

    def count_cameras(self):
        self.camaras = {}
        for i in range(10):
            capture = cv2.VideoCapture(i)
            if not capture.isOpened():
                continue
            self.camaras[f"Cámara {i+1}"]= i
            capture.release()
        return len(self.camaras.keys())

    def set_camera(self, camara_index):
        self.camara_index = camara_index
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(camara_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGTH)
        return self.cap.isOpened()
    
    def leave_camera(self): 
        if self.cap is not None:
            self.cap.release()

    
    def capture_frame(self):
        with_image = False 
        
        if self.cap is not None:
            with_image, frame = self.cap.read()

        if not with_image:
            frame = Image.open(os.path.join(os.getcwd(), "assets", "images", "image_not_available.png"))
        else:
            # Convert image from one color space to other
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Capture the latest frame and transform to image
            frame = Image.fromarray(opencv_image)
            #frame = Image.open(os.path.join(os.getcwd(), "assets", "images", "image_test.jpeg"))
        return with_image, frame