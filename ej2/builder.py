from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Pizza:
    def __init__(self, name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.toppings = []
        self.cooking_technique = None
        self.presentation = None
        self.pairing = None
        self.extra_finish = None

    def set_dough(self, dough):
        self.dough = dough

    def set_sauce(self, sauce):
        self.sauce = sauce

    def set_toppings(self, toppings):
        self.toppings = toppings

    def set_cooking_technique(self, technique):
        self.cooking_technique = technique

    def set_presentation(self, presentation):
        self.presentation = presentation

    def set_pairing(self, pairing):
        self.pairing = pairing

    def set_extra_finish(self, finish):
        self.extra_finish = finish

    def list_ingredients(self):
        print(f"Dough: {self.dough}")
        print(f"Sauce: {self.sauce}")
        print(f"Toppings: {', '.join(self.toppings)}")
        print(f"Cooking Technique: {self.cooking_technique}")
        print(f"Presentation: {self.presentation}")
        print(f"Pairing: {self.pairing}")
        print(f"Extra Finish: {self.extra_finish}")


class PizzaBuilder(ABC):
    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def build_dough(self):
        pass
    
    @abstractmethod
    def build_sauce(self):
        pass
    
    @abstractmethod
    def build_toppings(self):
        pass
    
    @abstractmethod
    def build_cooking_technique(self):
        pass
    
    @abstractmethod
    def build_presentation(self):
        pass
    
    @abstractmethod
    def build_pairing(self):
        pass
    
    @abstractmethod
    def build_extra_finish(self):
        pass

class CustomPizzaBuilder(PizzaBuilder):
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.pizza = Pizza("Custom")
        
    def build_dough(self):
        self.pizza.set_dough(input("Choose dough (e.g., thin, thick, sourdough): "))
        
    def build_sauce(self):
        self.pizza.set_sauce(input("Choose sauce (e.g., tomato, alfredo, pesto): "))
        
    def build_toppings(self):
        toppings = self.choose_toppings()
        self.pizza.set_toppings(toppings)
    
    def build_cooking_technique(self):
        self.pizza.set_cooking_technique(input("Choose cooking technique (e.g., wood-fired, traditional oven): "))
        
    def build_presentation(self):
        self.pizza.set_presentation(input("Choose presentation (e.g., classic, artistic): "))
        
    def build_pairing(self):
        self.pizza.set_pairing(input("Choose pairing (e.g., red wine, beer, soda): "))
        
    def build_extra_finish(self):
        self.pizza.set_extra_finish(input("Choose extra finish (e.g., truffle oil, balsamic glaze): "))
    
    def choose_toppings(self):
        available_toppings = ["Pepperoni", "Mushrooms", "Onions", "Sausage", "Bacon", "Extra Cheese", "Olives"]
        print("Choose up to 5 toppings (type 'done' when finished):")
        chosen_toppings = []
        while len(chosen_toppings) < 5:
            print(f"Available toppings: {available_toppings}")
            topping = input("Enter topping: ")
            if topping.lower() == 'done':
                break
            elif topping in available_toppings:
                chosen_toppings.append(topping)
                available_toppings.remove(topping)
            else:
                print("Invalid topping. Please choose from available toppings.")
        return chosen_toppings

if __name__ == "__main__":
    builder = CustomPizzaBuilder()
    
    builder.build_dough()
    builder.build_sauce()
    builder.build_toppings()
    builder.build_cooking_technique()
    builder.build_presentation()
    builder.build_pairing()
    builder.build_extra_finish()
    
    pizza = builder.pizza
    pizza.list_ingredients()
