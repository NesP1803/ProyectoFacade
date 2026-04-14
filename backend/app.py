from flask import Flask

from controllers.order_controller import order_blueprint
import controllers.order_controller as order_controller
from facade.order_facade import OrderFacade
from services.notification_service import NotificationService
from services.payment_service import PaymentService
from services.product_service import ProductService


def create_app() -> Flask:
    app = Flask(__name__)

    # Composition root: build concrete services and inject into Facade.
    product_service = ProductService()
    payment_service = PaymentService()
    notification_service = NotificationService()

    order_controller.order_facade = OrderFacade(
        product_service=product_service,
        payment_service=payment_service,
        notification_service=notification_service,
    )

    app.register_blueprint(order_blueprint)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
