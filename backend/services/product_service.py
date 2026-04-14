from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int


class ProductService:
    """Subsystem #1: Handles product lookup and stock management."""

    def __init__(self) -> None:
        self._products: Dict[str, Product] = {
            "p1": Product(id="p1", name="Wireless Headphones", price=59.99, stock=8),
            "p2": Product(id="p2", name="Mechanical Keyboard", price=89.99, stock=5),
            "p3": Product(id="p3", name="USB-C Hub", price=34.50, stock=12),
        }

    def get_product(self, product_id: str) -> Optional[Product]:
        print(f"[ProductService] Looking up product '{product_id}'")
        return self._products.get(product_id)

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        print(f"[ProductService] Reserving stock: product='{product_id}', quantity={quantity}")
        product = self._products.get(product_id)
        if not product:
            return False
        if quantity <= 0 or product.stock < quantity:
            return False
        product.stock -= quantity
        print(f"[ProductService] Reservation successful. Remaining stock={product.stock}")
        return True
