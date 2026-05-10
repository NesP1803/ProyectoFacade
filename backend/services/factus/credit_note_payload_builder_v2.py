from .payload_builder_v2 import build_payment_details, price_net_from_gross


def build_credit_note_item(description: str, quantity: float, gross_price: float, tax_rate: float) -> dict:
    taxes = [{"is_excluded": True}] if float(tax_rate) == 0 else [{"code": "01", "rate": f"{float(tax_rate):.2f}"}]
    return {
        "description": description,
        "quantity": str(quantity),
        "price": price_net_from_gross(gross_price, tax_rate),
        "taxes": taxes,
    }


def build_credit_note_payload(reference_code: str, bill_number: str, amount: float) -> dict:
    return {
        "reference_code": reference_code,
        "bill_number": bill_number,
        "payment_details": build_payment_details("1", "10", amount),
    }
