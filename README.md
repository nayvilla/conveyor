# conveyor
conveyor

Un colorímetro básicamente es un recurso que se utiliza para identificar el color y el matiz para realizar una medición de color aproximada. Esta herramienta mide la absorbancia de una disolución en una 
frecuencia de luz. El objetivo de este proyecto es la implementación de un sistema de detección de colores y formas utilizando visión artificial, si bien es cierto un colorímetro comercial posee la característica 
de tener un sensor de color, pero, en esta ocasión también se va a identificar la forma, por lo que la tecnología propicia para este tipo de identificación es la visión artificial, sin necesidad de un sensor de 
color por medio de dicha tecnología se logrará identificar el color de las figuras, por lo que además se puede ampliar el rango de colores a medir. El sistema consta de una cinta transportadora que mueve el objeto 
en cuestión, luego, cuando el sensor infrarrojo detecta una señal la cinta detiene su movimiento y se procede a captar imágenes por medio de la cámara web, estos datos son procesados por el software de visión 
artificial, el cual se basa en el algoritmo YOLO y la utilización de la librería Open CV, una vez que el sistema detecta los datos de color y forma son expuestos en la aplicación de computador y en la pantalla LCD 
que tiene el sistema en su parte física. De esta manera se logrará comparar valores de exactitud en las mediciones del sistema.

Cinta transportadora

![image](https://github.com/nayvilla/conveyor/assets/94719402/95ddfc1b-a3dc-49c4-99df-ed83c1beab8e)

Aplicación de control con visión artificial 

![image](https://github.com/nayvilla/conveyor/assets/94719402/de58696a-e713-4f77-8355-ba4711ce2730)

Resultados de modelo de YOLOV5x

![image](https://github.com/nayvilla/conveyor/assets/94719402/a5afe829-6a47-495d-aec7-77c6d33ab5bc)
![image](https://github.com/nayvilla/conveyor/assets/94719402/7dae95a9-4f65-4564-b69c-a7f9d66dfcf4)
![image](https://github.com/nayvilla/conveyor/assets/94719402/75fd05a8-d82e-4f24-bc03-da2ed716d7ad)
![image](https://github.com/nayvilla/conveyor/assets/94719402/448b9dba-6b53-46c9-aee6-c980c4f4b1cd)

Matriz de confusión
![image](https://github.com/nayvilla/conveyor/assets/94719402/9edf31e4-4a13-420c-8dab-f2fb99e86735)







