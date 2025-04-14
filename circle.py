import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return math.pi * self.radius ** 2
    
    def __str__(self):
        return f"Circle: Radius = {self.radius}"
