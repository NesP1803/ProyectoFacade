from dataclasses import asdict, dataclass

from services.notification_service import NotificationService
from services.payment_service import PaymentResult, PaymentService
from services.product_service import Product, ProductService


@dataclass
class ProcessOrderResponse:
    success: bool
    message: str
    order_reference: str | None = None
    total_amount: float | None = None
    transaction_id: str | None = None


class OrderFacade:
    """
    Facade pattern implementation:
    - Composes all subsystem services.
    - Exposes a single high-level method `process_order`.
    - Hides orchestration complexity from clients/controllers.
    """

    def __init__(
        self,
        product_service: ProductService,
        payment_service: PaymentService,
        notification_service: NotificationService,
    ) -> None:
        self.product_service = product_service
        self.payment_service = payment_service
        self.notification_service = notification_service

    def process_order(
        self,
        user_id: str,
        email: str,
        product_id: str,
        quantity: int,
        payment_method: str,
    ) -> dict:
        print("[OrderFacade] Starting order orchestration")

        product: Product | None = self.product_service.get_product(product_id)
        if not product:
            return asdict(ProcessOrderResponse(success=False, message="Product not found"))

        if quantity <= 0:
            return asdict(ProcessOrderResponse(success=False, message="Quantity must be greater than 0"))

        if not self.product_service.reserve_stock(product_id=product_id, quantity=quantity):
            return asdict(
                ProcessOrderResponse(success=False, message="Insufficient stock or invalid product")
            )

        total_amount = round(product.price * quantity, 2)
        payment_result: PaymentResult = self.payment_service.charge(
            user_id=user_id,
            amount=total_amount,
            payment_method=payment_method,
        )

        if not payment_result.success:
            return asdict(ProcessOrderResponse(success=False, message=payment_result.message or "Payment failed"))

        order_reference = f"ORD-{user_id[:3].upper()}-{product_id.upper()}-{quantity}"

        self.notification_service.send_order_confirmation(
            email=email,
            order_reference=order_reference,
        )

        print("[OrderFacade] Order orchestration completed successfully")
        return asdict(
            ProcessOrderResponse(
                success=True,
                message="Order processed successfully",
                order_reference=order_reference,
                total_amount=total_amount,
                transaction_id=payment_result.transaction_id,
            )
        )
