import cv2
import tensorflow as tf
from yolov8 import prodect_creews, display_image
#Vamos a capturar el objeto que queremos identificar



#Leemos la imagen del objeto que queremos identificar
#obj = cv2.imread('objeto.jpg',0)      # Leemos la imagen
#recorte = obj[160:300, 230:380]       # Recortamos la imagen para que quede solo el objeto (fila:fila, colum:colum)
#cv2.imshow('objeto',recorte)          # Mostramos en pantalla el objeto a reconocer

YOLO_MODEL = tf.keras.models.load_model('models/model', compile=False, safe_mode=False)

def main():

    cap = cv2.VideoCapture(0)  # Elegimos la camara con la que vamos a hacer la deteccion
    while (True):
        ret, frame = cap.read()  # Leemos el video
        cv2.imshow('Objeto', frame)  # Mostramos el video en pantalla
        if cv2.waitKey(1) == 27 or cv2.waitKey(1) == 32:  # Cuando oprimamos "Escape" rompe el video
            break
    cv2.imwrite('objeto.jpg', frame)  # Guardamos la ultima caputra del video como imagen
    cap.release()  # Cerramos
    #cv2.destroyAllWindows()

    prodect_creews(yolo_model=YOLO_MODEL, image_path='objeto.jpg')
    cv2.destroyAllWindows()

main()