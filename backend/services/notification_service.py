class NotificationService:
    """Subsystem #3: Sends notifications (mock)."""

    def send_order_confirmation(self, email: str, order_reference: str) -> bool:
        print(
            "[NotificationService] Sending confirmation "
            f"to '{email}' for order '{order_reference}'"
        )
        return True
