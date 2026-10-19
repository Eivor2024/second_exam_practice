from datetime import date, timedelta
from pizza_employee import PizzaEmployee
from pizza_hut import PizzaHut
from pizza_dominos import PizzaDominos
from pizza_voucher import PizzaVoucher


def print_top_three(store) -> None:
    print(f"\nTop 3 employees at {store.name} (before expiration):")
    remaining = store.employees  # A copy: removing here does not change the store.
    position = 1
    while position <= 3 and remaining:
        highest = remaining[0]
        for employee in remaining:
            if employee.pizza_rank > highest.pizza_rank:
                highest = employee
        print(f"{position}. {highest.first_name} {highest.last_name} "
              f"- rank: {highest.pizza_rank}")
        remaining.remove(highest)
        position += 1


def main() -> None:
    # 1. Supply initial ranks for predictable starting calculations.
    # Omit pizza_rank to generate a random initial rank instead.
    alice = PizzaEmployee(1, "Alice", "Cohen", "10 Main St", 6000, date(2025, 1, 1), pizza_rank=80)
    bob = PizzaEmployee(2, "Bob", "Levi", "20 Main St", 6500, date(2025, 2, 1), pizza_rank=60)
    dana = PizzaEmployee(3, "Dana", "David", "30 Main St", 7000, date(2025, 3, 1), pizza_rank=90)
    noam = PizzaEmployee(4, "Noam", "Katz", "40 Main St", 6200, date(2025, 4, 1), pizza_rank=95)
    maya = PizzaEmployee(5, "Maya", "Sharon", "50 Main St", 6400, date(2025, 5, 1), pizza_rank=85)
    omri = PizzaEmployee(6, "Omri", "Tal", "60 Main St", 6100, date(2025, 6, 1), pizza_rank=70)
    yael = PizzaEmployee(7, "Yael", "Barak", "70 Main St", 6800, date(2025, 7, 1), pizza_rank=98)
    liam = PizzaEmployee(8, "Liam", "Shalev", "80 Main St", 6300, date(2025, 8, 1), pizza_rank=82)
    roni = PizzaEmployee(9, "Roni", "Paz", "90 Main St", 6000, date(2025, 9, 1), pizza_rank=75)
    eyal = PizzaEmployee(10, "Eyal", "Golan", "100 Main St", 6500, date(2025, 10, 1), pizza_rank=65)

    # 2. Create both stores; each calculates its rank during construction.
    hut = PizzaHut(101, "1 Pizza St", "03-1111111", [alice, bob, noam, maya, omri])
    dominos = PizzaDominos(102, "2 Pizza St", "03-2222222", [dana, yael, liam, roni, eyal])
    print("INITIAL STORES")
    for store in (hut, dominos):
        print(f"{store.name}: employees={store.number_of_employees}, "
              f"expenses={store.calculate_employee_expenses():.2f}, "
              f"rank={store.rank:.2f}")

    # Display both leaderboards before changing any ranks or awarding gifts.
    print_top_three(hut)
    print_top_three(dominos)

    # 3. Make one rank old to demonstrate refreshing it.
    print("\nEXPIRATION AND RANK REFRESH")
    alice.pizza_rank_date = date.today() - timedelta(days=3)
    print(f"Demo: Alice Cohen's rank of {alice.pizza_rank} is now three days old.")
    print("Hut rank after refreshing:", hut.calculate_ranged_rank(1))
    print(f"Alice Cohen's new rank: {alice.pizza_rank}")

    # 4. Award each store's highest-ranked employees (including ties).
    print("\nSURPRISE WINNERS")
    for store in (hut, dominos):
        winners = store.get_best_employees()
        for employee in winners:
            voucher = PizzaVoucher()
            store.give_surprise(employee, voucher)
            print(f"{store.name} winner: {employee.first_name} {employee.last_name} "
                  f"- rank: {employee.pizza_rank}")
            employee.pizza_surprise.activate_surprise()

    # 5. A winner resigns; their surprise is returned automatically.
    print("\nRESIGNATION AND HIRING")
    hut_winners = hut.get_best_employees()
    leaving_employee = hut_winners[0]
    full_name = f"{leaving_employee.first_name} {leaving_employee.last_name}"
    hut.resign_employee(leaving_employee)
    print(f"{full_name} resigned from {hut.name}.")
    print(f"{full_name}'s surprise after resignation: {leaving_employee.pizza_surprise}")
    print("Hut employees after resignation:", hut.number_of_employees)

    # 6. Hire them at the other store.
    dominos.hire_employee(leaving_employee)
    print(f"{full_name} was hired by {dominos.name}.")
    print("Dominos employees after hiring:", dominos.number_of_employees)

    # 7. Show that hiring an existing employee is rejected.
    try:
        dominos.hire_employee(leaving_employee)
    except ValueError as error:
        print(f"Rejected duplicate hiring of {full_name} at {dominos.name}: {error}")


if __name__ == "__main__":
    main()
