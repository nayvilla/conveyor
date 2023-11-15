#Importación de librerias
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QMessageBox, QFrame
from PyQt5.QtGui import QFont, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QSize, QTimer
import os
import cv2
import torch
import serial 
import time 
import sys
# Redirige sys.stderr a sys.__stderr__ si sys.stderr es None
if sys.stderr is None:
    sys.stderr = sys.__stderr__

# Inicializar el modelo de detección de figuras
script_dir = os.path.dirname(os.path.abspath(__file__))
modelo_path = os.path.join(script_dir, "model", "detectorFiguras.pt")
model_figuras = torch.hub.load('ultralytics/yolov5', 'custom', path=modelo_path)

#Comunicacion serial
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1) 
def write_read(x): 
	arduino.write(bytes(x, 'utf-8')) 
	time.sleep(0.05) 
	data = arduino.readline() 
	return data 

# Definir los rangos de colores
azulBajo = 102#100
azulAlto = 110#113

amarilloBajo = 23#25
amarilloAlto = 30#38

naranjaBajo = 9#9 14
naranjaAlto = 13#12 18

rojoBajo = 0
rojoAlto = 8

moradoBajo = 114
moradoAlto = 143

verdeBajo = 39
verdeAlto = 92

cafeBajo = 14#11 9 
cafeAlto = 18#24 13

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

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 520, 480)
        self.setWindowTitle("Colorímetro")

        # Crear una etiqueta para la imagen de fondo
        fondo_label = QLabel(self)
        fondo_label.setGeometry(0, 0, 520, 480)

        # Cargar la imagen de fondo y ajustarla a las dimensiones de la etiqueta
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "src", "OBDPMQ0.jpg")
        fondo_image = QPixmap(image_path)
        fondo_image = fondo_image.scaled(520, 480)

        # Establecer la imagen de fondo en la etiqueta
        fondo_label.setPixmap(fondo_image)
        
        #Fondo de letras
        self.myFont_Enacabezado=QFont('Helvetica [Cronyx]', 12)
        self.myFont_Enacabezado.setBold(True)
        self.myFont_Cuerpo=QFont('Helvetica [Cronyx]', 10)
        self.myFont_Cuerpo.setBold(False)
        self.color_letra= "#E7E5E5"

        # Encabezado
        label_nombre = QLabel("UNIVERSIDAD TÉCNICA DE AMBATO", self)
        label_nombre.move(105, 30)
        label_nombre.resize(350, 30)
        label_nombre.setFont(self.myFont_Enacabezado)
        label_nombre.setStyleSheet(f'color:{self.color_letra}')

        label_fisei = QLabel("FISEI", self)
        label_fisei.move(230, 60)
        label_fisei.setFont(self.myFont_Enacabezado)
        label_fisei.setStyleSheet(f'color:{self.color_letra}')

        label_tele = QLabel("Telecomunicaciones", self)
        label_tele.move(175, 90)
        label_tele.resize(350, 30)
        label_tele.setFont(self.myFont_Enacabezado)
        label_tele.setStyleSheet(f'color:{self.color_letra}')

        # Integrantes
        label_integrantes = QLabel("Integrantes:", self)
        label_integrantes.move(280, 190)
        label_integrantes.setFont(self.myFont_Enacabezado)
        label_integrantes.setStyleSheet(f'color:{self.color_letra}')

        label_nombre1 = QLabel("• Joel Criollo", self)
        label_nombre1.move(300, 220)
        label_nombre1.setFont(self.myFont_Cuerpo)
        label_nombre1.setStyleSheet(f'color:{self.color_letra}')

        label_nombre2 = QLabel("• Romer Manobanda", self)
        label_nombre2.move(300, 250)
        label_nombre2.setFont(self.myFont_Cuerpo)
        label_nombre2.setStyleSheet(f'color:{self.color_letra}')

        label_nombre3 = QLabel("• Evelyn Manotoa", self)
        label_nombre3.move(300, 280)
        label_nombre3.setFont(self.myFont_Cuerpo)
        label_nombre3.setStyleSheet(f'color:{self.color_letra}')

        # Pie de página
        label_pie = QLabel("© 2023 UTA", self)
        label_pie.move(240, 400)
        label_pie.setFont(self.myFont_Cuerpo)
        label_pie.setStyleSheet(f'color:{self.color_letra}')

        # Botones
        boton_bienvenido = QPushButton("Bienvenido", self)
        boton_bienvenido.move(50, 220)
        boton_bienvenido.resize(120, 30)
        boton_bienvenido.setFont(self.myFont_Cuerpo)
        boton_bienvenido.setStyleSheet(f"background-color: #C70039; color: {self.color_letra}; border-radius: 10px;")
        boton_bienvenido.setToolTip('Presiona este botón para tomar una foto')

        boton_salir = QPushButton("Salir", self)
        boton_salir.move(50, 270)
        boton_salir.resize(120, 30)
        boton_salir.setFont(self.myFont_Cuerpo)
        boton_salir.setStyleSheet(f"background-color: #C70039; color: {self.color_letra}; border-radius: 10px;")
        boton_salir.setToolTip('Presiona para salir de la aplicación')

        # Conectar señal "clicked" de los botones a sus correspondientes funciones
        boton_bienvenido.clicked.connect(self.iniciar)
        boton_salir.clicked.connect(self.salir)

        # ... (resto del código)

    def iniciar(self):
        ventana.close()
        self.ventana_resultados = VentanaResultados(self)
        self.ventana_resultados.show()

    def salir(self):
        reply = QMessageBox.question(self, 'Salir', '¿Estás seguro de que quieres salir?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def mas_colores(self):
        self.ventana_resultados = VentanaResultados(self)
        self.ventana_resultados.close()

    def regreso_main(self):
        self.ventana_resultados = VentanaResultados(self)
        self.ventana_resultados.close()
        self.show()

class VentanaResultados(QWidget):
    def __init__(self, ventana_padre):
        super().__init__()
        
        font_cuerpo = ventana.myFont_Cuerpo
        color_letra = ventana.color_letra
        self.ventana_padre = ventana_padre
        self.desconectar = 0

        self.setWindowTitle("Detección de formas y colores")
        self.setGeometry(200, 200, 640, 600)

        # Crear una etiqueta para la imagen de fondo
        fondo_label = QLabel(self)
        fondo_label.setGeometry(0, 0, 640, 600)

        # Cargar la imagen de fondo y ajustarla a las dimensiones de la etiqueta
        fondo_image = QPixmap(r"src/OBDPMQ0.jpg")
        fondo_image = fondo_image.scaled(640, 600)

        # Establecer la imagen de fondo en la etiqueta
        fondo_label.setPixmap(fondo_image)

        # Inicializar cámara
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_frame)

        self.cap = cv2.VideoCapture(0)
        self.label_camara = QLabel(self)
        self.label_camara.setGeometry(20, 55, 600, 400)

        # Etiquetas para mostrar forma y nombre_color
        self.label_forma = QLabel("Forma: ", self)
        self.label_forma.setGeometry(20, 465, 300, 20)
        self.label_forma.setFont(font_cuerpo)
        self.label_forma.setStyleSheet(f'color:{color_letra}')

        self.label_color = QLabel("Color: ", self)
        self.label_color.setGeometry(20, 485, 300, 20)
        self.label_color.setFont(font_cuerpo)
        self.label_color.setStyleSheet(f'color:{color_letra}')

        #Etiqueta conexion con arduino
        self.label_arduino = QLabel("Arduino: ", self)
        self.label_arduino.setGeometry(325, 465, 300, 20)
        self.label_arduino.setFont(font_cuerpo)
        self.label_arduino.setStyleSheet(f'color:{color_letra}')

        boton_camara_iniciar = QPushButton("Iniciar Detección", self)
        boton_camara_iniciar.move(20, 10)
        boton_camara_iniciar.resize(295, 45)
        boton_camara_iniciar.setFont(font_cuerpo)
        boton_camara_iniciar.setStyleSheet(f"background-color: #C70039; color: {color_letra}; border-radius: 10px;")
        boton_camara_iniciar.setToolTip('Presiona para iniciar el sistema')
        boton_camara_iniciar.clicked.connect(self.abrir_camara)

        boton_camara_detener = QPushButton("Detener detección", self)
        boton_camara_detener.move(325, 10)
        boton_camara_detener.resize(295, 45)
        boton_camara_detener.setFont(font_cuerpo)
        boton_camara_detener.setStyleSheet(f"background-color: #C70039; color: {color_letra}; border-radius: 10px;")
        boton_camara_detener.setToolTip('Presiona para detener el sistema')
        boton_camara_detener.clicked.connect(self.detener_camara)

        boton_main = QPushButton("Regresar", self)
        boton_main.move(20, 550)
        boton_main.resize(600, 30)
        boton_main.setFont(font_cuerpo)
        boton_main.setStyleSheet(f"background-color: #C70039; color: {color_letra}; border-radius: 10px;")
        boton_main.setToolTip('Presiona para regresar a la ventana principal')
        boton_main.clicked.connect(self.regresar_main)

    def abrir_camara(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error al abrir la cámara")
            return
        self.timer.start(30)
        self.desconectar = 1
        self.label_arduino.setText(f"Arduino: Conectado!")

    def detener_camara(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
        self.desconectar = 0
        self.label_arduino.setText(f"Arduino: Desconectado!")

    def mostrar_frame(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if ret:
            #Comprueba la coneccion
            #conexion = arduino.readline()
            #if conexion.decode('utf-8') == "Esperando..":
                #print("Conexión exitosa")
                #while True:
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
                forma_num = None
                color_forma = None
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 500:  # Filtro para evitar ruido
                        x, y, w, h = cv2.boundingRect(contour)
                        rectangulo_color = (0, 255, 0)  # Color del rectángulo
                        nombre_color = obtener_color(fHSV[y + h // 2, x + w // 2])
                        cv2.rectangle(roi_color, (x, y), (x + w, y + h), rectangulo_color, 2)
                        cv2.putText(roi_color, f"C: {nombre_color} F: {forma}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, rectangulo_color, 2)
                        #Detectar la forma
                        indice_parentesis = str(forma).find('(')
                        indice_punto = str(forma).find('.')
                        forma_num = str(forma)[indice_parentesis + 1 : indice_punto]
                        if forma_num == "0":
                            forma_detectada="Cuadrado"
                        elif forma_num == "1":
                            forma_detectada="Rectangulo"
                        elif forma_num == "2":
                            forma_detectada="Triangulo"
                        else: 
                            forma_detectada="Circulo"
                        #Imprimir en las etiquetas el resultado
                        self.label_forma.setText(f"Forma: {forma_detectada}")
                        self.label_color.setText(f"Color: {nombre_color}")
                        #Envio de datos al arduino uno                            
                        if nombre_color=="Azul" or nombre_color=="Desconocido":
                            color_forma="B"
                            enceder = "1"
                        else:
                            color_forma = nombre_color[0]
                            enceder = "1"
                        

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(img)
                self.label_camara.setPixmap(pixmap)
                #print(forma_num)
                write_read(f"1{forma_num}{color_forma}") 

    def regresar_main(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
        self.ventana_padre.show()
        self.close()

if __name__ == '__main__':
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec_()
