import cv2
import numpy as np

# Función para obtener el nombre del color en función del rango
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

# Video captura
cap = cv2.VideoCapture(0)

# Colores en:         H    S   V
amarilloBajo = 25
amarilloAlto = 38

naranjaBajo = 9
naranjaAlto = 13

rojoBajo = 0
rojoAlto = 8

moradoBajo = 124
moradoAlto = 139

azulBajo = 100
azulAlto = 123

verdeBajo = 39
verdeAlto = 85

cafeBajo = 14
cafeAlto = 24

# Definir la región de interés (ROI)
x_roi, y_roi, w_roi, h_roi = 100, 100, 200, 200

# Ciclo infinito de video
while True:
    # Lectura de la cámara
    ret, frame = cap.read()

    if ret == True:
        # Aplicar un filtro de mediana al cuadro para suavizar la imagen
        frame = cv2.medianBlur(frame, 5)

        # Obtener la región de interés (ROI) del cuadro
        roi = frame[y_roi:y_roi + h_roi, x_roi:x_roi + w_roi]

        fHSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Crear máscaras específicas para cada rango de color
        mask_azul = cv2.inRange(fHSV, (azulBajo, 100, 100), (azulAlto, 255, 255))
        mask_amarillo = cv2.inRange(fHSV, (amarilloBajo, 100, 100), (amarilloAlto, 255, 255))
        mask_naranja = cv2.inRange(fHSV, (naranjaBajo, 100, 100), (naranjaAlto, 255, 255))
        mask_rojo = cv2.inRange(fHSV, (rojoBajo, 100, 100), (rojoAlto, 255, 255))
        mask_morado = cv2.inRange(fHSV, (moradoBajo, 100, 100), (moradoAlto, 255, 255))
        mask_verde = cv2.inRange(fHSV, (verdeBajo, 100, 100), (verdeAlto, 255, 255))
        mask_cafe = cv2.inRange(fHSV, (cafeBajo, 100, 100), (cafeAlto, 255, 255))

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
                cv2.rectangle(roi, (x, y), (x + w, y + h), rectangulo_color, 2)  # Dibuja un rectángulo verde alrededor del objeto
                cv2.putText(roi, nombre_color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, rectangulo_color, 2)

        # Mostrar el cuadro completo con el ROI
        frame[y_roi:y_roi + h_roi, x_roi:x_roi + w_roi] = roi
        cv2.imshow('frame', frame)

        #Cerrar ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
