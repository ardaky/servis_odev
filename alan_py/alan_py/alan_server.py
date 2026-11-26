import rclpy
from rclpy.node import Node
from alan_interfaces.srv import RectangleArea


class AlanSunucu(Node):
    def __init__(self):
        super().__init__('rectangle_area_server')
        self.srv = self.create_service(
            RectangleArea, 'rectangle_area', self.alan_hesapla)
        self.get_logger().info('RectangleArea servisi hazir.')

    def alan_hesapla(self, request, response):
        # Bonus: negatif degerleri reddet
        if request.width < 0 or request.height < 0:
            response.area = 0.0
            response.success = False
            self.get_logger().warn(
                f'Reddedildi: negatif deger '
                f'(width={request.width}, height={request.height})')
            return response

        response.area = request.width * request.height
        response.success = True
        self.get_logger().info(
            f'{request.width} x {request.height} = {response.area}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AlanSunucu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
