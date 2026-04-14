from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    transaction_id: str | None = None
    message: str | None = None


class PaymentService:
    """Subsystem #2: Handles payment authorization/capture simulation."""

    def charge(self, user_id: str, amount: float, payment_method: str) -> PaymentResult:
        print(
            "[PaymentService] Charging payment: "
            f"user='{user_id}', amount={amount:.2f}, method='{payment_method}'"
        )

        # Teaching rule: reject card tokens that start with 'FAIL' to simulate failure.
        if payment_method.upper().startswith("FAIL"):
            print("[PaymentService] Payment rejected by processor simulation")
            return PaymentResult(success=False, message="Payment was declined")

        tx_id = f"TX-{user_id[:3].upper()}-{int(amount * 100)}"
        print(f"[PaymentService] Payment authorized. transaction_id='{tx_id}'")
        return PaymentResult(success=True, transaction_id=tx_id, message="Payment approved")
