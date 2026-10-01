# g16_prii3_ws
Grupo 16. El nodo dibuja el número 16 con turtlesim y tiene servicios para parar, reanudar y reiniciar el dibujo.

## Requisitos
- Ubuntu 22.04
- ROS2 Humble
- turtlesim. Se instala con este comando:
sudo apt install ros-humble-turtlesim

## Instalación
En una terminal, copia estos comandos:
git clone https://github.com/eminmujahid4-maker/g16_prii3_ws.git
cd g16_prii3_ws
colcon build --symlink-install
source install/setup.bash

## Ejecución
Después, ejecuta este comando:
ros2 launch g16_prii3_turtlesim draw_number.launch.py

## Servicios
En otra terminal, desde la carpeta g16_prii3_ws, ejecuta uno de estos comandos:
ros2 service call /stop_drawing std_srvs/srv/Empty
ros2 service call /resume_drawing std_srvs/srv/Empty
ros2 service call /restart_drawing std_srvs/srv/Empty

 -stop_drawing: detiene el dibujo.
 -resume_drawing: lo reanuda.
 -restart_drawing: borra la pantalla y lo reinicia.
