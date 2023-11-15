import cv2
import numpy as np

# Función para seleccionar el color y definir los rangos
def seleccionar_color(event, x, y, flags, param):
    global frame, seleccionando_color, rango_color, valor_matiz
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_seleccionado = hsv[y, x]
        h_min = max(0, int(color_seleccionado[0]) - 10)  # Asegúrate de que los valores sean enteros
        h_max = min(180, int(color_seleccionado[0]) + 10)  # Asegúrate de que los valores sean enteros
        rango_color = (h_min, h_max)
        valor_matiz = color_seleccionado[0]
        seleccionando_color = False

# Inicialización
cap = cv2.VideoCapture(0)
seleccionando_color = True
rango_color = None
valor_matiz = None

while True:
    ret, frame = cap.read()

    if ret:
        if seleccionando_color:
            cv2.putText(frame, "Haz clic en un color", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (rango_color[0], 100, 100), (rango_color[1], 255, 255))
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            texto0 = "Rango Color: {}-{}".format(rango_color[0], rango_color[1])
            texto1 = "Valor de Matiz: {}".format( valor_matiz)
            cv2.putText(frame, texto0, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, texto1, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        cv2.setMouseCallback('frame', seleccionar_color)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
