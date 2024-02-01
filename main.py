import cv2
import tensorflow as tf
from yolov8 import prodect_creews, display_image
#Vamos a capturar el objeto que queremos identificar



#Leemos la imagen del objeto que queremos identificar
#obj = cv2.imread('objeto.jpg',0)      # Leemos la imagen
#recorte = obj[160:300, 230:380]       # Recortamos la imagen para que quede solo el objeto (fila:fila, colum:colum)
#cv2.imshow('objeto',recorte)          # Mostramos en pantalla el objeto a reconocer



def main():
    cap = cv2.VideoCapture(0)  # Elegimos la camara con la que vamos a hacer la deteccion
    while (True):
        ret, frame = cap.read()  # Leemos el video
        cv2.imshow('Objeto', frame)  # Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el video
            break
    cv2.imwrite('objeto.jpg', frame)  # Guardamos la ultima caputra del video como imagen
    cap.release()  # Cerramos
    cv2.destroyAllWindows()
    YOLO_MODEL = tf.keras.models.load_model('media/saved_model/model', compile=False, safe_mode=False)
    prodect_creews(yolo_model=YOLO_MODEL, image_path='objeto.jpg')

main()