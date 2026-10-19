from surprise import Surprise

class PizzaVoucher(Surprise):
    def activate_surprise(self) -> None:
        print("You got a surprise! Congratulations!")
