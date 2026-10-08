import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.srv import SetPen

def mov(lin, ang, seg, arriba=False):
    return {"lin": lin, "ang": ang, "seg": seg, "arriba": arriba}


MOVS = [
    mov(0.0, 1.0, 1.57),
    mov(1.0, 0.0, 3.0),
    mov(0.0, 1.0, 4.71, True),
    mov(1.0, 0.0, 1.5, True),
    mov(0.0, 1.0, 4.71, True),
    mov(1.0, 0.0, 2.0),
    mov(1.0, 1.0, 6.28),
]


class DrawNumber(Node):
    def __init__(self):
        super().__init__('draw_number')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.reset_cli = self.create_client(Empty, '/reset')
        self.pen_cli = self.create_client(SetPen, '/turtle1/set_pen')

        self.create_service(Empty, 'stop_drawing', self.stop)
        self.create_service(Empty, 'resume_drawing', self.resume)
        self.create_service(Empty, 'restart_drawing', self.restart)

        self.paso = 0
        self.tiempo = 0.0
        self.pausa = False
        self.arriba = False
        self.create_timer(0.05, self.dibujar)

    def stop(self, request, response):
        self.pausa = True
        self.pub.publish(Twist())
        return response

    def resume(self, request, response):
        self.pausa = False
        return response

    def restart(self, request, response):
        self.pub.publish(Twist())
        self.reset_cli.call_async(Empty.Request())
        self.paso = 0
        self.tiempo = 0.0
        self.pausa = False
        self.arriba = False
        return response

    def lapiz(self, arriba):
        if arriba == self.arriba:
            return
        req = SetPen.Request()
        req.r = 255
        req.g = 255
        req.b = 255
        req.width = 3
        req.off = 1 if arriba else 0
        self.pen_cli.call_async(req)
        self.arriba = arriba

    def dibujar(self):
        if self.pub.get_subscription_count() == 0:
            return
        if self.pausa or self.paso >= len(MOVS):
            return

        actual = MOVS[self.paso]
        self.lapiz(actual["arriba"])

        msg = Twist()
        msg.linear.x = actual["lin"]
        msg.angular.z = actual["ang"]
        self.pub.publish(msg)

        self.tiempo += 0.05
        if self.tiempo >= actual["seg"]:
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
