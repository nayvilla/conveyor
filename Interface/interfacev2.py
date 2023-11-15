from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QSize, QTimer
import cv2

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 520, 480)
        self.setWindowTitle("Colorímetro")

        # Crear una etiqueta para la imagen de fondo
        fondo_label = QLabel(self)
        fondo_label.setGeometry(0, 0, 520, 550)

        # Cargar la imagen de fondo y ajustarla a las dimensiones de la etiqueta
        fondo_image = QPixmap(r"src\OBDPMQ0.jpg")
        fondo_image = fondo_image.scaled(520, 600)

        # Establecer la imagen de fondo en la etiqueta
        fondo_label.setPixmap(fondo_image)

        # Encabezado
        label_nombre = QLabel("Universidad Técnica Ambato", self)
        label_nombre.move(50, 30)
        label_nombre.resize(200, 30)
        label_nombre.setFont(QFont('Arial', 10))

        label_fisei = QLabel("FISEI", self)
        label_fisei.move(50, 60)
        label_fisei.setFont(QFont('Arial', 9))

        label_tele = QLabel("Telecomunicaciones", self)
        label_tele.move(50, 90)
        label_tele.setFont(QFont('Arial', 10))

        # Integrantes
        label_integrantes = QLabel("Integrantes:", self)
        label_integrantes.move(280, 190)
        label_integrantes.setFont(QFont('Arial', 10))

        label_nombre1 = QLabel("• Nombre 1", self)
        label_nombre1.move(300, 220)
        label_nombre1.setFont(QFont('Arial', 10))

        label_nombre2 = QLabel("• Nombre 2", self)
        label_nombre2.move(300, 250)
        label_nombre2.setFont(QFont('Arial', 10))

        label_nombre3 = QLabel("• Nombre 3", self)
        label_nombre3.move(300, 280)
        label_nombre3.setFont(QFont('Arial', 10))

        label_nombre4 = QLabel("• Nombre 4", self)
        label_nombre4.move(300, 310)
        label_nombre4.setFont(QFont('Arial', 10))

        # Pie de página
        label_pie = QLabel("© 2023 UTA", self)
        label_pie.move(240, 400)
        label_pie.setFont(QFont('Arial', 9))

        # Botones
        boton_tomar = QPushButton("Bienvenido", self)
        boton_tomar.move(50, 220)
        boton_tomar.resize(120, 30)
        boton_tomar.setStyleSheet("background-color: #C70039; color: white; border-radius: 10px;")
        boton_tomar.setToolTip('Presiona este botón para tomar una foto')

        boton_salir = QPushButton("Salir", self)
        boton_salir.move(50, 270)
        boton_salir.resize(120, 30)
        boton_salir.setStyleSheet("background-color: #C70039; color: white; border-radius: 10px;")
        boton_salir.setToolTip('Presiona para salir de la aplicación')

        # Conectar señal "clicked" de los botones a sus correspondientes funciones
        boton_tomar.clicked.connect(self.iniciar)
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

        self.ventana_padre = ventana_padre

        self.setWindowTitle("Detección de formas y Colores")
        self.setGeometry(200, 200, 640, 600)

        # Inicializar cámara
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_frame)

        self.cap = cv2.VideoCapture(0)
        self.label_camara = QLabel(self)
        self.label_camara.setGeometry(20, 55, 600, 400)

        boton_camara_iniciar = QPushButton("Iniciar Detección", self)
        boton_camara_iniciar.move(20, 10)
        boton_camara_iniciar.resize(295, 45)
        boton_camara_iniciar.setStyleSheet("background-color: #C70039; color: white; border-radius: 10px;")
        boton_camara_iniciar.setToolTip('Presiona para iniciar el sistema')
        boton_camara_iniciar.clicked.connect(self.abrir_camara)

        boton_camara_detener = QPushButton("Detener detección", self)
        boton_camara_detener.move(325, 10)
        boton_camara_detener.resize(295, 45)
        boton_camara_detener.setStyleSheet("background-color: #C70039; color: white; border-radius: 10px;")
        boton_camara_detener.setToolTip('Presiona para detener el sistema')
        boton_camara_detener.clicked.connect(self.detener_camara)

        boton_main = QPushButton("Regresar", self)
        boton_main.move(20, 550)
        boton_main.resize(600, 30)
        boton_main.setStyleSheet("background-color: #C70039; color: white; border-radius: 10px;")
        boton_main.setToolTip('Presiona para regresar a la ventana principal')
        boton_main.clicked.connect(self.regresar_main)

    def abrir_camara(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error al abrir la cámara")
            return
        self.timer.start(30)

    def detener_camara(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()

    def mostrar_frame(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if not ret:
            print(f"Error al capturar el fotograma. Retorno: {ret}")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.label_camara.setPixmap(pixmap)

    def regresar_main(self):
        self.ventana_padre.show()
        self.close()

if __name__ == '__main__':
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec_()
