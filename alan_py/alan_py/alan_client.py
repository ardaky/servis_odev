import sys

import rclpy
from rclpy.node import Node
from alan_interfaces.srv import RectangleArea


class AlanIstemci(Node):
    def __init__(self):
        super().__init__('rectangle_area_client')
        self.cli = self.create_client(RectangleArea, 'rectangle_area')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Servis bekleniyor...')

    def istek_gonder(self, width, height):
        req = RectangleArea.Request()
        req.width = width
        req.height = height
        return self.cli.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    argv = rclpy.utilities.remove_ros_args(sys.argv)
    if len(argv) != 3:
        print('Kullanim: ros2 run alan_py alan_client <width> <height>')
        rclpy.shutdown()
        return

    width, height = float(argv[1]), float(argv[2])
    node = AlanIstemci()
    future = node.istek_gonder(width, height)
    rclpy.spin_until_future_complete(node, future)
    sonuc = future.result()
    if sonuc.success:
        node.get_logger().info(f'Alan: {width} x {height} = {sonuc.area}')
    else:
        node.get_logger().error(
            f'Sunucu istegi reddetti (negatif deger): {width}, {height}')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
