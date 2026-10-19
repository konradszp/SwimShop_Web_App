from typing import List, Optional
from app.repositories.base import BaseRepository
from app.models.customer import Customer

class CustomerRepository(BaseRepository):
    def _to_customer(self, row:dict) -> Customer:
        return Customer(
            customer_id=row["customer_id"],
            full_name=row["full_name"],
            email=row["email"],
            phone=row["phone"],
            address=row["address"],
        )

    def get_all(self) -> list[Customer]:
        query = "SELECT * FROM customers ORDER BY full_name ASC"
        rows = self.execute_query(query)

        customers = []

        for row in rows:
            customers.append(self._to_customer(row))

        return customers


    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        query = "SELECT * FROM customers WHERE customer_id = %s"
        rows = self.execute_query(query, (customer_id,))

        if not rows:
            return None
        
        return self._to_customer(rows[0])

    def create(self, full_name: str, email: str, phone: str, address: str) -> int | None:
        query = """
            INSERT INTO customers (full_name, email, phone, address)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_insert(query, (full_name, email, phone, address))

    def update(self, customer_id: int, full_name: str, email: str, phone: str, address: str) -> bool:
        query = """
            UPDATE customers
            SET full_name = %s, email = %s, phone = %s, address = %s
            WHERE customer_id = %s
        """
        return self.execute_statement(query, (full_name, email, phone, address, customer_id))

    def delete(self, customer_id: int) -> bool:
        query = "DELETE FROM customers WHERE customer_id = %s"
        return self.execute_statement(query, (customer_id,))
        
        