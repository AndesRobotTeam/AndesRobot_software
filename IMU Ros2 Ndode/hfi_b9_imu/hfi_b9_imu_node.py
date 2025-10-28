#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion, TransformStamped
import tf_transformations
import serial, struct, math, threading
from tf2_ros import TransformBroadcaster

# ---------- FUNCIONES AUXILIARES ----------
def check_sum(data):
    return sum(data[0:10]) & 0xff == data[10]

def hex_to_short(raw):
    return list(struct.unpack("hhhh", bytearray(raw)))

def euler_to_quaternion(roll, pitch, yaw):
    qx, qy, qz, qw = tf_transformations.quaternion_from_euler(roll, pitch, yaw)
    q = Quaternion()
    q.x, q.y, q.z, q.w = qx, qy, qz, qw
    return q


# ---------- NODO PRINCIPAL ----------
class HfiB9Node(Node):
    def __init__(self):
        super().__init__('hfi_b9_imu')

        # Variables
        self.buf = bytearray()
        self.accel = [0.0, 0.0, 0.0]
        self.gyro = [0.0, 0.0, 0.0]
        self.ang = [0.0, 0.0, 0.0]

        # Publicadores
        self.publisher = self.create_publisher(Imu, '/imu/data', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # Puerto serie
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 921600, timeout=0.5)
            self.get_logger().info('✅ Puerto /dev/ttyUSB0 abierto a 921600 baud')
        except Exception as e:
            self.get_logger().error(f'❌ No se pudo abrir el puerto: {e}')
            raise SystemExit

        # Hilo de lectura
        threading.Thread(target=self.read_serial, daemon=True).start()


    # ---------- LECTURA DE DATOS ----------
    def read_serial(self):
        while rclpy.ok():
            data = self.ser.read()
            if not data:
                continue
            b = data[0]
            self.buf.append(b)
            if len(self.buf) >= 11:
                if self.buf[0] != 0x55:
                    self.buf.pop(0)
                    continue
                head = self.buf[1]
                if head in [0x51, 0x52, 0x53] and check_sum(self.buf):
                    vals = hex_to_short(self.buf[2:10])
                    if head == 0x51:
                        self.accel = [v/32768*16*9.8 for v in vals[:3]]
                    elif head == 0x52:
                        self.gyro = [v/32768*2000*math.pi/180 for v in vals[:3]]
                    elif head == 0x53:
                        self.ang = [v/32768*math.pi for v in vals[:3]]
                        self.publish_imu()
                    self.buf.clear()
                else:
                    self.buf.clear()


    # ---------- PUBLICACIÓN DE IMU + TF ----------
    def publish_imu(self):
        roll, pitch, yaw = self.ang
        q = euler_to_quaternion(roll, pitch, yaw)

        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'  # ✅ frame correcto
        msg.orientation = q

        msg.linear_acceleration.x = self.accel[0]
        msg.linear_acceleration.y = self.accel[1]
        msg.linear_acceleration.z = self.accel[2]

        msg.angular_velocity.x = self.gyro[0]
        msg.angular_velocity.y = self.gyro[1]
        msg.angular_velocity.z = self.gyro[2]

        self.publisher.publish(msg)

        # TF base_link → imu_link
        t = TransformStamped()
        t.header.stamp = msg.header.stamp
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'imu_link'
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation = q
        self.tf_broadcaster.sendTransform(t)


# ---------- MAIN ----------
def main(args=None):
    rclpy.init(args=args)
    node = HfiB9Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
