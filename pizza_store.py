from abc import ABC, abstractmethod
from datetime import date
from pizza_employee import PizzaEmployee


class PizzaStore(ABC):
    def __init__(self, store_id: int, name: str, address: str,
                 phone_number: str, employees=None):
        self.id = store_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self._employees = []
        if employees is not None:
            for employee in employees:
                if self._find_employee(employee.id) is not None:
                    raise ValueError("Employee IDs must be unique within a store.")
                self._employees.append(employee)
        self.rank = self.calculate_rank()

    @property
    def employees(self) -> list[PizzaEmployee]:
        return self._employees.copy()

    @property
    def number_of_employees(self) -> int:
        return len(self._employees)

    def _find_employee(self, employee_id: int):
        for employee in self._employees:
            if employee.id == employee_id:
                return employee
        return None

    def hire_employee(self, employee: PizzaEmployee) -> None:
        if self._find_employee(employee.id) is not None:
            raise ValueError("This employee already works at this store.")
        self._employees.append(employee)
        self.calculate_rank()

    def resign_employee(self, employee: PizzaEmployee) -> None:
        # Use the stored object, identified by ID, when changing its surprise.
        stored_employee = self._find_employee(employee.id)
        if stored_employee is None:
            raise ValueError("This employee does not work at this store.")
        stored_employee.pizza_surprise = None
        self._employees.remove(stored_employee)
        self.calculate_rank()

    def calculate_employee_expenses(self) -> float:
        total = 0.0
        for employee in self._employees:
            total += employee.salary
        return total

    @abstractmethod
    def calculate_rank(self) -> float:
        """Update and return the store rank using the store's own rule."""
        pass

    def calculate_ranged_rank(self, rank_range: int) -> float:
        if type(rank_range) is not int or rank_range < 0:
            raise ValueError("rank_range must be a non-negative integer.")
        today = date.today()
        for employee in self._employees:
            age = (today - employee.pizza_rank_date).days
            if age < 0 or age > rank_range:
                print(f"{self.name}: {employee.first_name} {employee.last_name}, "
                      "please rank the pizza again.")
                employee.set_rank()
        return self.calculate_rank()

    def get_best_employees(self) -> list[PizzaEmployee]:
        if not self._employees:
            return []
        highest_rank = self._employees[0].pizza_rank
        for employee in self._employees:
            if employee.pizza_rank > highest_rank:
                highest_rank = employee.pizza_rank

        winners = []
        for employee in self._employees:
            if employee.pizza_rank == highest_rank:
                winners.append(employee)
        return winners

    def give_surprise(self, employee: PizzaEmployee, surprise) -> None:
        stored_employee = self._find_employee(employee.id)
        if stored_employee is None:
            raise ValueError("This employee does not work at this store.")
        if stored_employee not in self.get_best_employees():
            raise ValueError("Surprises are awarded to the highest-ranked employees.")
        if not callable(getattr(surprise, "activate_surprise", None)):
            raise TypeError("A surprise must have an activate_surprise() method.")
        stored_employee.pizza_surprise = surprise
