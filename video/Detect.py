#importar librerias
import torch
import cv2
import numpy as np

#leemos el modelo
model=torch.hub.load('ultralytics/yolov5', 'custom',
                     path = r'model\detectorFiguras')

#video captura
cap =cv2.VideoCapture(0)

#ciclo infiinito de video
while True:
    #lectura de la camara
    ret, frame = cap.read()

    #deteciones
    detect = model (frame)

    #mostrar fps
    cv2.imshow('detector de figuras', np.squeeze(detect.render()))

    #Cerrar ventana
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

