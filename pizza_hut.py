from pizza_store import PizzaStore

class PizzaHut(PizzaStore):
    def __init__(self, store_id: int, address: str, phone_number: str,
                 employees=None):
        super().__init__(store_id, "Pizza Hut", address, phone_number, employees)

    def calculate_rank(self) -> float:
        if self.number_of_employees == 0:
            self.rank = 0.0
        else:
            total = 0
            for employee in self._employees:
                total += employee.pizza_rank
            self.rank = total / self.number_of_employees
        return self.rank
