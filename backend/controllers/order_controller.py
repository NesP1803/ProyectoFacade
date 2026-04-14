from flask import Blueprint, jsonify, request

from facade.order_facade import OrderFacade

order_blueprint = Blueprint("orders", __name__)


# Set by app factory in app.py.
order_facade: OrderFacade | None = None


@order_blueprint.route("/process", methods=["POST"])
def process_order():
    if order_facade is None:
        return jsonify({"success": False, "message": "OrderFacade is not configured"}), 500

    payload = request.get_json(silent=True) or {}

    required_fields = ["userId", "email", "productId", "quantity", "paymentMethod"]
    missing = [field for field in required_fields if field not in payload]
    if missing:
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Missing required fields: {', '.join(missing)}",
                }
            ),
            400,
        )

    try:
        quantity = int(payload["quantity"])
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Quantity must be an integer"}), 400

    response = order_facade.process_order(
        user_id=str(payload["userId"]),
        email=str(payload["email"]),
        product_id=str(payload["productId"]),
        quantity=quantity,
        payment_method=str(payload["paymentMethod"]),
    )

    status_code = 200 if response.get("success") else 400
    return jsonify(response), status_code
