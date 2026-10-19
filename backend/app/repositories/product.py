from typing import List
from app.repositories.base import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository):
    def _to_product(self, row: dict) -> Product:
        return Product(
            product_id=row['product_id'],
            category_id=row['category_id'],
            category_name=row.get('category_name'),
            name=row['name'],
            brand=row['brand'],
            price=float(row['price']),
            cost_price=float(row['cost_price']),
            stock_quantity=row['stock_quantity'],
            min_stock_level=row['min_stock_level'],
            size=row.get('size'),
            description=row.get('description')
        )

    def get_all(self) -> List[Product]:
        query = """
            SELECT product.*, category.name AS category_name
            FROM products product
            LEFT JOIN categories category ON product.category_id = category.category_id
            ORDER BY product.name ASC
        """
        rows = self.execute_query(query)
        products = []
        
        for row in rows:
            products.append(self._to_product(row))
        return products

    def get_by_id(self, product_id: int) -> Product | None:
        query = """
            SELECT product.*, category.name AS category_name
            FROM products product
            LEFT JOIN categories category ON product.category_id = category.category_id
            WHERE product.product_id = %s
        """

        rows = self.execute_query(query, (product_id,))
        if not rows:
            return None

        row = rows[0]
        return self._to_product(row)

    def get_by_category(self, category_id: int) -> List[Product]:
        query = """
            SELECT product.*, category.name AS category_name
            FROM products product
            LEFT JOIN categories category ON product.category_id = category.category_id
            WHERE product.category_id = %s
            ORDER BY product.name ASC
        """
        rows = self.execute_query(query, (category_id,))
        products = []

        for row in rows:
            products.append(self._to_product(row))
        return products

    def search(self, search_term: str) -> List[Product]:
        query = """
            SELECT product.*, category.name AS category_name
            FROM products product
            LEFT JOIN categories category ON product.category_id = category.category_id
            WHERE product.name LIKE %s OR product.brand LIKE %s
            ORDER BY product.name ASC
        """
        term = f"%{search_term}%"
        rows = self.execute_query(query, (term, term))
        products = []

        for row in rows:
            products.append(self._to_product(row))
        return products

    def update_stock(self, product_id: int, quantity_delta: int) -> bool:
        query = """
            UPDATE products
            SET stock_quantity = stock_quantity + %s
            WHERE product_id = %s
        """
        return self.execute_statement(query, (quantity_delta, product_id))