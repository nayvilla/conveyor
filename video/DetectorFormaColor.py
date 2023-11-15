import cv2
#import numpy as np
import torch

# Inicializar el modelo de detección de figuras
model_figuras = torch.hub.load('ultralytics/yolov5', 'custom',
                              path=r'model\detectorFiguras.pt')

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Definir los rangos de colores
azulBajo = 100
azulAlto = 113

amarilloBajo = 25
amarilloAlto = 38

naranjaBajo = 14#9
naranjaAlto = 24#12

rojoBajo = 0
rojoAlto = 8

moradoBajo = 114
moradoAlto = 170

verdeBajo = 39
verdeAlto = 85

cafeBajo = 9#11
cafeAlto = 13#24

def obtener_color(hsv):
    if azulBajo <= hsv[0] <= azulAlto:
        return "Azul"
    elif amarilloBajo <= hsv[0] <= amarilloAlto:
        return "Amarillo"
    elif naranjaBajo <= hsv[0] <= naranjaAlto:
        return "Naranja"
    elif rojoBajo <= hsv[0] <= rojoAlto:
        return "Rojo"
    elif moradoBajo <= hsv[0] <= moradoAlto:
        return "Morado"
    elif verdeBajo <= hsv[0] <= verdeAlto:
        return "Verde"
    elif cafeBajo <= hsv[0] <= cafeAlto:
        return "Cafe"
    else:
        return "Desconocido"

# Ciclo infinito de video
while True:
    # Lectura de la cámara
    ret, frame = cap.read()

    if ret:
        # Aplicar un filtro de mediana al cuadro para suavizar la imagen
        #frame = cv2.medianBlur(frame, 5)

        # Detección de figuras
        detect_figuras = model_figuras(frame)  # Usa el modelo para detectar figuras en el cuadro completo

        for det in detect_figuras.pred[0]:
            forma = det[5]
            x1, y1, x2, y2 = map(int, det[:4])

            roi_color = frame[y1:y2, x1:x2]
            fHSV = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)

            # Crear máscaras específicas para cada rango de color
            mask_azul = cv2.inRange(fHSV, (azulBajo, 100, 100), (azulAlto, 255, 255))
            mask_amarillo = cv2.inRange(fHSV, (amarilloBajo, 100, 100), (azulAlto, 255, 255))
            mask_naranja = cv2.inRange(fHSV, (naranjaBajo, 100, 100), (azulAlto, 255, 255))
            mask_rojo = cv2.inRange(fHSV, (rojoBajo, 100, 100), (azulAlto, 255, 255))
            mask_morado = cv2.inRange(fHSV, (moradoBajo, 100, 100), (azulAlto, 255, 255))
            mask_verde = cv2.inRange(fHSV, (verdeBajo, 100, 100), (azulAlto, 255, 255))
            mask_cafe = cv2.inRange(fHSV, (cafeBajo, 100, 100), (azulAlto, 255, 255))

            # Aplicar las máscaras a la imagen
            mask = mask_azul + mask_amarillo + mask_naranja + mask_rojo + mask_morado + mask_verde + mask_cafe

            # Encuentra los contornos de los objetos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Filtro para evitar ruido
                    x, y, w, h = cv2.boundingRect(contour)
                    rectangulo_color = (0, 255, 0)  # Color del rectángulo
                    nombre_color = obtener_color(fHSV[y + h // 2, x + w // 2])
                    cv2.rectangle(roi_color, (x, y), (x + w, y + h), rectangulo_color, 2)
                    cv2.putText(roi_color, f"C: {nombre_color} F: {forma}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, rectangulo_color, 2)
                    #cv2.putText(roi_color, f"Forma: {forma}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, rectangulo_color, 2)
            print("Forma: " + str(forma) + " Color: "+ nombre_color)
        # Mostrar el cuadro completo
        cv2.imshow('frame', frame)

        #Cerrar ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
