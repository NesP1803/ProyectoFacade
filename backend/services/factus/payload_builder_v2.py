from decimal import Decimal, ROUND_HALF_UP


def to_decimal(value: float | str | Decimal) -> Decimal:
    return Decimal(str(value))


def price_net_from_gross(price_gross: float | str, tax_rate: float | str) -> str:
    gross = to_decimal(price_gross)
    rate = to_decimal(tax_rate)
    if rate <= 0:
        return str(gross.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    net = gross / (Decimal("1") + (rate / Decimal("100")))
    return str(net.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def build_payment_details(payment_form: str, payment_method_code: str, amount: float, reference_code: str = "", due_date: str | None = None) -> list[dict]:
    detail = {
        "payment_form": payment_form,
        "payment_method_code": payment_method_code,
        "reference_code": reference_code,
        "amount": str(to_decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
    }
    if due_date:
        detail["due_date"] = due_date
    return [detail]
