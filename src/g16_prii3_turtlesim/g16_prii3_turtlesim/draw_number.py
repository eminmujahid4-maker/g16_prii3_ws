import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.srv import SetPen

PASOS = [
    ("girar", 1.57),
    ("avanzar", 3),
    ("lapiz_arriba", 0),
    ("girar", 4.71),
    ("avanzar", 1.5),
    ("girar", 4.71),
    ("lapiz_abajo", 0),
    ("avanzar", 2),
    ("circulo", 6.28),
]


class DrawNumber(Node):
    def __init__(self):
        super().__init__('draw_number')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.reset_client = self.create_client(Empty, '/reset')
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        self.create_service(Empty, 'stop_drawing', self.stop)
        self.create_service(Empty, 'resume_drawing', self.resume)
        self.create_service(Empty, 'restart_drawing', self.restart)

        self.paso = 0
        self.tiempo = 0.0
        self.pausado = False
        self.create_timer(0.05, self.dibujar)

    def stop(self, request, response):
        self.pausado = True
        self.pub.publish(Twist())
        return response

    def resume(self, request, response):
        self.pausado = False
        return response

    def restart(self, request, response):
        self.pub.publish(Twist())
        self.reset_client.call_async(Empty.Request())
        self.paso = 0
        self.tiempo = 0.0
        self.pausado = False
        return response

    def poner_lapiz(self, apagado):
        req = SetPen.Request()
        req.r = 179
        req.g = 184
        req.b = 255
        req.width = 3
        req.off = apagado
        self.pen_client.call_async(req)

    def dibujar(self):
        if self.pausado or self.paso >= len(PASOS):
            return

        accion, cantidad = PASOS[self.paso]

        if accion == "lapiz_arriba":
            self.poner_lapiz(1)
            self.paso += 1
            return
        if accion == "lapiz_abajo":
            self.poner_lapiz(0)
            self.paso += 1
            return

        msg = Twist()
        if accion == "avanzar":
            msg.linear.x = 1.0
        elif accion == "girar":
            msg.angular.z = 1.0
        elif accion == "circulo":
            msg.linear.x = 1.0
            msg.angular.z = 1.0
        self.pub.publish(msg)

        self.tiempo += 0.05
        if self.tiempo >= cantidad:
            self.pub.publish(Twist())
            self.paso += 1
            self.tiempo = 0.0


def main(args=None):
    rclpy.init(args=args)
    node = DrawNumber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
