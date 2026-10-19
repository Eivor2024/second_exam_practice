from pizza_store import PizzaStore

class PizzaDominos(PizzaStore):
    def __init__(self, store_id: int, address: str, phone_number: str,
                 employees=None):
        super().__init__(store_id, "Pizza Dominos", address, phone_number, employees)

    def calculate_rank(self) -> float:
        total = 0.0
        for employee in self._employees:
            total += employee.pizza_rank
        self.rank = total
        return self.rank
