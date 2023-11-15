
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QTextEdit, QPushButton, QAction, QMessageBox, QLineEdit, QWidget, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize
from datetime import datetime
import cv2
import subprocess #correr script de python
import shutil #guardar imagen con nuevo nombre
import pandas as pd

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
        boton_tomar = QPushButton("Iniciar", self)
        boton_tomar.move(50, 220)
        boton_tomar.resize(120, 30)
        boton_tomar.setStyleSheet("background-color: #C70039; color: white; border-radius: 10px;")
        boton_tomar.setToolTip('Preciona este boton para tomar una foto')

        boton_salir = QPushButton("Salir", self)
        boton_salir.move(50, 270)
        boton_salir.resize(120, 30)
        boton_salir.setStyleSheet("background-color: #C70039; color: white; border-radius: 10px;")
        boton_salir.setToolTip('Preciona para salir de la aplicación')

        # Conectar señal "clicked" de los botones a sus correspondientes funciones
        boton_tomar.clicked.connect(self.iniciar)
        boton_salir.clicked.connect(self.salir)
    #--------------------------------CREACION DE FUNCIONES---------------------------------------------------
    # Función que se ejecuta cuando se presiona el botón "ENCONTRAR MI COLOR"
    def Camarea(self):
        # seleccion de la base de datos
        ventana.close()

    # Función que se ejecuta cuando se presiona el botón "TOMAR"
    def iniciar(self):
        #sasasas
        ventana.close()
        #///////////////////////////////////////////////
        # Mostrar VentanaResultados
        self.ventana_resultados = VentanaResultados()
        self.ventana_resultados.show()
                        
    # Función que se ejecuta cuando se presiona el botón "SALIR"
    def salir(self):
        # Mostramos un mensaje de confirmación al usuario
        reply = QMessageBox.question(self, 'Salir', '¿Estás seguro de que quieres salir?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Si el usuario elige 'Yes', cerramos la aplicación
        if reply == QMessageBox.Yes:
            QApplication.quit()

   
    def mas_colores(self):
        #------------Cerar ventana anterior--------------
        self.ventana_resultados = VentanaResultados()
        self.ventana_resultados.close()
        #///////////////////////////////////////////////
        # Mostrar VentanaColores
       
    def regreso_main(self):
        self.ventana_resultados = VentanaResultados()
        self.ventana_resultados.close()
        ventana.show()  

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------VENTANA RESULTADOS ------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class VentanaResultados(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resultados")
        self.setGeometry(200, 200, 668, 810)

        # Parte izquierda
        # imagen_original = QLabel("Imagen original", self)
        # imagen_original.move(130, 20)

        imagen_original_path = r"src\utaLogo.png" # Reemplazar con la ruta de la imagen
        imagen_original_pixmap = QPixmap(imagen_original_path)
        imagen_original_pixmap = imagen_original_pixmap.scaled(QSize(300, 300))
        imagen_original_imagen = QLabel("", self)
        imagen_original_imagen.setPixmap(imagen_original_pixmap)
        imagen_original_imagen.move(20, 50)

        # Parte inferior
        renderizado = QLabel("Renderizado de coloración", self)
        renderizado.move(150, 370)
        
        # Botones inferiores
        boton_probar_mas_colores = QPushButton("Cámara", self)
        boton_probar_mas_colores.move(450, 500)
        boton_probar_mas_colores.resize(200, 30)
        boton_probar_mas_colores.setStyleSheet("background-color: #C70039; color: white; border-radius: 15px;")
        boton_probar_mas_colores.setToolTip('Preciona para ver más opciones de coloración capilar')
        boton_probar_mas_colores.clicked.connect(ventana.mas_colores)

        boton_main = QPushButton("REGRESAR", self)
        boton_main.move(450, 700)
        boton_main.resize(200, 30)
        boton_main.setStyleSheet("background-color: #C70039; color: white; border-radius: 15px;")
        boton_main.setToolTip('Presiona para regresar a la ventana principal')
        boton_main.clicked.connect(ventana.regreso_main)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------VENTANA MAS COLORES------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# class VentanaColores(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Más recomendaciones")
#         self.setGeometry(200, 200, 2000, 810)
        
#         # Parte 1
#         imagen_1 = QLabel("Rubio cenizo", self)
#         imagen_1.move(130, 10)

#         imagen_1_path = r"src\utaLogo.png" # Reemplazar con la ruta de la imagen original
#         imagen_1_pixmap = QPixmap(imagen_1_path)
#         imagen_1_pixmap = imagen_1_pixmap.scaled(QSize(300, 300))
#         imagen_1_imagen = QLabel("", self)
#         imagen_1_imagen.setPixmap(imagen_1_pixmap)
#         imagen_1_imagen.move(20, 40)

#         #configuracion de boton salir
#         boton_salir_colores = QPushButton("SALIR", self)
#         boton_salir_colores.move(1670, 10)
#         boton_salir_colores.resize(200, 500)
#         boton_salir_colores.setStyleSheet("background-color: #C70039; color: white; border-radius: 15px;")
#         boton_salir_colores.setToolTip('Preciona para salir de la aplicacion')
#         boton_salir_colores.clicked.connect(ventana.salir)

#         #configuracion de boton regresar
#         boton_regresar_colores = QPushButton("REGRESAR", self)
#         boton_regresar_colores.move(1670, 540)
#         boton_regresar_colores.resize(200, 450)
#         boton_regresar_colores.setStyleSheet("background-color: #C70039; color: white; border-radius: 15px;")
#         boton_regresar_colores.setToolTip('Preciona para regresar a la pestaña anterior')
#         boton_regresar_colores.clicked.connect(ventana.procesar_imagen)


if __name__ == '__main__':
    app = QApplication([])
    ventana = Ventana()
    #ventana.setStyleSheet("background-color: #222222;")
    ventana.show()
    app.exec_()


