from datetime import date
from random import randint

class PizzaEmployee:
    def __init__(self, employee_id: int, first_name: str, last_name: str,
                 address: str, salary: float, start_date: date, pizza_rank=None):
        if salary < 0:
            raise ValueError("Salary cannot be negative.")
        if pizza_rank is not None:
            if type(pizza_rank) is not int or not 1 <= pizza_rank <= 100:
                raise ValueError("Initial rank must be an integer from 1 to 100.")
        self.id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.salary = salary
        self.start_date = start_date
        self.pizza_surprise = None
        if pizza_rank is None:
            self.set_rank()
        else:
            self.pizza_rank = pizza_rank
            self.pizza_rank_date = date.today()

    def set_rank(self) -> None:
        self.pizza_rank = randint(1, 100)
        self.pizza_rank_date = date.today()
