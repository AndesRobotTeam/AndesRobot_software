===============================
 HFI-B9 IMU ROS2 LAUNCH PACKAGE
===============================

📦 Este paquete contiene todo lo necesario para ejecutar el nodo y visualizar el IMU HFI-B9 en RViz2 (ROS2 Humble).

---
🧭 INSTRUCCIONES DE INSTALACIÓN
---

1️⃣ Clonar o descomprimir en tu workspace:
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws/src
    unzip hfi_b9_imu_full.zip

2️⃣ Compilar el paquete:
    cd ~/ros2_ws
    colcon build --packages-select hfi_b9_imu

3️⃣ Activar el entorno:
    source /opt/ros/humble/setup.bash
    source ~/ros2_ws/install/setup.bash

4️⃣ Ejecutar el nodo + RViz:
    ros2 launch hfi_b9_imu view_imu.launch.py

---
✅ El nodo publicará:
    /imu/data
    /tf  (frames base_link → imu_link)
Y mostrará los ejes del IMU rotando en tiempo real en RViz2.

